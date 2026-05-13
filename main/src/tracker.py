import json
import os
from typing import Optional, Any


class RecordTracker:
    """Persistent tracker for rutmk_uid records using a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: dict[str, dict[str, Any]] = self._load()

    def _load(self) -> dict[str, dict[str, Any]]:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.file_path, 'w', encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def scan_new_records(self, db_connector, date_col: str, start_date: str):
        """
        Query database for rutmk_uid where date_col >= start_date and not already in tracker.
        Add them with status "NEW".
        Also fetch associated status‑history ParentNumbers and add them as status_history entries.
        """
        existing_uids = list(self.data.keys())
        if existing_uids:
            placeholders = ','.join(['%s'] * len(existing_uids))
            query = f"""
                SELECT rutmk_uid FROM fips_rutrademark
                WHERE {date_col} >= %s AND rutmk_uid NOT IN ({placeholders})
            """
            params = [start_date] + existing_uids
        else:
            query = f"""
                SELECT rutmk_uid FROM fips_rutrademark
                WHERE {date_col} >= %s
            """
            params = [start_date]

        rows = db_connector.fetchall(query, params)
        for row in rows:
            uid = row[0]
            if uid not in self.data:
                # initialise main record
                self.data[uid] = {
                    "status": "NEW",
                    "status_history": []   # will be filled below
                }

        # Now for each rutmk_uid (new or existing) we need to ensure its status_history
        # is up‑to‑date. We'll do it for all uids to catch newly added statuses later.
        # But to avoid excessive queries, we only do it for NEW uids here,
        # and let the periodic scan (or a separate step) handle updates.
        # For simplicity, we'll update status_history for all uids now.
        for uid in list(self.data.keys()):
            self._refresh_status_history(db_connector, uid)

        self.save()

    def _refresh_status_history(self, db_connector, uid: str):
        """Query the database for current ParentNumbers of statusHistory (Kind=150002) for this uid,
        along with OCCode, OCDate and CreatedDate."""
        query = """
            WITH obj AS (
                SELECT object_uid FROM fips_rutrademark WHERE rutmk_uid = %s
            ),
            status_objects AS (
                SELECT o2."Number" as parent_number
                FROM "Objects" o1
                JOIN "Objects" o2 ON o1."ParentNumber" = o2."ParentNumber"
                WHERE o1."Number" = (SELECT object_uid FROM obj)
                  AND o2."Kind" = '150002'
            )
            SELECT
                so.parent_number,
                sa_code."TextValue" as occ_code,
                sa_date."TextValue" as occ_date,
                COALESCE(sa_code."CreatedDate", sa_date."CreatedDate") as created_date
            FROM status_objects so
            LEFT JOIN "SearchAttributes" sa_code
                ON sa_code."ParentNumber" = so.parent_number AND sa_code."Name" = 'OCCode'
            LEFT JOIN "SearchAttributes" sa_date
                ON sa_date."ParentNumber" = so.parent_number AND sa_date."Name" = 'OCDate'
        """
        rows = db_connector.fetchall(query, (uid,))
        current_parents = {}
        for row in rows:
            parent = str(row[0])
            current_parents[parent] = {
                'occ_code_raw': row[1],
                'occ_date_raw': row[2],
                'created_date': str(row[3]) if row[3] else None
            }

        # Get existing status_history from tracker
        existing = self.data[uid].get("status_history", [])
        existing_map = {entry["parent_number"]: entry for entry in existing}

        new_history = []
        for parent, extra in current_parents.items():
            if parent in existing_map:
                # keep existing entry (status unchanged)
                new_history.append(existing_map[parent])
            else:
                # new statusHistory record with extra fields
                new_entry = {
                    "parent_number": parent,
                    "status": "NEW",
                    "path_to_xml": None,
                    "error_text": None,
                    **extra
                }
                new_history.append(new_entry)
        self.data[uid]["status_history"] = new_history

    def get_records_by_status(self, *statuses: str) -> list[tuple]:
        """Return list of (uid, record) for records whose overall status is in statuses."""
        result = []
        for uid, rec in self.data.items():
            if rec.get("status") in statuses:
                result.append((uid, rec))
        return result

    def get_status_history_entries_by_status(self, uid: str, *statuses: str) -> list[dict]:
        """Return list of status_history entries for the given uid whose status is in statuses."""
        entries = self.data.get(uid, {}).get("status_history", [])
        return [e for e in entries if e.get("status") in statuses]

    def update_record(self, uid: str, **kwargs):
        """Update fields for a main record. If the record does not exist, it is created."""
        if uid not in self.data:
            self.data[uid] = {}
        self.data[uid].update(kwargs)
        # remove keys with None value
        self.data[uid] = {k: v for k, v in self.data[uid].items() if v is not None}
        self.save()

    def update_status_history_entry(self, uid: str, parent_number: str, **kwargs):
        """Update a specific status_history entry."""
        if uid not in self.data:
            self.data[uid] = {"status_history": []}
        history = self.data[uid].setdefault("status_history", [])
        for entry in history:
            if entry["parent_number"] == parent_number:
                entry.update(kwargs)
                # remove keys with None
                for k in list(entry.keys()):
                    if entry[k] is None:
                        del entry[k]
                break
        else:
            # not found – add new
            new_entry = {"parent_number": parent_number}
            new_entry.update(kwargs)
            history.append(new_entry)
        self.save()

    def get_elk_order_number(self, uid: str) -> Optional[str]:
        return self.data.get(uid, {}).get("elkOrderNumber", None)

    def get_create_request_id(self, uid: str) -> Optional[str]:
        return self.data.get(uid, {}).get("createRequestId", None)

    def get_update_seq(self, uid: str) -> int:
        return self.data.get(uid, {}).get("update_seq", 0)

    def increment_update_seq(self, uid: str) -> int:
        if uid not in self.data:
            self.data[uid] = {}
        seq = self.data[uid].get("update_seq", 0) + 10
        self.data[uid]["update_seq"] = seq
        self.save()
        return seq

