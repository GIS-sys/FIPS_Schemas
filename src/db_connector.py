import psycopg2


class DBIndex:
    def __init__(self, value):
        self.value = value

    @classmethod
    def column(cls) -> str:
        return "appl_receiving_date"

    def where(self) -> str:
        return f"({self.column()} > '{self.value}')"


class DBConnector:
    def __init__(self, host: str, port: int, name: str, user: str, pswd: str):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=name,
            user=user,
            password=pswd,
        )
        self.LAST_INDEX = DBIndex("2025-06-25")  # "2025-03-04" # 2025880254 # TODO

    def __del__(self):
        self.conn.close()

    def fetchall(self, request: str) -> list:
        with self.conn.cursor() as cur:
            cur.execute(request)
            data = cur.fetchall()
        return data

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

