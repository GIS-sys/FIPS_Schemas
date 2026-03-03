import copy
import json
import os
import time
import traceback
from tqdm import tqdm

from src.logger import logger
from src.db_connector import DBConnector
from src.data_template import DataTemplate, clear_validation_errors, get_validation_errors, generate_status_history_dict
from src.xml_generator import XMLGenerator
from src.tracker import RecordTracker

import src.config as config


def main():
    print(f"Connecting to {config.CONFIG_PATH}")
    # Initialize database connection
    db_connector = DBConnector(**config.load_config(config.CONFIG_PATH))

    # Write debug info once (optional)
    info = db_connector.get_debug_info()
    with open(config.FILE_DB_DEBUG, "w", encoding="utf-8") as f:
        f.write(str(info))

    # Initialize XML generator
    xml_gen = XMLGenerator(config.FILE_SCHEMAS_XSD)

    # Create default template if missing
    if not os.path.exists(config.FILE_TEMPLATE_JSON):
        example_json = DataTemplate.create_example_json()
        with open(config.FILE_TEMPLATE_JSON, "w", encoding="utf-8") as f:
            json.dump(example_json, f, indent="\t")
        print(f"WARNING: No JSON template found\nSample JSON template was created in {config.FILE_TEMPLATE_JSON}\nChange it if needed\n\n")

    # Load the template once (it will be deep‑copied for each record)
    with open(config.FILE_TEMPLATE_JSON, "r", encoding="utf-8") as f:
        data_template_json = json.load(f)

    # Initialize the persistent tracker
    tracker = RecordTracker(config.TRACKER_JSON)

    # Main loop – runs forever, checking for new records and processing them
    while True:
        print("\n" * 16 + "New scan")
        # ----- Step 1: scan for new records (and refresh status_history) -----
        tracker.scan_new_records(
            db_connector,
            config.MONITOR_STARTING_DATE_COL,
            config.MONITOR_STARTING_DATE_VAL
        )

        # ----- Step 2: process records with status NEW or FORM_FAIL (main XML) -----
        for uid, rec in tqdm(tracker.get_records_by_status("NEW", "FORM_FAIL")):
            print("=" * 16)
            print(f"Tracking {uid} status={rec['status']}")
            logger.set_file(config.DATA_FOLDER / f"log.{uid}.txt", clear=True)
            try:
                # Create a fresh copy of the template for this record
                data_template = DataTemplate(copy.deepcopy(data_template_json))

                # Clear previous validation errors
                clear_validation_errors()

                # Fill the template using this uid as the starting index
                data_template.fill_template(db_connector, ind=uid)

                # Convert to XML
                xml_data = xml_gen.json_to_xml(data_template.data)
                xml_path = config.DATA_FOLDER / f"{uid}.xml"
                with open(xml_path, "w", encoding="utf-8") as f:
                    f.write(xml_data)

                # Check for custom validation errors
                errors = get_validation_errors()
                if errors:
                    error_msg = "Custom validation errors:\n" + "\n".join(errors)
                    raise Exception(error_msg)

                # Validate against XSD
                validation_result = xml_gen.validate_xml(xml_data)
                if validation_result.get("valid"):
                    tracker.update_record(uid, status="FORM_SUCC", path_to_xml=str(xml_path), error_text=None)
                    logger.log(f"XML generated and validated for {uid}", force_print=True)
                else:
                    error_msg = validation_result.get("message") or \
                                "; ".join(validation_result.get("errors", []))
                    tracker.update_record(uid, status="FORM_FAIL", error_text=error_msg)
                    logger.log(f"Validation failed for {uid}: {error_msg}", force_print=True)

            except Exception as e:
                tracker.update_record(uid, status="FORM_FAIL", error_text=str(e))
                logger.log(f"Exception while processing {uid}:\n{traceback.format_exc()}", force_print=True)

            logger.set_file(None)   # close per‑record log

        # ----- Step 3: process status_history entries (for records with any status) -----
        # We'll process all uids that have status_history entries with status NEW or VAL_FAIL
        for uid, rec in tracker.data.items():
            status_entries = tracker.get_status_history_entries_by_status(uid, "NEW", "VAL_FAIL")
            if not status_entries:
                continue
            print("=" * 16)
            print(f"Processing status_history for {uid}")
            logger.set_file(config.DATA_FOLDER / f"log.status.{uid}.txt", clear=True)

            # Re‑fill the full template for this uid (same as in step 2)
            try:
                data_template = DataTemplate(copy.deepcopy(data_template_json))
                clear_validation_errors()
                data_template.fill_template(db_connector, ind=uid)
                # The filled data now contains the full structure, including multiple statusHistory entries
                full_data = data_template.data
            except Exception as e:
                # If the main template cannot be filled, we cannot generate any status XML.
                # Mark all status entries as failed with this error.
                logger.log(f"Failed to fill main template for {uid} while processing status: {e}", force_print=True)
                for entry in status_entries:
                    tracker.update_status_history_entry(uid, entry["parent_number"],
                                                        status="VAL_FAIL",
                                                        error_text=f"Main template fill failed: {e}")
                logger.set_file(None)
                continue

            # Process each status entry individually
            for entry in status_entries:
                parent = entry["parent_number"]
                try:
                    # Generate the status data dict for this parent
                    status_dict = generate_status_history_dict(db_connector, parent)

                    # Clone the full filled data
                    cloned_data = copy.deepcopy(full_data)

                    # Replace the statusHistory list with a list containing only this status
                    # Path: CreateOrdersRequest.orders.order[0].statusHistoryList.statusHistory
                    try:
                        order_list = cloned_data["CreateOrdersRequest"]["orders"]["order"]
                        if not isinstance(order_list, list) or len(order_list) == 0:
                            raise Exception("Invalid structure: order list missing")
                        order = order_list[0]
                        status_history_list = order["statusHistoryList"]["statusHistory"]
                        # Replace with a single-element list
                        order["statusHistoryList"]["statusHistory"] = [status_dict]
                    except KeyError as e:
                        raise Exception(f"Could not locate statusHistoryList in template: {e}")

                    # Convert to XML
                    xml_data = xml_gen.json_to_xml(cloned_data)  # root tag defaults to "ElkOrderRequest"
                    xml_path = config.DATA_FOLDER / f"{uid}.{parent}.xml"
                    with open(xml_path, "w", encoding="utf-8") as f:
                        f.write(xml_data)

                    # Check for custom validation errors (from generate_status_history_dict or elsewhere)
                    errors = get_validation_errors()
                    if errors:
                        error_msg = "Custom validation errors for status:\n" + "\n".join(errors)
                        raise Exception(error_msg)

                    # Optionally validate against XSD (if you have a schema for status updates, you could call xml_gen.validate_xml again)
                    tracker.update_status_history_entry(uid, parent,
                                                        status="VAL_SUCCESS",
                                                        path_to_xml=str(xml_path),
                                                        error_text=None)
                    logger.log(f"Status XML for {parent} generated and validated", force_print=True)

                except Exception as e:
                    tracker.update_status_history_entry(uid, parent,
                                                        status="VAL_FAIL",
                                                        error_text=str(e))
                    logger.log(f"Exception while processing status {parent}:\n{traceback.format_exc()}", force_print=True)

                # Clear validation errors after each status entry to avoid mixing
                clear_validation_errors()

            logger.set_file(None)

        ## ----- Step 4: check FORM_SUCC records for Kind = 150002 (unchanged) -----
        #for uid, rec in tqdm(tracker.get_records_by_status("FORM_SUCC")):
        #    print("=" * 16)
        #    print(f"Tracking {uid} status={rec['status']}")
        #    try:
        #        kinds = db_connector.get_kinds_for_object_parent(uid)
        #        if "150002" in kinds:
        #            tracker.update_record(uid, status="150002")
        #            logger.log(f"Record {uid} has Kind=150002, status updated.", force_print=True)
        #        else:
        #            logger.log(f"Record {uid} DOESN'T have Kind=150002, skipping.", force_print=True)
        #    except Exception:
        #        logger.log(f"Exception checking Kind for {uid}:\n{traceback.format_exc()}", force_print=True)

        ## ----- Step 5: check FORM_SUCC records for Kind = 150002 (unchanged) -----
        #for uid, rec in tqdm(tracker.get_records_by_status("150002")):
        #    print("=" * 16)
        #    print(f"NEED TO SEND {rec['path_to_xml']}")
        # ----- Step 5: check FORM_SUCC records for Kind = 150002 (unchanged) -----
        for uid, rec in tqdm(tracker.get_records_by_status("FORM_SUCC")):
            for hist in tracker.get_status_history_entries_by_status(uid, "VAL_SUCCESS"):
                print("=" * 16)
                print(f"NEED TO SEND {hist['path_to_xml']}")

        # Wait before next iteration
        print("Scan finished" + "\n" * 16)
        time.sleep(config.SLEEP_INTERVAL)


if __name__ == "__main__":
    main()

