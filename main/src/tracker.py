import json
import os
from typing import Dict, List, Optional, Any


class RecordTracker:
    """Persistent tracker for rutmk_uid records using a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Dict[str, Dict[str, Any]] = self._load()

    def _load(self) -> Dict[str, Dict[str, Any]]:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def scan_new_records(self, db_connector, date_col: str, start_date: str):
        """
        Query database for rutmk_uid where date_col >= start_date and not already in tracker.
        Add them with status "NEW".
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
            if uid not in self.data:          # safety check
                self.data[uid] = {"status": "NEW"}
        self.save()

    def get_records_by_status(self, *statuses: str) -> List[tuple]:
        """Return list of (uid, record) for records whose status is in statuses."""
        result = []
        for uid, rec in self.data.items():
            if rec.get("status") in statuses:
                result.append((uid, rec))
        return result

    def update_record(self, uid: str, **kwargs):
        """Update fields for a record. If the record does not exist, it is created."""
        if uid not in self.data:
            self.data[uid] = {}
        self.data[uid].update(kwargs)
        self.save()

