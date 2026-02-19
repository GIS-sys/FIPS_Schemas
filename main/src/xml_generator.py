import os
from typing import Any
from xml.dom import minidom
import xml.etree.ElementTree as ET
import xmlschema


class XMLGenerator:
    def __init__(self, xsd_path: str = "schemas.xsd"):
        self.xsd_path = xsd_path
        self.schema = None

        if os.path.exists(xsd_path):
            try:
                self.schema = xmlschema.XMLSchema(xsd_path)
            except Exception as e:
                raise Exception(f"Could not load XSD schema")

    def _create_element_with_ns(self, tag: str, text: str = None,
                               attributes: dict[str, str] = None) -> ET.Element:
        ns = "http://epgu.gosuslugi.ru/elk/status/1.0.2"
        element = ET.Element(f"{{{ns}}}{tag}")

        if text is not None:
            element.text = str(text)

        if attributes:
            for key, value in attributes.items():
                element.set(key, str(value))

        return element

    def _dict_to_xml(self, parent: ET.Element, data: dict[str, Any],
                    is_root: bool = False):
        # if is_root:
        #     parent.set("xmlns", "http://epgu.gosuslugi.ru/elk/status/1.0.2")

        for key, value in data.items():
            if key.startswith('@'):  # Attribute
                attr_name = key[1:]
                parent.set(attr_name, str(value))
            elif key == '#text':  # Text content
                parent.text = str(value)
            elif isinstance(value, dict):
                # Create child element and process nested dict
                child = self._create_element_with_ns(key)
                self._dict_to_xml(child, value)
                parent.append(child)
            elif isinstance(value, list):
                # Handle lists - create multiple elements with same tag
                for item in value:
                    if isinstance(item, dict):
                        child = self._create_element_with_ns(key)
                        self._dict_to_xml(child, item)
                        parent.append(child)
                    else:
                        child = self._create_element_with_ns(key, str(item))
                        parent.append(child)
            else:
                # Simple element with text content
                child = self._create_element_with_ns(key, str(value))
                parent.append(child)

    def json_to_xml(self, json_data: dict[str, Any],
                         root_tag: str = "ElkOrderRequest") -> str:
        try:
            # Create root element
            root = self._create_element_with_ns(root_tag)

            # Convert dictionary to XML
            self._dict_to_xml(root, json_data, is_root=True)

            # Create XML tree
            tree = ET.ElementTree(root)

            # Format XML for better readability
            xml_str = ET.tostring(root, encoding='unicode')
            xml_pretty = self._prettify_xml(xml_str)

            return xml_pretty

        except Exception as e:
            raise Exception(f"Error creating XML file")

    def _prettify_xml(self, xml_string: str) -> str:
        try:
            parsed = minidom.parseString(xml_string)
            return parsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
        except:
            # Fallback to simple formatting if minidom fails
            return xml_string

    def validate_xml(self, xml_str: str) -> dict[str, Any]:
        result = {
            'valid': False,
            'errors': [],
            'warnings': []
        }

        if not self.schema:
            result['errors'].append("XSD schema not loaded")
            return result
        try:
            # Validate against schema
            validation_result = self.schema.validate(xml_str)

            if validation_result is None:
                result['valid'] = True
                result['message'] = "XML is valid according to XSD schema"
            else:
                result['valid'] = False
                # Try to get more detailed error information
                try:
                    errors = list(self.schema.iter_errors(xml_str))
                    for error in errors:
                        result['errors'].append(str(error))
                except:
                    result['errors'].append("XML validation failed")

        except Exception as e:
            result['errors'].append(f"Validation error: {e}")

        return result

    def validate_xml_string(self, xml_string: str) -> dict[str, Any]:
        result = {
            'valid': False,
            'errors': [],
            'warnings': []
        }

        if not self.schema:
            result['errors'].append("XSD schema not loaded")
            return result

        try:
            # Parse XML string
            root = ET.fromstring(xml_string)

            # Convert back to string for validation
            xml_bytes = ET.tostring(root, encoding='utf-8')

            # Validate
            validation_result = self.schema.validate(xml_bytes)

            if validation_result is True:
                result['valid'] = True
                result['message'] = "XML is valid according to XSD schema"
            else:
                result['valid'] = False
                # Try to get more detailed error information
                try:
                    errors = list(self.schema.iter_errors(xml_bytes))
                    for error in errors:
                        result['errors'].append(str(error))
                except:
                    result['errors'].append("XML validation failed")

        except ET.ParseError as e:
            result['errors'].append(f"XML parsing error: {e}")
        except Exception as e:
            result['errors'].append(f"Validation error: {e}")

        return result
