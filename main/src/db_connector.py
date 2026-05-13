import psycopg2
from sshtunnel import SSHTunnelForwarder

import src.config as config
from src.tunnel_manager import SingleThreadedTunnelManager


class DBConnector:
    def get_index_column_name(self) -> str:
        return "rutmk_uid"

    def fetchall(self, request: str, params: tuple = None) -> list:
        try:
            with SingleThreadedTunnelManager.instance().db_appl_connection() as conn:
                with conn.cursor() as cursor:
                    with conn.cursor() as cur:
                        if params:
                            cur.execute(request, params)
                        else:
                            cur.execute(request)
                        return cur.fetchall()
        except Exception:
            print("fetchall error:", request, params)
            raise

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
        result += f"\n\nAmount of data after {config.loaded_config.monitor_starting_date}:\n"
        result += str(self.fetchall(
            f"""
                SELECT COUNT(*) FROM fips_rutrademark WHERE ({config.MONITOR_STARTING_DATE_COL} >= '{config.loaded_config.monitor_starting_date}')
            """
        ))
        return result

