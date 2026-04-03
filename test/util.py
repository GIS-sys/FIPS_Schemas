import yaml


CONFIG_PATH_PROD = "../config.prod.yaml"
CONFIG_PATH_TEST = "../config.test.yaml"
LIMIT_ROWS = 10000
OUTPUT_DIR = "database"


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

