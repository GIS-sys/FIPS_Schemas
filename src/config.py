from pathlib import Path

DATA_FOLDER = Path("./data")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)
FILE_SCHEMAS_XSD = DATA_FOLDER / "schemas.xsd"
FILE_TEMPLATE_JSON = DATA_FOLDER / "template.json"

DB_HOST = "10.2.53.15"
DB_PORT = 5432
DB_NAME = "uad_int"
DB_USER = "gegorov"
DB_PASS = "87zerkaLo22"
