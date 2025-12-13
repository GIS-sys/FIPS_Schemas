import copy
import json
import os

from src.logger import logger
from src.db_connector import DBConnector
from src.data_template import DataTemplate
from src.xml_generator import XMLGenerator

import src.config as config


def main():
    # Initialize class for connecting to the database and pulling data out of it
    db_connector = DBConnector(
        host=config.DB_HOST,
        port=config.DB_PORT,
        name=config.DB_NAME,
        user=config.DB_USER,
        pswd=config.DB_PASS
    )
    info = db_connector.get_debug_info()
    with open(config.FILE_DB_DEBUG, "w") as f:
        f.write(str(info))

    # Initialize class for work filling and validating XML
    xml_gen = XMLGenerator(config.FILE_SCHEMAS_XSD)

    # If no data template - create a default one
    # It will tell where to get data from the database, and how to convert it to an XML
    if not os.path.exists(config.FILE_TEMPLATE_JSON):
        example_json = DataTemplate.create_example_json()
        with open(config.FILE_TEMPLATE_JSON, "w") as f:
            json.dump(example_json, f, indent="\t")
        print(f"WARNING: No JSON template found\nSample JSON template was created in {config.FILE_TEMPLATE_JSON}\nChange it if needed\n\n")

    # Load data template
    with open(config.FILE_TEMPLATE_JSON, "r") as f:
        data_template_json = json.load(f)

    while db_connector.get_last_index() is not None:
        logger.set_file(config.DATA_FOLDER / f"log.{db_connector.get_last_index()}.txt", clear=True)
        # Main actions:
        # - gather data from the database according to the template
        # - convert the gathered data to XML
        # - validate XML against the XSD schema
        data_template = DataTemplate(copy.deepcopy(data_template_json))
        logger.log("\nDEBUG Data from template\n", data_template.data, "\n")
        last_id = data_template.fill_template(db_connector)
        logger.log("\nDEBUG Data filled from database\n", data_template.data, "\n")
        xml_data = xml_gen.json_to_xml(data_template.data)
        logger.log("\nDEBUG XML", xml_data, "\n")
        validation_result = xml_gen.validate_xml(xml_data)
        logger.log("XML Validation result:")
        if validation_result["valid"]:
            logger.log(f"OK {validation_result["message"]}")
            with open(config.DATA_FOLDER / f"{last_id}.xml", "w") as f:
                f.write(xml_data)
        else:
            logger.log("Failed!")
            logger.log("\nErrors:")
            for error in validation_result["errors"]:
                logger.log(f"  - {error}")
        db_connector.mark_last_index(last_id)
        logger.set_file(None)

    print("Everything was processed")


if __name__ == "__main__":
    main()
