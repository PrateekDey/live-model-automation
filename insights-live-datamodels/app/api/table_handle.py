import requests

from app.api.sisense_endpoints import get_endpoint
from app.setup_structlog import get_logger

_logger = get_logger(__name__)


def get_recent_connections():
    _logger.info("Fetching the recent connection")
    endpoint, headers = get_endpoint('connections')
    response = requests.get(url=endpoint, headers=headers)
    return response.json()[-1]


def list_tables(conn_id: str, parameter: dict):
    raw_table_list = []
    _logger.info(f"List the schema based on schema {parameter['schema']}")
    endpoint, headers = get_endpoint('list_tables', conn_id)
    data = {
        "provider": parameter['provider'],
        "connectionData": {
            "connection": {
                "ApiVersion": 2,
                "Server": parameter["server"],
                "UserName": parameter["username"],
                "DefaultDatabase": parameter["defaultdatabase"],
                "EncryptConnection": True,
                "TrustServerCertificate": True,
                "AdditionalParameters": "",
                "Database": parameter["database"]
            }
        }
    }

    response = requests.post(url=endpoint, json=data, headers=headers)
    [raw_table_list.append(i) for i in response.json() if i.get("schemaName") == parameter['schema']]
    return raw_table_list


def table_schema_data(conn_oid: str, parameter: dict, table_name: str):
    _logger.info('Fetching details of the table based on connection', connection_id=conn_oid)
    endpoint, headers = get_endpoint('table_schema_details', conn_oid)
    data = {
        "provider": parameter['provider'],
        "connectionData": {
            "connection": {
                "ApiVersion": "2",
                "Server": parameter['server'],
                "UserName": parameter['username'],
                "DefaultDatabase": parameter['defaultdatabase'],
                "EncryptConnection": False,
                "AdditionalParameters": "",
                "Database": parameter['database']
            },
            "provider": parameter['provider'],
            "schema": parameter['schema'],
            "table": table_name
        }
    }

    response = requests.post(url=endpoint, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


def orient_columns(column_list: list):
    new_column_list = []
    for column in column_list:
        ex = {
            "id": column.get("columnName"),
            "name": column['columnName'],
            "type": column['dbType'],
            "size": column['size'],
            "precision": column['precision'],
            "scale": column['scale'],
            "hidden": False
        }
        new_column_list.append(ex)
    return new_column_list


def add_base_table(parameter: dict, table_name: str, table_oid: str, column_list: list):
    _logger.info(f"Adding table {table_name} to the dataset")
    endpoint, headers = get_endpoint('ecm')
    data = {
        "operationName": "addTableToDataset",
        "query": "mutation addTableToDataset($elasticubeOid: UUID!, $datasetOid: UUID!, $table: TableInput!) {\n  table: addTableToDataset(elasticubeOid: $elasticubeOid, datasetOid: $datasetOid, table: $table) {\n    oid\n    __typename\n  }\n}\n",
        "variables": {
            "elasticubeOid": parameter['datamodel_oid'],
            "datasetOid": parameter['dataset_oid'],
            "table": {
                "id": table_name,
                "name": table_name,
                "oid": table_oid,
                "hidden": False,
                "schemaName": parameter['schema'],
                "buildBehavior": {
                    "type": "sync"
                },
                "columns": column_list,
                "tupleTransformations": [

                ]
            }
        }
    }

    response = requests.post(url=endpoint, json=data, headers=headers)
    response.raise_for_status()
    return response.status_code
