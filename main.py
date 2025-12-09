"""
# 1. Initialize XML generator
xml_gen = XMLGenerator("schemas.xsd")

# 2. Load your JSON data (from file or API)
with open('data.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 3. Convert to XML
xml_gen.json_to_xml_file(json_data, "output.xml")

# 4. Validate
result = xml_gen.validate_xml("output.xml")
if result['valid']:
    print("XML is valid!")
else:
    print("Validation errors:", result['errors'])
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import uuid
from typing import Dict, Any, Optional
import xmlschema
import os


class XMLGenerator:
    """Class for generating XML from JSON data with XSD schema validation"""
    
    def __init__(self, xsd_path: str = "schemas.xsd"):
        """
        Initialize XML generator with XSD schema
        
        Args:
            xsd_path: Path to XSD schema file
        """
        self.xsd_path = xsd_path
        self.schema = None
        
        # Load schema if file exists
        if os.path.exists(xsd_path):
            try:
                self.schema = xmlschema.XMLSchema(xsd_path)
            except Exception as e:
                print(f"Warning: Could not load XSD schema: {e}")
    
    def _create_element_with_ns(self, tag: str, text: str = None, 
                               attributes: Dict[str, str] = None) -> ET.Element:
        """
        Create XML element with namespace handling
        
        Args:
            tag: Element tag
            text: Element text content
            attributes: Element attributes
            
        Returns:
            XML element
        """
        # Define namespace
        ns = "http://epgu.gosuslugi.ru/elk/status/1.0.2"
        element = ET.Element(f"{{{ns}}}{tag}")
        
        if text is not None:
            element.text = str(text)
        
        if attributes:
            for key, value in attributes.items():
                element.set(key, str(value))
        
        return element
    
    def _dict_to_xml(self, parent: ET.Element, data: Dict[str, Any], 
                    is_root: bool = False):
        """
        Recursively convert dictionary to XML elements
        
        Args:
            parent: Parent XML element
            data: Dictionary data to convert
            is_root: Whether this is the root element
        """
        # Handle root element namespace
        if is_root:
            parent.set("xmlns", "http://epgu.gosuslugi.ru/elk/status/1.0.2")
        
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
    
    def json_to_xml_file(self, json_data: Dict[str, Any], 
                         output_file: str = "output.xml",
                         root_tag: str = "ElkOrderRequest") -> bool:
        """
        Convert JSON data to XML file
        
        Args:
            json_data: Dictionary containing JSON data
            output_file: Path to output XML file
            root_tag: Root tag name (ElkOrderRequest or ElkOrderResponse)
            
        Returns:
            True if successful, False otherwise
        """
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
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_pretty)
            
            print(f"XML file created successfully: {output_file}")
            return True
            
        except Exception as e:
            print(f"Error creating XML file: {e}")
            return False
    
    def _prettify_xml(self, xml_string: str) -> str:
        """
        Prettify XML string for better readability
        
        Args:
            xml_string: Raw XML string
            
        Returns:
            Prettified XML string
        """
        try:
            parsed = minidom.parseString(xml_string)
            return parsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
        except:
            # Fallback to simple formatting if minidom fails
            return xml_string
    
    def validate_xml(self, xml_file: str) -> Dict[str, Any]:
        """
        Validate XML file against XSD schema
        
        Args:
            xml_file: Path to XML file to validate
            
        Returns:
            Dictionary with validation results
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': []
        }
        
        if not self.schema:
            result['errors'].append("XSD schema not loaded")
            return result
        
        if not os.path.exists(xml_file):
            result['errors'].append(f"XML file not found: {xml_file}")
            return result
        
        try:
            # Validate against schema
            validation_result = self.schema.validate(xml_file)
            
            if validation_result is None:
                result['valid'] = True
                result['message'] = "XML is valid according to XSD schema"
            else:
                result['valid'] = False
                # Try to get more detailed error information
                try:
                    errors = list(self.schema.iter_errors(xml_file))
                    for error in errors:
                        result['errors'].append(str(error))
                except:
                    result['errors'].append("XML validation failed")
            
        except Exception as e:
            result['errors'].append(f"Validation error: {e}")
        
        return result
    
    def validate_xml_string(self, xml_string: str) -> Dict[str, Any]:
        """
        Validate XML string against XSD schema
        
        Args:
            xml_string: XML string to validate
            
        Returns:
            Dictionary with validation results
        """
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


# Example usage functions
def create_example_json() -> Dict[str, Any]:
    """
    Create example JSON data based on the XSD schema structure
    """
    current_time = datetime.now().isoformat()
    
    example_data = {
        "@env": "EPGU",  # Attribute
        "CreateOrdersRequest": {
            "orders": {
                "order": [{
                    "user": {
                        "userPersonalDoc": {
                            "PersonalDocType": "1",
                            "number": "1234567890",
                            "lastName": "Иванов",
                            "firstName": "Иван",
                            "middleName": "Иванович",
                            "citizenship": "1"
                        }
                    },
                    "senderInn": "1234567890",
                    "serviceTargetCode": "12345678901234567890",
                    "userSelectedRegion": "45000000",
                    "orderNumber": str(uuid.uuid4())[:36],
                    "requestDate": current_time,
                    "OfficeInfo": {
                        "OfficeName": "МФЦ Центрального района",
                        "ApplicationAcceptance": "1"
                    },
                    "statusHistoryList": {
                        "statusHistory": [{
                            "status": "1",
                            "IsInformed": False,
                            "statusDate": current_time
                        }]
                    }
                }]
            }
        }
    }
    
    return example_data


def main():
    """
    Main function demonstrating XML generation and validation
    """
    # Initialize XML generator
    xml_gen = XMLGenerator("schemas.xsd")
    
    # Create example JSON data
    example_json = create_example_json()
    print("Example JSON data created")
    
    # Convert JSON to XML file
    output_file = "generated_request.xml"
    success = True
    if not os.path.exists(output_file):
        success = xml_gen.json_to_xml_file(example_json, output_file)
    
    if success:
        # Validate the generated XML
        validation_result = xml_gen.validate_xml(output_file)
        
        print("\n" + "="*50)
        print("VALIDATION RESULTS:")
        print("="*50)
        
        if validation_result['valid']:
            print(f"✓ {validation_result['message']}")
        else:
            print("✗ XML validation failed!")
            print("\nErrors:")
            for error in validation_result['errors']:
                print(f"  - {error}")
    
    # Example of reading JSON from file and converting
    print("\n" + "="*50)
    print("USAGE EXAMPLE:")
    print("="*50)


if __name__ == "__main__":
    # Install required packages if not already installed
    try:
        import xmlschema
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(["pip", "install", "xmlschema"])
        import xmlschema
    
    main()
