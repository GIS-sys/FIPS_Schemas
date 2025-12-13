import psycopg2

import src.config as config


class DBIndexTrackProcessed:
    def __init__(self):
        self.used: list[str] = []

    @classmethod
    def column(cls) -> str:
        return "rutmk_uid"

    def add(self, ind: str):
        self.used.append(ind)

    def where(self) -> str:
        if len(self.used) == 0:
            return "(true)"
        ind_str = ", ".join(["'" + ind + "'" for ind in self.used])
        return f"({self.column()} NOT IN ({ind_str}))"


class DBConnector:
    def __init__(self, host: str, port: int, name: str, user: str, pswd: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=name,
            user=user,
            password=pswd,
        )
        self.index_track = DBIndexTrackProcessed()

    def get_index_column_name(self) -> str:
        return self.index_track.column()

    def __del__(self):
        self.conn.close()

    def fetchall(self, request: str) -> list:
        with self.conn.cursor() as cur:
            cur.execute(request)
            data = cur.fetchall()
        return data

    def get_last_index(self):
        req = f"""
            SELECT {self.index_track.column()} FROM fips_rutrademark
            WHERE ({config.MONITOR_STARTING_DATE_COL} >= '{config.MONITOR_STARTING_DATE_VAL}') AND {self.index_track.where()}
            ORDER BY appl_receiving_date LIMIT 1
        """
        data = self.fetchall(req)
        print("TODO", data)
        if not data:
            return None
        return data[0][0]

    def mark_last_index(self, last_id):
        self.index_track.add(last_id)

    def get_debug_info(self) -> str:
        result = ""
        result += "All tables:\n"
        result += str(self.fetchall(
            """
                SELECT table_name
                FROM information_schema.tables
            """
        ))
        result += "\n\nSpecific table 'fips_rutrademark' columns:\n"
        result += str(self.fetchall(
            """
                SELECT column_name, data_type FROM information_schema.columns
                WHERE table_name = 'fips_rutrademark'
            """
        ))
        result += "\n\nSpecific table 'fips_contact' columns:\n"
        result += str(self.fetchall(
            """
                SELECT column_name, data_type FROM information_schema.columns
                WHERE table_name = 'fips_contact'
            """
        ))
        result += "\n\nSpecific table 'fips_rutrademark' data:\n"
        result += str(self.fetchall(
            """
                SELECT * FROM fips_rutrademark LIMIT 1
            """
        ))
        result += "\n\nSpecific table 'fips_contact' data:\n"
        result += str(self.fetchall(
            """
                SELECT * FROM fips_contact LIMIT 1
            """
        ))
        return result

