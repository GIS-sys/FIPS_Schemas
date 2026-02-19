from pathlib import Path
import yaml


DATA_FOLDER = Path("./data")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)
FILE_SCHEMAS_XSD = DATA_FOLDER / "schemas.xsd"
FILE_TEMPLATE_JSON = DATA_FOLDER / "template.json"
FILE_DB_DEBUG = DATA_FOLDER / "_db_debug.txt"

DB_HOST = "10.2.53.15"
DB_PORT = 5432
DB_NAME = "uad_int"
DB_USER = "gegorov"
DB_PASS = "87zerkaLo22"

MONITOR_STARTING_DATE_VAL = "2026-02-18"
MONITOR_STARTING_DATE_COL = "appl_receiving_date"

# Add these lines at the end of config.py
TRACKER_JSON = DATA_FOLDER / "tracker.json"
SLEEP_INTERVAL = 10

CONFIG_PATH = "../config.test.yaml"


def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return {
        "host": config["host"],
        "port": config["port"],
        "dbname": config["dbname"],
        "user": config["user"],
        "password": config["password"]
    }

