from pathlib import Path
import yaml


DATA_FOLDER = Path("./data")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)
FILE_SCHEMAS_XSD = DATA_FOLDER / "schemas.xsd"
FILE_TEMPLATE_JSON = DATA_FOLDER / "template.json"
FILE_DB_DEBUG = DATA_FOLDER / "_db_debug.txt"

MONITOR_STARTING_DATE_VAL = "2026-02-15"
MONITOR_STARTING_DATE_COL = "appl_receiving_date"

# Add these lines at the end of config.py
TRACKER_JSON = DATA_FOLDER / "tracker.json"
SLEEP_INTERVAL = 10

CONFIG_PATH = "../config.test.yaml"
STATUS_TEMPLATE_JSON = DATA_FOLDER / "status_template.json"


def load_config_db_appl(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return {
        "host": config["db_appl_host"],
        "port": config["db_appl_port"],
        "dbname": config["db_appl_dbname"],
        "user": config["db_appl_user"],
        "password": config["db_appl_password"]
    }

