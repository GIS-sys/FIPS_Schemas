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

STATUS_TEMPLATE_JSON = DATA_FOLDER / "status_template.json"



class LoadedConfig:
    def __init__(self, config_path: str):
        print(f"Loading config: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        self.db_appl_host = config["db_appl_host"]
        self.db_appl_port = config["db_appl_port"]
        self.db_appl_dbname = config["db_appl_dbname"]
        self.db_appl_user = config["db_appl_user"]
        self.db_appl_password = config["db_appl_password"]

        self.proxy_ip = config["proxy_ip"]
        self.proxy_ssh_user = config["proxy_ssh_user"]
        self.proxy_ssh_password = config["proxy_ssh_password"]

        self.api_ip = config["api_ip"]
        self.api_port = config["api_port"]
        self.api_bind_port = config["api_bind_port"]
        self.api_ssh_user = config["api_ssh_user"]
        self.api_ssh_password = config["api_ssh_password"]

        self.db_adapter_ip = config["db_adapter_ip"]
        self.db_adapter_port = config["db_adapter_port"]
        self.db_adapter_dbname = config["db_adapter_dbname"]
        self.db_adapter_user = config["db_adapter_user"]
        self.db_adapter_password = config["db_adapter_password"]

loaded_config = LoadedConfig("../config.test.yaml")
