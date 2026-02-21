import traceback
from typing import Any, Self

from src.db_connector import DBConnector
from src.logger import logger
from src.validate import validate_list_functions


class DataTemplateHowToElement:
    def __init__(self, table_name: str, column_name: str, condition_column: str = None, after: str = None, clause_after_when: str = None):
        self.table_name = table_name
        self.column_name = column_name
        self.condition_column = condition_column
        self.after = after
        self.clause_after_when = clause_after_when

    @staticmethod
    def from_dict(obj: dict) -> Self:
        dthte = DataTemplateHowToElement(
            table_name=obj["table_name"],
            column_name=obj["column_name"],
            condition_column=obj.get("condition_column", None),
            after=obj.get("after", None),
            clause_after_when=obj.get("clause_after_when", None),
        )
        return dthte

    def to_dict(self) -> dict[str, Any]:
        result = {
            "table_name": self.table_name,
            "column_name": self.column_name,
            "condition_column": self.condition_column,
            "after": self.after,
            "clause_after_when": self.clause_after_when,
        }
        result = {k: result[k] for k in result if result[k] is not None}
        return result

    def to_value(self, db_connector: DBConnector, condition_value: Any):
        condition_column = (self.condition_column if self.condition_column is not None else db_connector.get_index_column_name())
        req = f"""
            SELECT "{self.column_name}" FROM "{self.table_name}"
            WHERE "{condition_column}" = '{condition_value}' {self.clause_after_when if self.clause_after_when is not None else ''}
        """
        data = db_connector.fetchall(req)
        logger.log("Debug", "to_value\n", data, "\n", req)
        if not data or data[0] is None or data[0][0] is None:
            return None
        data = data[0][0]
        if self.after is not None:
            try:
                foo = eval(f"lambda x: ({self.after})")
                data = foo(data)
            except Exception:
                raise Exception(f"{data} could not be formatted using after={self.after}")
        return data


_validation_errors = []

def clear_validation_errors():
    global _validation_errors
    _validation_errors = []

def add_validation_error(msg):
    global _validation_errors
    _validation_errors.append(msg)

def get_validation_errors():
    return _validation_errors


