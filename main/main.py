import copy
import json
import os
import time

from src.logger import logger
from src.db_connector import DBConnector
from src.data_template import DataTemplate
from src.xml_generator import XMLGenerator
from src.tracker import RecordTracker

import src.config as config


def main():
    print(f"Connecting to {config.CONFIG_PATH}")
    # Initialize database connection
    db_connector = DBConnector(**config.load_config(config.CONFIG_PATH))

    # Write debug info once (optional)
    info = db_connector.get_debug_info()
    with open(config.FILE_DB_DEBUG, "w") as f:
        f.write(str(info))

    # Initialize XML generator
    xml_gen = XMLGenerator(config.FILE_SCHEMAS_XSD)

    # Create default template if missing
    if not os.path.exists(config.FILE_TEMPLATE_JSON):
        example_json = DataTemplate.create_example_json()
        with open(config.FILE_TEMPLATE_JSON, "w") as f:
            json.dump(example_json, f, indent="\t")
        print(f"WARNING: No JSON template found\nSample JSON template was created in {config.FILE_TEMPLATE_JSON}\nChange it if needed\n\n")

    # Load the template once (it will be deep‑copied for each record)
    with open(config.FILE_TEMPLATE_JSON, "r") as f:
        data_template_json = json.load(f)

    # Initialize the persistent tracker
    tracker = RecordTracker(config.TRACKER_JSON)

    # Main loop – runs forever, checking for new records and processing them
    while True:
        print("\n\n\nNew scan")
        # ----- Step 1: scan for new records -----
        tracker.scan_new_records(
            db_connector,
            config.MONITOR_STARTING_DATE_COL,
            config.MONITOR_STARTING_DATE_VAL
        )

        # ----- Step 2: process records with status NEW or FORM_FAIL -----
        for uid, rec in tracker.get_records_by_status("NEW", "FORM_FAIL"):
            print("=" * 16)
            print(f"Tracking {uid} status={rec['status']}")
            logger.set_file(config.DATA_FOLDER / f"log.{uid}.txt", clear=True)
            try:
                # Create a fresh copy of the template for this record
                data_template = DataTemplate(copy.deepcopy(data_template_json))

                # Fill the template using this uid as the starting index
                data_template.fill_template(db_connector, ind=uid)

                # Convert to XML
                xml_data = xml_gen.json_to_xml(data_template.data)
                xml_path = config.DATA_FOLDER / f"{uid}.xml"
                with open(xml_path, "w") as f:
                    f.write(xml_data)

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
                logger.log(f"Exception while processing {uid}: {e}", force_print=True)

            logger.set_file(None)   # close per‑record log

        # ----- Step 3: check FORM_SUCC records for Kind = 150002 -----
        for uid, rec in tracker.get_records_by_status("FORM_SUCC"):
            print("=" * 16)
            print(f"Tracking {uid} status={rec['status']}")
            try:
                kinds = db_connector.get_kinds_for_object_parent(uid)
                if "150002" in kinds:
                    tracker.update_record(uid, status="150002")
                    logger.log(f"Record {uid} has Kind=150002, status updated.", force_print=True)
                else:
                    logger.log(f"Record {uid} DOESN'T have Kind=150002, skipping.", force_print=True)
            except Exception as e:
                # Log error but do not change status – will be retried next cycle?
                # Here we simply log it; you might want to set a temporary error field.
                logger.log(f"Error checking Kind for {uid}: {e}", force_print=True)

        # ----- Step 4: check FORM_SUCC records for Kind = 150002 -----
        for uid, rec in tracker.get_records_by_status("150002"):
            print("=" * 16)
            print(f"NEED TO SEND {rec['path_to_xml']}")

        # Wait before next iteration
        print("Scan finished\n\n\n")
        time.sleep(config.SLEEP_INTERVAL)


if __name__ == "__main__":
    main()

