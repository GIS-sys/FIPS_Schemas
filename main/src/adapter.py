import psycopg2
import requests
from sshtunnel import SSHTunnelForwarder
import uuid

from src.config import loaded_config


def send_xml_path(xml_path: str) -> requests.models.Response:
    with open(xml_path, "r", encoding="utf-8") as f:
        xml_content = f.read()
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

    with SSHTunnelForwarder(
        (loaded_config.proxy_ip, 22),
        ssh_username=loaded_config.proxy_ssh_user,
        ssh_password=loaded_config.proxy_ssh_password,
        remote_bind_address=(loaded_config.api_ip, 22),
    ) as jump_tunnel:
        with SSHTunnelForwarder(
            ('localhost', jump_tunnel.local_bind_port),
            ssh_username=loaded_config.api_ssh_user,
            ssh_password=loaded_config.api_ssh_password,
            remote_bind_address=(loaded_config.api_ip, loaded_config.api_port),
            local_bind_address=('localhost', loaded_config.api_bind_port),
        ) as tunnel:
            response = requests.post(
                f"http://localhost:{loaded_config.api_bind_port}/requests",
                headers={
                    "of": "epgu_exchange",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            return response


def execute_psql(query: str) -> list:
    with SSHTunnelForwarder(
        (loaded_config.proxy_ip, 22),  # jump host
        ssh_username=loaded_config.proxy_user,
        ssh_password=loaded_config.proxy_password,
        remote_bind_address=(loaded_config.db_adapter_ip, 22),  # next hop handled below
    ) as tunnel:
        with SSHTunnelForwarder(
            ('localhost', tunnel.local_bind_port),
            ssh_username=loaded_config.db_adapter_user,
            ssh_password=loaded_config.db_adapter_password,
            remote_bind_address=('localhost', loaded_config.db_adapter_port),
        ) as db_tunnel:
            with psycopg2.connect(
                host='localhost',
                port=db_tunnel.local_bind_port,
                user=loaded_config.db_adapter_user,
                password=loaded_config.db_adapter_password,
                database=loaded_config.db_adapter_dbname
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall()


if __name__ == "__main__":
    ROOT = "C:\PythonPrograms\FIPS_Schemas-separate_history\main\data"
    filename = "e6da7e65-46f9-375d-a9fc-76b673976d3a.df10cb71-2768-4154-df5d-08ddb7be29ce.xml"

    response = send_xml_path(f"{ROOT}\{filename}")
    print(response.status_code, response.text)

    if response.status_code // 100 == 2:
        result = execute_psql(f"SELECT id FROM core.delivery_log WHERE smev_message LIKE '%38117939404%' ORDER BY created_at DESC;")
        print(result[0])
        print(len(result), result)