class DataTemplateElement:
    def __init__(self, example: str, howto: list[DataTemplateHowToElement], after: str = None, validate: list[str] = None):
        self.example = example
        self.howto = howto
        self.after = after
        self.validate = validate if validate is not None else []

    @staticmethod
    def from_dict_able(obj: dict) -> bool:
        return (isinstance(obj, dict) and "_DataTemplateElement_" in obj)

    def to_dict(self) -> dict[str, Any]:
        return {
            "_DataTemplateElement_": {
                "example": self.example,
                "howto": [howto_el.to_dict() for howto_el in self.howto],
                "after": self.after,
                "validate": self.validate,
            }
        }

    @staticmethod
    def from_dict(obj: dict) -> Self:
        obj = obj["_DataTemplateElement_"]
        dte = DataTemplateElement(
            example=obj["example"],
            howto=[DataTemplateHowToElement.from_dict(howto_el) for howto_el in obj["howto"]],
            after=obj.get("after", None),
            validate=obj.get("validate", []),
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
        data = last_result
        if self.after is not None:
            try:
                foo = eval(f"lambda x: ({self.after})")
                data = foo(data)
            except Exception:
                raise Exception(f"{data} could not be formatted using after={self.after}")
        if not validate_list_functions(self.validate, data):
            msg = f"Validation failed for value '{data}' with rules {self.validate}"
            add_validation_error(msg)
            logger.log(msg)
        return str(data)


class ConditionalElement:
    def __init__(self, howto: list[DataTemplateHowToElement], result, **conditions):
        self.howto = howto
        self.result = result
        # Store exactly one condition type
        if 'condition_value_equal' in conditions:
            self.condition_value_equal = conditions['condition_value_equal']
        elif 'condition_values_in' in conditions:
            self.condition_values_in = conditions['condition_values_in']
        elif 'condition_values_not_in' in conditions:
            self.condition_values_not_in = conditions['condition_values_not_in']
        elif 'condition_value_empty' in conditions:
            self.condition_value_empty = conditions['condition_value_empty']
        else:
            raise ValueError("ConditionalElement must have one condition")

    @staticmethod
    def from_dict(obj: dict):
        """Create a ConditionalElement from a dict with marker '_ConditionalElement_'."""
        data = obj['_ConditionalElement_']
        # Convert howto list
        howto = [DataTemplateHowToElement.from_dict(h) for h in data['howto']]
        # Extract the single condition
        conditions = {}
        if 'condition_value_equal' in data:
            conditions['condition_value_equal'] = data['condition_value_equal']
        elif 'condition_values_in' in data:
            conditions['condition_values_in'] = data['condition_values_in']
        elif 'condition_values_not_in' in data:
            conditions['condition_values_not_in'] = data['condition_values_not_in']
        elif 'condition_value_empty' in data:
            conditions['condition_value_empty'] = data['condition_value_empty']
        # Recursively convert the result (it may contain nested special nodes)
        result = DataTemplate._convert_special_nodes(data['result'])
        return ConditionalElement(howto, result, **conditions)

    def to_dict(self) -> dict:
        """Convert to a JSON‑serializable dict."""
        result_dict = {
            'howto': [h.to_dict() for h in self.howto],
        }
        # Add the condition that is present
        if hasattr(self, 'condition_value_equal'):
            result_dict['condition_value_equal'] = self.condition_value_equal
        elif hasattr(self, 'condition_values_in'):
            result_dict['condition_values_in'] = self.condition_values_in
        elif hasattr(self, 'condition_values_not_in'):
            result_dict['condition_values_not_in'] = self.condition_values_not_in
        elif hasattr(self, 'condition_value_empty'):
            result_dict['condition_value_empty'] = self.condition_value_empty

        # Convert result (it might be a special node or a plain dict)
        if isinstance(self.result, (DataTemplateElement, ConditionalElement)):
            result_dict['result'] = self.result.to_dict()
        else:
            # It's a plain dict/list – but may contain special nodes inside,
            # so we recursively convert it as well.
            result_dict['result'] = DataTemplate._convert_special_nodes(self.result, to_dict=True)
        return {'_ConditionalElement_': result_dict}

    def to_value(self, db_connector: DBConnector, ind: Any):
        """Evaluate the howto chain, check condition, and return the result (or None)."""
        # Walk the howto chain starting from ind
        last = ind
        for howto_el in self.howto:
            val = howto_el.to_value(db_connector, last)
            last = val
        condition_value = last

        # Determine if condition is met
        condition_met = False
        if hasattr(self, 'condition_value_equal'):
            condition_met = (condition_value == self.condition_value_equal)
        elif hasattr(self, 'condition_values_in'):
            condition_met = (condition_value in self.condition_values_in)
        elif hasattr(self, 'condition_values_not_in'):
            condition_met = (condition_value not in self.condition_values_not_in)
        elif hasattr(self, 'condition_value_empty'):
            # condition_value_empty = True  -> we want the value to be empty
            # condition_value_empty = False -> we want the value to be non‑empty
            is_empty = (condition_value is None or condition_value == '')
            condition_met = (is_empty == self.condition_value_empty)

        if condition_met:
            # Return the result as‑is – it will be further processed by the recursive fill
            return self.result
        else:
            return None   # signal that this branch should be omitted


class DataTemplate:
    def __init__(self, data_template_json: dict):
        # Recursively convert all special markers to objects
        self.data = self._convert_special_nodes(data_template_json)

    @staticmethod
    def _convert_special_nodes(node, to_dict=False):
        """
        Recursively traverse a structure (dict/list) and replace any dict
        containing a marker with the corresponding object.
        If to_dict=True, instead of creating objects, we call to_dict() on them
        (used when serializing a ConditionalElement's result).
        """
        if isinstance(node, dict):
            # Check for markers
            if '_DataTemplateElement_' in node:
                if to_dict:
                    return node
                return DataTemplateElement.from_dict(node)
            if '_ConditionalElement_' in node:
                if to_dict:
                    return node
                return ConditionalElement.from_dict(node)

            # Regular dict – recurse into values
            new_dict = {}
            for k, v in node.items():
                new_dict[k] = DataTemplate._convert_special_nodes(v, to_dict)
            return new_dict

        elif isinstance(node, list):
            # Recurse into each item
            return [DataTemplate._convert_special_nodes(item, to_dict) for item in node]

        else:
            # Base type (str, int, etc.) – return unchanged
            return node

    def _fill_recursive(self, node, db_connector, ind):
        """
        Recursively walk the structure and evaluate any special nodes.
        Returns the processed node (which may be a dict, list, string, or None).
        """
        if isinstance(node, dict):
            new_dict = {}
            for key, value in node.items():
                processed = self._fill_recursive(value, db_connector, ind)
                if processed is not None:   # omit keys that evaluate to None
                    new_dict[key] = processed
            return new_dict

        elif isinstance(node, list):
            new_list = []
            for item in node:
                processed = self._fill_recursive(item, db_connector, ind)
                if processed is not None:   # optionally remove None from lists
                    new_list.append(processed)
            return new_list

        elif isinstance(node, DataTemplateElement):
            # Leaf element: compute the string value
            return node.to_value(db_connector, ind)

        elif isinstance(node, ConditionalElement):
            # Branch: evaluate condition, get result, then recursively process that result
            result = node.to_value(db_connector, ind)
            if result is None:
                return None
            # The result may contain more special nodes – process them
            return self._fill_recursive(result, db_connector, ind)

        else:
            # Plain value (str, int, etc.)
            return node

    def fill_template(self, db_connector: DBConnector, ind: Any) -> Any:
        self.data = self._fill_recursive(self.data, db_connector, ind)
        return ind

    @staticmethod
    def create_example_json() -> dict[str, Any]:
        example_data = {
            "@env": "SVCDEV",  # SVCDEV/EPGU/ERUL
            "CreateOrdersRequest": {
                "orders": {
                    "order": [{
                        "user": ConditionalElement(
                            howto=[
                                DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                DataTemplateHowToElement(column_name="contact_type", table_name="fips_contact", condition_column="contact_uid", after="str(x)"),
                            ],
                            condition_value_equal="0",
                            result={
                                "userDocSnils": ConditionalElement(
                                    howto=[
                                        DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                        DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                        DataTemplateHowToElement(column_name="snils", table_name="fips_contact", condition_column="contact_uid", after="''.join(c for c in str(x) if c in '1234567890')"),
                                    ],
                                    condition_value_empty=False,
                                    result={
                                        "snils": DataTemplateElement(
                                            example="12345678900",
                                            howto=[
                                                DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                                DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                                DataTemplateHowToElement(column_name="snils", table_name="fips_contact", condition_column="contact_uid", after="''.join(c for c in str(x) if c in '1234567890')"),
                                            ],
                                            validate=["snils"],
                                        ).to_dict(),
                                        "lastName": DataTemplateElement(
                                            example="Иванов",
                                            howto=[
                                                DataTemplateHowToElement(column_name="applicants", table_name="fips_rutrademark", after="x.strip().split(' ')[0]"),
                                            ]
                                        ).to_dict(),
                                        "firstName": DataTemplateElement(
                                            example="Иван",
                                            howto=[
                                                DataTemplateHowToElement(column_name="applicants", table_name="fips_rutrademark", after="x.strip().split(' ')[1]"),
                                            ]
                                        ).to_dict(),
                                        "middleName": DataTemplateElement(
                                            example="Иванович",
                                            howto=[
                                                DataTemplateHowToElement(column_name="applicants", table_name="fips_rutrademark", after="(x.strip().split(' ')+[None,None,None])[2]"),
                                            ],
                                            after="'' if x is None else x"
                                        ).to_dict(),
                                        "citizenship": "0",
                                    },
                                ).to_dict(),
                                "userDocInn": ConditionalElement(
                                    howto=[
                                        DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                        DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                        DataTemplateHowToElement(column_name="snils", table_name="fips_contact", condition_column="contact_uid", after="''.join(c for c in str(x) if c in '1234567890')"),
                                    ],
                                    condition_value_empty=True,
                                    result={
                                        "INN": DataTemplateElement(
                                            example="123456789000",
                                            howto=[
                                                DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                                DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                                DataTemplateHowToElement(column_name="inn", table_name="fips_contact", condition_column="contact_uid"),
                                            ],
                                            validate=["inn_fl"],
                                        ).to_dict(),
                                        "lastName": DataTemplateElement(
                                            example="Иванов",
                                            howto=[
                                                DataTemplateHowToElement(column_name="applicants", table_name="fips_rutrademark", after="x.strip().split(' ')[0]"),
                                            ]
                                        ).to_dict(),
                                        "firstName": DataTemplateElement(
                                            example="Иван",
                                            howto=[
                                                DataTemplateHowToElement(column_name="applicants", table_name="fips_rutrademark", after="x.strip().split(' ')[1]"),
                                            ]
                                        ).to_dict(),
                                        "middleName": DataTemplateElement(
                                            example="Иванович",
                                            howto=[
                                                DataTemplateHowToElement(column_name="applicants", table_name="fips_rutrademark", after="(x.strip().split(' ')+[None,None,None])[2]"),
                                            ],
                                            after="'' if x is None else x"
                                        ).to_dict(),
                                        "citizenship": "0",
                                    },
                                ).to_dict(),
                            },
                        ).to_dict(),
                        "organization": ConditionalElement(
                            howto=[
                                DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                DataTemplateHowToElement(column_name="contact_type", table_name="fips_contact", condition_column="contact_uid", after="str(x)"),
                            ],
                            condition_values_in=("1", "2"),
                            result={
                                "ogrn_inn_IP": ConditionalElement(
                                    howto=[
                                        DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                        DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                        DataTemplateHowToElement(column_name="contact_type", table_name="fips_contact", condition_column="contact_uid", after="str(x)"),
                                    ],
                                    condition_value_equal="2",
                                    result={
                                        "ogrn": DataTemplateElement(
                                            example="1234567890000",
                                            howto=[
                                                DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                                DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                                DataTemplateHowToElement(column_name="ogrn", table_name="fips_contact", condition_column="contact_uid"),
                                            ],
                                            validate=["ogrn_ip"],
                                        ).to_dict(),
                                        "inn": DataTemplateElement(
                                            example="123456789000",
                                            howto=[
                                                DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                                DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                                DataTemplateHowToElement(column_name="inn", table_name="fips_contact", condition_column="contact_uid"),
                                            ],
                                            validate=["inn_ip"],
                                        ).to_dict(),
                                        "lastName": DataTemplateElement(
                                            example="Иванов",
                                            howto=[
                                                DataTemplateHowToElement(column_name="applicants", table_name="fips_rutrademark", after="(x.strip()[3:] if x.strip().lower().startswith('ип ') else (x.strip()[31:] if x.strip().lower().startswith('индивидуальный предприниматель ') else x.strip())).split(' ')[0]"),
                                            ]
                                        ).to_dict(),
                                        "firstName": DataTemplateElement(
                                            example="Иван",
                                            howto=[
                                                DataTemplateHowToElement(column_name="applicants", table_name="fips_rutrademark", after="(x.strip()[3:] if x.strip().lower().startswith('ип ') else (x.strip()[31:] if x.strip().lower().startswith('индивидуальный предприниматель ') else x.strip())).split(' ')[1]"),
                                            ]
                                        ).to_dict(),
                                        "middleName": DataTemplateElement(
                                            example="Иванович",
                                            howto=[
                                                DataTemplateHowToElement(column_name="applicants", table_name="fips_rutrademark", after="((x.strip()[3:] if x.strip().lower().startswith('ип ') else (x.strip()[31:] if x.strip().lower().startswith('индивидуальный предприниматель ') else x.strip())).split(' ')+[None,None,None])[2]"),
                                            ],
                                            after="'' if x is None else x"
                                        ).to_dict(),
                                    },
                                ).to_dict(),
                                "ogrn_inn_UL": ConditionalElement(
                                    howto=[
                                        DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                        DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                        DataTemplateHowToElement(column_name="contact_type", table_name="fips_contact", condition_column="contact_uid", after="str(x)"),
                                    ],
                                    condition_value_equal="1",
                                    result={
                                        "ogrn": ConditionalElement(
                                            howto=[
                                                DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                                DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                                DataTemplateHowToElement(column_name="ogrn", table_name="fips_contact", condition_column="contact_uid", after="''.join(c for c in str(x) if c in '1234567890')"),
                                            ],
                                            condition_value_empty=False,
                                            result=DataTemplateElement(
                                                example="1234567890000",
                                                howto=[
                                                    DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                                    DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                                    DataTemplateHowToElement(column_name="ogrn", table_name="fips_contact", condition_column="contact_uid"),
                                                ],
                                                validate=["ogrn_ul"],
                                            ).to_dict(),
                                        ).to_dict(),
                                        "inn_kpp": ConditionalElement(
                                            howto=[
                                                DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                                DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                                DataTemplateHowToElement(column_name="ogrn", table_name="fips_contact", condition_column="contact_uid", after="''.join(c for c in str(x) if c in '1234567890')"),
                                            ],
                                            condition_value_empty=True,
                                            result={
                                                "inn": DataTemplateElement(
                                                    example="1234567890",
                                                    howto=[
                                                        DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                                        DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                                        DataTemplateHowToElement(column_name="inn", table_name="fips_contact", condition_column="contact_uid"),
                                                    ],
                                                    validate=["inn_ul"],
                                                ).to_dict(),
                                                "kpp": DataTemplateElement(
                                                    example="123456789",
                                                    howto=[
                                                        DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                                        DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                                        DataTemplateHowToElement(column_name="customer_number", table_name="fips_contact", condition_column="contact_uid"),
                                                    ],
                                                    validate=["kpp"],
                                                ).to_dict(),
                                            },
                                        ).to_dict(),
                                    },
                                ).to_dict(),
                            },
                        ).to_dict(),
                        "DEBUG_contact_type": ConditionalElement(
                            howto=[
                                DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                DataTemplateHowToElement(column_name="contact_type", table_name="fips_contact", condition_column="contact_uid", after="str(x)"),
                            ],
                            condition_values_not_in=("0", "1", "2"),
                            result={
                                "contact_type": DataTemplateElement(
                                    example="1",
                                    howto=[
                                        DataTemplateHowToElement(column_name="rutmk_uid", table_name="fips_rutrademark"),
                                        DataTemplateHowToElement(column_name="contact_uid", table_name="fips_rutmkapplicant", condition_column="rutmk_uid"),
                                        DataTemplateHowToElement(column_name="contact_type", table_name="fips_contact", condition_column="contact_uid", after="str(x)"),
                                    ],
                                ).to_dict(),
                            },
                        ).to_dict(),
                        "senderKpp": "773001001",
                        "senderInn": "7730176088",
                        "serviceTargetCode": "60012726",
                        "userSelectedRegion": "00000000",
                        "orderNumber": DataTemplateElement(
                            example="2025933465",
                            howto=[
                                DataTemplateHowToElement(column_name="appl_number", table_name="fips_rutrademark"),
                            ]
                        ).to_dict(),
                        "requestDate": DataTemplateElement(
                            example="2025-12-12T10:31:23.042643",
                            howto=[
                                DataTemplateHowToElement(column_name="appl_receiving_date", table_name="fips_rutrademark", after="str(x) + 'T12:00:00.000000'"),
                            ]
                        ).to_dict(),
                        "OfficeInfo": {
                            "OfficeName": "Федеральная служба по интеллектуальной собственности",
                            "OfficeAdress": "121059, г. Москва, наб Бережковская, д. 30, к. 1",
                            "OfficeFrguCode": "0000000075",
                            "ApplicationAcceptance": "-1",
                        },
                        "statusHistoryList": {
                            "statusHistory": [{
                                "status": DataTemplateElement(
                                    example="TODOTODOTODO",
                                    howto=[
                                        DataTemplateHowToElement(column_name="object_uid", table_name="fips_rutrademark"),
                                        DataTemplateHowToElement(column_name="TextValue", table_name="SearchAttributes", condition_column="ParentNumber", clause_after_when="AND \"Name\" = 'OC.OCCode'"),
                                    ],
                                    after="str(x)",
                                ).to_dict(),
                                "statusDate": DataTemplateElement(
                                    example="2025-12-12T10:32:23.042643",
                                    howto=[
                                        DataTemplateHowToElement(column_name="object_uid", table_name="fips_rutrademark"),
                                        DataTemplateHowToElement(column_name="TextValue", table_name="SearchAttributes", condition_column="ParentNumber", clause_after_when="AND \"Name\" = 'OC.OCDate'"),
                                    ],
                                    after="str(x) + 'T12:00:00.000000'",
                                ).to_dict(),
                                "MessageType": "<#if text?hasContent>Направлена исходящая корреспонденция по форме SearchAttributes.OCCode ${(text)!}</#if>",
                            }]
                        },
                    }]
                }
            }
        }

        return example_data
