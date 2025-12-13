from pathlib import Path

DATA_FOLDER = Path("./data")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)
FILE_SCHEMAS_XSD = DATA_FOLDER / "schemas.xsd"
FILE_TEMPLATE_JSON = DATA_FOLDER / "template.json"
FILE_DB_DEBUG = DATA_FOLDER / "db_debug.txt"

DB_HOST = "10.2.53.15"
DB_PORT = 5432
DB_NAME = "uad_int"
DB_USER = "gegorov"
DB_PASS = "87zerkaLo22"

MONITOR_STARTING_DATE_VAL = "2025-06-25"  # "2025-03-04"
MONITOR_STARTING_DATE_COL = "appl_receiving_date"
