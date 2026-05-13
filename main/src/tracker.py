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
        """Query the database for current ParentNumbers of statusHistory (Kind=150002) for this uid."""
        query = """
            WITH obj AS (
                SELECT object_uid FROM fips_rutrademark WHERE rutmk_uid = %s
            )
            SELECT o2."Number"
            FROM "Objects" o1
            JOIN "Objects" o2 ON o1."ParentNumber" = o2."ParentNumber"
            WHERE o1."Number" = (SELECT object_uid FROM obj)
              AND o2."Kind" = '150002'
        """
        rows = db_connector.fetchall(query, (uid,))
        current_parents = {str(row[0]) for row in rows}

        # Get existing status_history from tracker
        existing = self.data[uid].get("status_history", [])
        existing_map = {entry["parent_number"]: entry for entry in existing}

        new_history = []
        for parent in current_parents:
            if parent in existing_map:
                # keep existing entry (status unchanged)
                new_history.append(existing_map[parent])
            else:
                # new statusHistory record
                new_history.append({
                    "parent_number": parent,
                    "status": "NEW",
                    "path_to_xml": None,
                    "error_text": None
                })
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

