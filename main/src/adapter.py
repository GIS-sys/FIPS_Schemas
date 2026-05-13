import psycopg2
import re
import requests
from sshtunnel import SSHTunnelForwarder
import uuid
import xml.etree.ElementTree as ET

from src.config import loaded_config
from src.logger import logger
from src.tunnel_manager import SingleThreadedTunnelManager


def send_xml_path(xml_path: str) -> requests.models.Response:
    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()
    xml_content = re.sub(r'>\s+<', '><', xml_content).replace("\n", "")
    return send_xml_content(xml_content)


def send_xml_content(xml_content: str) -> requests.models.Response:
    payload = {
        "to": "pmvz",
        "data": {
            "meta": {
                "smevMessageId": str(uuid.uuid4()),
                "adapterSmevRequestId": str(uuid.uuid4()),
            },
            "files": None,
            "xmlContent": xml_content,
        },
        "callback": "",
        "type": "request_to_smev",
    }
    logger.log(f"Sending XML {payload}")

    with SingleThreadedTunnelManager.instance().api_connection():
        response = requests.post(
            f"http://localhost:{loaded_config.api_bind_port}/requests",
            headers={"of": "epgu_exchange", "Content-Type": "application/json"},
            json=payload,
        )
        return response


def execute_psql(query: str) -> list:
    with SingleThreadedTunnelManager.instance().adapter_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def parse_adapter_response(message_content: str) -> tuple[dict, str]:
    # Attempt to parse the XML response content
    try:
        if not message_content:
            return None, "Message not found"
        # Parse XML string
        root = ET.fromstring(message_content)
        root = root.find('.//{*}SenderProvidedResponseData')
        if root.find('.//{*}AsyncProcessingStatus'):
            el = root.find('.//{*}AsyncProcessingStatus').find('.//{*}SmevFault')
            parsed_data = {
                'type': 'SmevFault',
                'code': el.find('.//{*}Code').text,
                'description': el.find('.//{*}Description').text,
                'validation_error': [x.text for x in el.findall('.//{*}ValidationError')]
            }
            return parsed_data, "SMEV error"
        if root.find('.//{*}CreateOrdersResponse'):
            el = root.find('.//{*}CreateOrdersResponse')
            parsed_data = {
                'type': 'CreateOrdersResponse',
                'code': el.find('.//{*}code').text,
                'message': el.find('.//{*}message').text,
                'orders': [
                    {
                        'orderNumber': x.find('.//{*}order').find('.//{*}orderNumber').text,
                        'status': x.find('.//{*}order').find('.//{*}status').text,
                        'message': x.find('.//{*}order').find('.//{*}message').text,
                        'elkOrderNumber': (x.find('.//{*}order').find('.//{*}elkOrderNumber').text if x.find('.//{*}order').find('.//{*}elkOrderNumber') is not None else None)
                    }
                for x in el.findall('.//{*}orders')]
            }
            if all([x['status'] == '0' for x in parsed_data['orders']]):
                parse_error = None
            else:
                parse_error = "CreateOrdersResponse error"
            return parsed_data, parse_error
        if root.find('.//{*}UpdateOrdersResponse'):
            el = root.find('.//{*}UpdateOrdersResponse')
            parsed_data = {
                'type': 'UpdateOrdersResponse',
                'code': el.find('.//{*}code').text,
                'message': el.find('.//{*}message').text,
                'orders': [
                    {
                        'elkOrderNumber': x.find('.//{*}order').find('.//{*}elkOrderNumber').text,
                        'orderNumber': x.find('.//{*}order').find('.//{*}orderNumber').text,
                        'status': x.find('.//{*}order').find('.//{*}status').text,
                        'message': x.find('.//{*}order').find('.//{*}message').text,
                    }
                for x in el.findall('.//{*}orders')]
            }
            return parsed_data, None
        return None, "Unexpected parsing format"
    except ET.ParseError as e:
        return None, f"XML parse error: {e}"
    except Exception as e:
        return None, f"Unexpected parsing error: {e}"


if __name__ == "__main__":
    ROOT = "C:\\PythonPrograms\\backups\\FIPS_Schemas-separate_history\\main\\data"
    filename = "e6da7e65-46f9-375d-a9fc-76b673976d3a.df10cb71-2768-4154-df5d-08ddb7be29ce.xml"

    response = send_xml_path(f"{ROOT}\\{filename}")
    print(response.status_code, response.text)

    if response.status_code // 100 == 2:
        result = execute_psql(f"SELECT id FROM core.delivery_log WHERE smev_message LIKE '%38117939404%' ORDER BY created_at DESC;")
        print(result[0])
        print(len(result), result)
