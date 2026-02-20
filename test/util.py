import yaml


CONFIG_PATH_PROD = "../config.prod.yaml"
CONFIG_PATH_TEST = "../config.test.yaml"
LIMIT_ROWS = 10000
OUTPUT_DIR = "database"


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return {
        "host": config["host"],
        "port": config["port"],
        "dbname": config["dbname"],
        "user": config["user"],
        "password": config["password"]
    }

