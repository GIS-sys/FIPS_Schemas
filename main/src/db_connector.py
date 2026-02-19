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
    def __init__(self, host: str, port: int, dbname: str, user: str, password: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=dbname,
            user=user,
            password=password,
        )
        self.index_track = DBIndexTrackProcessed()

    def get_index_column_name(self) -> str:
        return self.index_track.column()

    def __del__(self):
        self.conn.close()

    def fetchall(self, request: str, params: tuple = None) -> list:
        with self.conn.cursor() as cur:
            if params:
                cur.execute(request, params)
            else:
                cur.execute(request)
            data = cur.fetchall()
        return data

    def get_kinds_for_object_parent(self, rutmk_uid: str) -> list[int]:
        """
        Given a rutmk_uid, return all Kind values from the Objects table
        that share the same Parent as the object linked to this rutmk_uid.
        """
        query = """
            WITH obj AS (
                SELECT object_uid FROM fips_rutrademark WHERE rutmk_uid = %s
            )
            SELECT o2."Kind"
            FROM "Objects" o1
            JOIN "Objects" o2 ON o1."ParentNumber" = o2."ParentNumber"
            WHERE o1."Number" = (SELECT object_uid FROM obj)
        """
        rows = self.fetchall(query, (rutmk_uid,))
        return [str(row[0]) for row in rows]

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
        result += f"\n\nAmount of data after {config.MONITOR_STARTING_DATE_VAL}:\n"
        result += str(self.fetchall(
            f"""
                SELECT COUNT(*) FROM fips_rutrademark WHERE ({config.MONITOR_STARTING_DATE_COL} >= '{config.MONITOR_STARTING_DATE_VAL}')
            """
        ))
        return result

