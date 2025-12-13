from typing import Any, Self

from src.db_connector import DBConnector
from src.logger import logger


class DataTemplateHowToElement:
    def __init__(self, table_name: str, column_name: str, condition_column: str = None, after: str = None):
        self.table_name = table_name
        self.column_name = column_name
        self.condition_column = condition_column
        self.after = after

    @staticmethod
    def from_dict(obj: dict) -> Self:
        dthte = DataTemplateHowToElement(
            table_name=obj["table_name"],
            column_name=obj["column_name"],
            condition_column=obj.get("condition_column", None),
            after=obj.get("after", None),
        )
        return dthte

    def to_dict(self) -> dict[str, Any]:
        result = {
            "table_name": self.table_name,
            "column_name": self.column_name,
            "condition_column": self.condition_column,
            "after": self.after,
        }
        result = {k: result[k] for k in result if result[k] is not None}
        return result

    def to_value(self, db_connector: DBConnector, condition_value: Any):
        condition_column = (self.condition_column if self.condition_column is not None else db_connector.get_index_column_name())
        req = f"""
            SELECT {self.column_name} FROM {self.table_name}
            WHERE {condition_column} = '{condition_value}'
        """
        data = db_connector.fetchall(req)
        logger.log("Debug", "to_value\n", data, "\n", req)
        if not data or data[0] is None or data[0][0] is None:
            return None
        data = data[0][0]
        if self.after is not None:
            foo = eval(f"lambda x: ({self.after})")
            data = foo(data)
        return data


class DataTemplateElement:
    def __init__(self, example: str, howto: list[DataTemplateHowToElement]):
        self.example = example
        self.howto = howto

    @staticmethod
    def from_dict_able(obj: dict) -> bool:
        return (isinstance(obj, dict) and "_DataTemplateElement_" in obj)

    def to_dict(self) -> dict[str, Any]:
        return {
            "_DataTemplateElement_": {
                "example": self.example,
                "howto": [howto_el.to_dict() for howto_el in self.howto],
            }
        }

    @staticmethod
    def from_dict(obj: dict) -> Self:
        obj = obj["_DataTemplateElement_"]
        dte = DataTemplateElement(
            example=obj["example"],
            howto=[DataTemplateHowToElement.from_dict(howto_el) for howto_el in obj["howto"]],
        )
        return dte

    def to_value(self, db_connector: DBConnector = None, ind = None) -> str:
        if db_connector is None:
            return self.example
        if ind is None:
            raise Exception("DataTemplateElement::to_value got ind=None")
        last_result = ind
        for howto_el in self.howto:
            data = howto_el.to_value(db_connector, last_result)
            last_result = data
        return str(last_result)



class DataTemplate:
    def __init__(self, data_template_json: dict):
        self.elements: list[tuple[Any, str]] = []
        self.data = data_template_json
        for root, key in self.iterate():
            if not DataTemplateElement.from_dict_able(root[key]):
                continue
            root[key] = DataTemplateElement.from_dict(root[key])
            self.elements.append((root, key))

    def iterate(self, data = None):
        if data is None:
            data = self.data
        if isinstance(data, dict) or isinstance(data, list):
            keys = data.keys() if isinstance(data, dict) else range(len(data))
            for k in keys:
                yield data, k
                for args in self.iterate(data[k]):
                    yield args

    def fill_template(self, db_connector: DBConnector) -> Any:
        ind = db_connector.get_last_index()
        for root, key in self.elements:
            root[key] = root[key].to_value(db_connector, ind)
        return ind

    @staticmethod
    def create_example_json() -> dict[str, Any]:
        example_data = {
            "@env": "EPGU",
            "CreateOrdersRequest": {
                "orders": {
                    "order": [{
                        "user": {
                            "userPersonalDoc": {
                                "PersonalDocType": "1",
                                "number": DataTemplateElement(
                                    example="1234567890",
                                    howto=[
                                        DataTemplateHowToElement(column_name="appl_number", table_name="fips_rutrademark"),
                                    ]
                                ).to_dict(),
                                "lastName": DataTemplateElement(
                                    example="Иванов",
                                    howto=[
                                        DataTemplateHowToElement(column_name="applicants", table_name="fips_rutrademark", after="x.split(' ')[0]"),
                                    ]
                                ).to_dict(),
                                "firstName": "Иван",
                                "middleName": "Иванович",
                                "citizenship": "1"
                            }
                        },
                        "senderInn": "1234567890",
                        "serviceTargetCode": "12345678901234567890",
                        "userSelectedRegion": "45000000",
                        "orderNumber": '31d4ec1a-43b3-4ade-bce8-eb3df9e6e940',
                        "requestDate": '2025-12-12T10:31:23.042643',
                        "OfficeInfo": {
                            "OfficeName": "МФЦ Центрального района",
                            "ApplicationAcceptance": "1"
                        },
                        "statusHistoryList": {
                            "statusHistory": [{
                                "status": "1",
                                "IsInformed": "false",
                                "statusDate": '2025-12-12T10:32:23.042643',
                            }]
                        }
                    }]
                }
            }
        }

        return example_data
