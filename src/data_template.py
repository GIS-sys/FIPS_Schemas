from typing import Any, Self

from src.db_connector import DBConnector


class DataTemplateElement:
    def __init__(self, example: str, howto: list[str]):
        self.example = example
        self.howto = howto

    @staticmethod
    def from_dict_able(obj: dict) -> bool:
        return (isinstance(obj, dict) and "_DataTemplateElement_" in obj)

    def to_dict(self) -> dict[str, Any]:
        return {
            "_DataTemplateElement_": {
                "example": self.example,
                "howto": self.howto
            }
        }

    @staticmethod
    def from_dict(obj: dict) -> Self:
        obj = obj["_DataTemplateElement_"]
        dte = DataTemplateElement(obj["example"], obj["howto"])
        return dte

    def to_value(self, db_connector: DBConnector = None, ind = None) -> str:
        if db_connector is None:
            return self.example
        if ind is None:
            raise Exception("DataTemplateElement::to_value got ind=None")
        # TODO
        data = db_connector.fetchall(
            f"""
                SELECT {self.howto[0]} FROM {self.howto[1]}
                WHERE {db_connector.LAST_INDEX.column()} = {ind}
            """
        )
        return str(data)


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

    def fill_template(self, db_connector: DBConnector) -> dict:
        # TODO
        data = db_connector.fetchall(
            f"""
                SELECT {db_connector.LAST_INDEX.column()} FROM fips_rutrademark
                WHERE {db_connector.LAST_INDEX.where()}
                ORDER BY appl_receiving_date LIMIT 1
            """
        )
        print(data)
        ind = data[0][0]
        for root, key in self.elements:
            root[key] = root[key].to_value(db_connector, ind)

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
                                "number": "1234567890",
                                "lastName": DataTemplateElement(
                                    example="Иванов",
                                    howto=[
                                        "applicants",
                                        "fips_rutrademark"
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
                                "IsInformed": False,
                                "statusDate": '2025-12-12T10:32:23.042643',
                            }]
                        }
                    }]
                }
            }
        }

        return example_data
