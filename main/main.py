import copy
from datetime import datetime
import json
import os
import shutil
import time
import traceback
from tqdm import tqdm

from src.logger import logger
from src.db_connector import DBConnector
from src.data_template import DataTemplate, clear_validation_errors, get_validation_errors
from src.xml_generator import XMLGenerator
from src.tracker import RecordTracker
from src.adapter import send_xml_path, execute_psql, parse_adapter_response

import src.config as config


def main():
    # Initialize database connection
    db_connector = DBConnector()

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

    # Create default update template if missing
    if not os.path.exists(config.FILE_TEMPLATE_UPDATE_JSON):
        example_update_json = DataTemplate.create_update_example_json()
        with open(config.FILE_TEMPLATE_UPDATE_JSON, "w", encoding="utf-8") as f:
            json.dump(example_update_json, f, indent="\t")
        print(f"WARNING: No JSON update template found\nSample JSON update template was created in {config.FILE_TEMPLATE_UPDATE_JSON}\nChange it if needed\n\n")

    # Load both templates
    with open(config.FILE_TEMPLATE_JSON, "r", encoding="utf-8") as f:
        data_template_json = json.load(f)
    with open(config.FILE_TEMPLATE_UPDATE_JSON, "r", encoding="utf-8") as f:
        data_template_update_json = json.load(f)

    # Initialize the persistent tracker
    tracker = RecordTracker(config.TRACKER_JSON)

    # Main loop – runs forever, checking for new records and processing them
    while True:
        print("\n" * 16 + "New scan", flush=True)
        # BACKUP: создаём папку для бэкапов текущего цикла
        backup_dir = config.DATA_FOLDER / f"backup.{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        def backup_tracker(step_num: int):
            """Копирует tracker.json в папку бэкапа с указанием шага."""
            try:
                shutil.copy(config.TRACKER_JSON, backup_dir / f"tracker.step{step_num}.json")
            except Exception as e:
                print(f"Error while backing up a tracker file for step: {step_num}")

        # ----- Step 1: scan for new records (and refresh status_history) -----
        print("\n" * 8 + "STEP 1")
        tracker.scan_new_records(
            db_connector,
            config.MONITOR_STARTING_DATE_COL,
            config.loaded_config.monitor_starting_date
        )
        backup_tracker(1)

        # ----- Step 2: process records with status NEW or FORM_FAIL (main XML) -----
        print("\n" * 8 + "STEP 2")
        for loop_i, (uid, rec) in enumerate(tqdm(tracker.get_records_by_status("NEW", "FORM_FAIL"))):
            print("=" * 16, loop_i, flush=True)
            print(f"Tracking {uid} status={rec['status']}", flush=True)
            logger.set_file(config.DATA_FOLDER / f"log.{uid}.txt", clear=True)

            try:
                # Create a fresh copy of the template for this record
                data_template = DataTemplate(copy.deepcopy(data_template_json))
                # Clear previous validation errors
                clear_validation_errors()
                # Fill the template using this uid as the starting index
                data_template.fill_template(db_connector, ind=uid)

                # Convert to XML
                # --- Копия для валидации: подменяем статусы заглушкой ---
                full_data = data_template.data
                validation_data = copy.deepcopy(full_data)
                try:
                    order = validation_data["CreateOrdersRequest"]["orders"]["order"][0]
                    dummy_status = {
                        "status": "0",
                        "statusDate": "2026-01-01T12:00:00.000000",
                        "MessageType": "."
                    }
                    order["statusHistoryList"]["statusHistory"] = [dummy_status]
                except KeyError as e:
                    raise Exception(f"Could not locate statusHistoryList in template: {e} {validation_data}")
                xml_data = xml_gen.json_to_xml(validation_data)
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
        backup_tracker(2)

        # ----- Step 3: process status_history entries for records with FORM_SUCC -----
        print("\n" * 8 + "STEP 3")
        for loop_i, (uid, rec) in enumerate(tqdm(tracker.data.items())):
            if rec.get("status") != "FORM_SUCC":
                continue
            # Determine mode
            elk_order_number = tracker.get_elk_order_number(uid)
            create_request_id = tracker.get_create_request_id(uid)
            # If no elkOrderNumber and no pending create, we are in Create mode.
            if elk_order_number is None and create_request_id is None:
                # We will select exactly one status entry to process.
                status_entries = tracker.get_status_history_entries_by_status(uid, "NEW", "VAL_FAIL")
                if not status_entries:
                    continue
                # Choose the one with code 940
                chosen_entry = None
                for entry in status_entries:
                    if entry.get('occ_code_raw') == '940':
                        chosen_entry = entry
                        break
                if chosen_entry is None:
                    logger.log(f"No status with OCCode=940 found for uid {uid}, skipping Create", force_print=True)
                    continue
                # Store its parent_number as createRequestId
                tracker.update_record(uid, createRequestId=chosen_entry["parent_number"])
                # Process only this entry as a Create request
                entries_to_process = [chosen_entry]
                is_create_mode = True
            elif elk_order_number is None:
                # We are waiting for elkOrderNumber
                continue
            else:
                # Update mode: process all entries that are NEW or VAL_FAIL
                entries_to_process = tracker.get_status_history_entries_by_status(uid, "NEW", "VAL_FAIL")
                entries_to_process.sort(key=lambda e: e.get('created_date') or '')
                is_create_mode = False
            if not entries_to_process:
                continue

            print("=" * 16, loop_i, flush=True)
            print(f"Processing status_history for {uid}", flush=True)
            logger.set_file(config.DATA_FOLDER / f"log.status.{uid}.txt", clear=True)
            # Re‑fill the full template for this uid (same as in step 2)
            try:
                if is_create_mode:
                    template_json = data_template_json
                    request_key = "CreateOrdersRequest"
                else:
                    template_json = data_template_update_json
                    request_key = "UpdateOrdersRequest"
                data_template = DataTemplate(copy.deepcopy(template_json))
                clear_validation_errors()
                data_template.fill_template(db_connector, ind=uid)
                # The filled data now contains the full structure, including multiple statusHistory entries
                full_data = data_template.data
                order_number = full_data[request_key]["orders"]["order"][0].get("orderNumber")
            except Exception as e:
                logger.log(f"Failed to fill main template for {uid}: {e}", force_print=True)
                for entry in entries_to_process:
                    tracker.update_status_history_entry(uid, entry["parent_number"],
                                                        status="VAL_FAIL",
                                                        error_text=f"Main template fill failed: {e}")
                logger.set_file(None)
                continue

            # Process each status entry individually
            for entry in entries_to_process:
                parent = entry["parent_number"]
                try:
                    # Clone the full filled data
                    cloned_data = copy.deepcopy(full_data)
                    # Replace orderNumber with elkOrderNumber if in Update mode
                    if not is_create_mode:
                        # For Update, use elkOrderNumber from tracker
                        if elk_order_number is None:
                            raise Exception("Update mode but elkOrderNumber is missing")
                        order_elem = cloned_data[request_key]["orders"]["order"][0]
                        order_elem["elkOrderNumber"] = elk_order_number

                    # Replace the statusHistory list with a list containing only this status
                    # Path: request_key.orders.order[0].statusHistoryList.statusHistory
                    try:
                        order_list = cloned_data[request_key]["orders"]["order"]
                        if not isinstance(order_list, list) or len(order_list) == 0:
                            raise Exception("Invalid structure: order list missing")
                        order = order_list[0]
                        # Replace with a single-element list
                        status_dict = None
                        for specific_history in order["statusHistoryList"]["statusHistory"]:
                            if specific_history["_debug_parent"] == parent:
                                status_dict = copy.deepcopy(specific_history)
                                status_dict.pop("_debug_parent")
                                break
                        if status_dict is None:
                            raise Exception(f"No status history entry with _debug_parent={parent} found!")
                        order["statusHistoryList"]["statusHistory"] = [status_dict]
                        status_date = status_dict.get("statusDate")
                    except KeyError as e:
                        raise Exception(f"Could not locate statusHistoryList: {e}")

                    # For Update mode, apply sequential timestamp suffix
                    if not is_create_mode:
                        seq = tracker.increment_update_seq(uid)
                        # status_date is like "2026-04-16T12:00:00.000000"
                        # Replace the last 6 digits with zero-padded seq
                        if status_date and len(status_date) >= 20 and "." in status_date:
                            base = status_date[:status_date.rindex(".")+1]
                            new_status_date = f"{base}{seq:06d}"
                            status_dict["statusDate"] = new_status_date
                            status_date = new_status_date

                    # Convert to XML
                    xml_data = xml_gen.json_to_xml(cloned_data)
                    xml_path = config.DATA_FOLDER / f"{uid}.{parent}.xml"
                    with open(xml_path, "w", encoding="utf-8") as f:
                        f.write(xml_data)

                    # Check for custom validation errors (from generate_status_history_dict or elsewhere)
                    errors = get_validation_errors()
                    if errors:
                        error_msg = "Custom validation errors:\n" + "\n".join(errors)
                        raise Exception(error_msg)

                    # XSD валидация (раньше отсутствовала)
                    validation_result = xml_gen.validate_xml(xml_data)
                    if validation_result.get("valid"):
                        kwarg = {'order_number': order_number} if is_create_mode else {'elk_order_number': elk_order_number}
                        tracker.update_status_history_entry(uid, parent,
                                                            status="VAL_SUCCESS",
                                                            path_to_xml=str(xml_path),
                                                            status_date=status_date,
                                                            error_text=None,
                                                            **kwarg)
                        logger.log(f"Status XML for {parent} generated and validated", force_print=True)
                    else:
                        error_msg = validation_result.get("message") or \
                                    "; ".join(validation_result.get("errors", []))
                        tracker.update_status_history_entry(uid, parent,
                                                            status="VAL_FAIL",
                                                            error_text=error_msg)
                        logger.log(f"XSD validation failed for status {parent}: {error_msg}", force_print=True)

                except Exception as e:
                    tracker.update_status_history_entry(uid, parent,
                                                        status="VAL_FAIL",
                                                        error_text=str(e))
                    logger.log(f"Exception while processing status {parent}:\n{traceback.format_exc()}", force_print=True)

                # Clear validation errors after each status entry to avoid mixing
                clear_validation_errors()
            logger.set_file(None)
        backup_tracker(3)

        # ----- Step 4: send XMLs with status VAL_SUCCESS -----
        print("\n" * 8 + "STEP 4")
        for loop_i, (uid, rec) in enumerate(tqdm(tracker.data.items())):
            if rec.get("status") != "FORM_SUCC":
                continue
            status_entries = tracker.get_status_history_entries_by_status(uid, "VAL_SUCCESS", "SEND_ERROR")
            if not status_entries:
                continue
            print("=" * 16, loop_i, flush=True)
            print(f"Sending valid xmls for {uid}", flush=True)
            logger.set_file(config.DATA_FOLDER / f"log.sending.{uid}.txt", clear=True)

            history = rec.get("status_history", [])
            for entry in history:
                if entry.get("status") not in ("VAL_SUCCESS", "SEND_ERROR"):
                    continue
                xml_path = entry.get("path_to_xml")
                if not xml_path:
                    continue
                try:
                    logger.log(f"Sending XML {xml_path}", force_print=True)
                    response = send_xml_path(xml_path)
                    tracker.update_status_history_entry(
                        uid, entry["parent_number"],
                        status="SENT_INFO",
                        delivery_time=time.time(),
                        delivery_response=f"{response.status_code} {response.text}",
                        delivery_error=None
                    )
                    logger.log(f"Sent status XML for {uid}/{entry['parent_number']}, response {response.status_code} {response.text}", force_print=True)
                except Exception as e:
                    logger.log(f"Failed to send XML for {uid}/{entry['parent_number']}: {e}", force_print=True)
                    tracker.update_status_history_entry(
                        uid, entry["parent_number"],
                        status="SEND_ERROR",
                        delivery_error=str(e)
                    )
            logger.set_file(None)
        backup_tracker(4)

        # ----- Step 5: check delivery logs for SENT_INFO entries -----
        print("\n" * 8 + "STEP 5")
        for loop_i, (uid, rec) in enumerate(tqdm(tracker.data.items())):
            if rec.get("status") != "FORM_SUCC":
                continue
            status_entries = tracker.get_status_history_entries_by_status(uid, "SENT_INFO")
            if not status_entries:
                continue
            print("=" * 16, loop_i, flush=True)
            print(f"Checking delivery status for {uid}", flush=True)
            logger.set_file(config.DATA_FOLDER / f"log.delivery_check.{uid}.txt", clear=True)

            history = rec.get("status_history", [])
            for entry in history:
                if entry.get("status") != "SENT_INFO":
                    continue
                order_number = entry.get("order_number") or entry.get("elk_order_number")
                status_date = entry.get("status_date")
                if not order_number or not status_date:
                    logger.log(f"Skipping {entry['parent_number']}: {order_number=} {status_date=}", force_print=True)
                    continue
                like_pattern = f"%{order_number}%{status_date}%"
                query = f"SELECT client_id FROM core.delivery_log WHERE smev_message LIKE '{like_pattern}' ORDER BY created_at DESC;"
                try:
                    rows = execute_psql(query)
                    if rows:
                        tracker.update_status_history_entry(
                            uid, entry["parent_number"],
                            status="DELIVERED",
                            delivery_client_id=rows[0][0]
                        )
                        logger.log(f"Delivery confirmed for {uid}/{entry['parent_number']}, id={rows[0][0]}", force_print=True)
                    else:
                        logger.log(f"No delivery log entry yet for {uid}/{entry['parent_number']} (pattern={like_pattern})", force_print=True)
                except Exception as e:
                    logger.log(f"Error checking delivery for {uid}/{entry['parent_number']}: {e}", force_print=True)
            logger.set_file(None)
        backup_tracker(5)

        # ----- Step 6: check for SMEV response for entries with status DELIVERED or RESPONSE_PARSE_ERROR -----
        print("\n" * 8 + "STEP 6")
        for loop_i, (uid, rec) in enumerate(tqdm(tracker.data.items())):
            if rec.get("status") != "FORM_SUCC":
                continue
            status_entries = tracker.get_status_history_entries_by_status(uid, "DELIVERED", "RESPONSE_PARSE_ERROR")
            if not status_entries:
                continue
            print("=" * 16, loop_i, flush=True)
            print(f"Checking SMEV response for {uid}", flush=True)
            logger.set_file(config.DATA_FOLDER / f"log.smev_response.{uid}.txt", clear=True)

            history = rec.get("status_history", [])
            for entry in history:
                if entry.get("status") not in ("DELIVERED", "RESPONSE_PARSE_ERROR"):
                    continue
                client_id = entry.get("delivery_client_id")
                if not client_id:
                    continue
                query = f"""
                    SELECT id, smev_response FROM core.delivery_log
                    WHERE reference_client_id = '{client_id}'
                      AND (message_type = 'RESPONSE' OR message_type = 'REJECT')
                      AND status = 'FINISHED'
                      AND stage = 'WS'
                    ORDER BY created_at DESC
                    LIMIT 1
                """
                try:
                    rows = execute_psql(query)
                    if rows:
                        response_id, message_content = rows[0]
                        parsed_data, parse_error = parse_adapter_response(message_content)

                        if parse_error is None:
                            if len(parsed_data.get('orders', [])) != 1:
                                raise Exception(f"Got several or none orders in response, expected exactly 1: {parsed_data.get('orders', [])}")
                            tracker.update_status_history_entry(
                                uid, entry["parent_number"],
                                status="RESPONSE_RECEIVED",
                                response_log_id=response_id,
                                response_content=message_content if message_content else None,
                                response_content_parsed=parsed_data,
                                parse_error=None,
                                parse_error_data=None
                            )
                            logger.log(f"SMEV response received and parsed for {uid}/{entry['parent_number']}, {response_id=}, {parsed_data=}", force_print=True)
                            # If this is a successful Create response, store elkOrderNumber
                            if parsed_data.get('type') == 'CreateOrdersResponse':
                                # Extract elkOrderNumber from the first order
                                elk_num = parsed_data['orders'][0].get('elkOrderNumber')
                                if elk_num:
                                    tracker.update_record(uid, elkOrderNumber=elk_num)
                                logger.log(f"Stored elkOrderNumber={elk_num} for {uid}", force_print=True)
                        else:
                            tracker.update_status_history_entry(
                                uid, entry["parent_number"],
                                status="RESPONSE_PARSE_ERROR",
                                response_log_id=response_id,
                                response_content=message_content if message_content else None,
                                parse_error=parse_error,
                                parse_error_data=parsed_data
                            )
                            logger.log(f"SMEV response parsing failed for {uid}/{entry['parent_number']}: {parse_error}\n{parsed_data}", force_print=True)
                    else:
                        logger.log(f"No FINISHED RESPONSE/REJECT from WS yet for client_id={client_id}", force_print=True)
                except Exception as e:
                    logger.log(f"Error checking SMEV response for {uid}/{entry['parent_number']}: {e}", force_print=True)
            logger.set_file(None)
        backup_tracker(6)

        # BACKUP: копируем все логи за текущий цикл в папку бэкапа
        for log_file in config.DATA_FOLDER.glob("log.*.txt"):
            try:
                shutil.move(log_file, backup_dir / log_file.name)
            except Exception as e:
                print(f"Error while backing up a log file: {log_file}")
        # Wait before next iteration
        print("Scan finished" + "\n" * 16, flush=True)
        time.sleep(config.loaded_config.sleep_interval)

if __name__ == "__main__":
    main()

