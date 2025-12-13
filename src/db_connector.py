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

    def print_debug_info(self):
        print("All tables:")
        print(self.fetchall(
            """
                SELECT table_name
                FROM information_schema.tables
            """
        ))
        print("\nSpecific table 'fips_rutrademark' columns:")
        print(self.fetchall(
            """
                SELECT column_name, data_type FROM information_schema.columns
                WHERE table_name = 'fips_rutrademark'
            """
        ))
        print("\nSpecific table 'fips_contact' columns:")
        print(self.fetchall(
            """
                SELECT column_name, data_type FROM information_schema.columns
                WHERE table_name = 'fips_contact'
            """
        ))
        print("\nSpecific table 'fips_rutrademark' data:")
        print(self.fetchall(
            """
                SELECT * FROM fips_rutrademark LIMIT 1
            """
        ))
        print("\nSpecific table 'fips_contact' data:")
        print(self.fetchall(
            """
                SELECT * FROM fips_contact LIMIT 1
            """
        ))

