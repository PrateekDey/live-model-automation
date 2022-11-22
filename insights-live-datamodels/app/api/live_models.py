import requests
import app.api.table_handle as table_handle

from app.api.sisense_endpoints import get_endpoint
from app.setup_structlog import get_logger

_logger = get_logger(__name__)


def create_live_cube(parameter: dict):
    _logger.info('Creating live cube on LocalHost', Live_cube=parameter['datamodel_name'])
    endpoint, headers = get_endpoint('create_live_cube')
    data = {
        "title": parameter['datamodel_name'],
        "type": "live"
    }
    response = requests.post(url=endpoint, json=data, headers=headers)
    response.raise_for_status()
    _logger.info('Successfully created live cube on LocalHost')
    return response.json()["oid"]


def create_live_dataset(parameter: dict):
    _logger.info('Creating datasets for Live cube', Live_oid=parameter['datamodel_oid'])
    endpoint, headers = get_endpoint('create_live_dataset', parameter['datamodel_oid'])
    data = {
        "name": parameter["dataset_name"],
        "type": "live",
        "connection": {
            "provider": parameter["provider"],
            "parameters": {
                "ApiVersion": "2",
                "Server": parameter["server"],
                "UserName": parameter["username"],
                "Password": parameter["password"],
                "DefaultDatabase": parameter["defaultdatabase"],
                "EncryptConnection": "true",
                "TrustServerCertificate": "true",
                "AdditionalParameters": "",
                "Database": parameter["database"]
            },
            "schema": parameter["schema"],
            "timeout": 60000,
            "refreshRate": 30000,
            "resultLimit": 5000,
            "uiParams": {},
            "globalTableConfigOptions": None
        }
    }
    response = requests.post(url=endpoint, json=data, headers=headers)
    response.raise_for_status()
    _logger.info(f"Successfully added dataset to the datamodel {parameter['datamodel_name']}")
    return response.json()['oid']


def add_table(parameter):
    conn_oid = table_handle.get_recent_connections().get('oid')
    table_list = []
    raw_table_list = table_handle.list_tables(conn_oid, parameter)
    for raw_table in raw_table_list:
        table_list.append(raw_table.get('tableName'))

    [print(table) for table in table_list]
    table_list = list(map(str.strip, (input("\nChoose the table: ").split(','))))

    for table in table_list:
        table_schema_details = table_handle.table_schema_data(conn_oid, parameter, table)
        column_list = table_handle.orient_columns(table_schema_details.get('columns'))
        table_oid = table_schema_details.get('oid')

        table_handle.add_base_table(parameter, table, table_oid, column_list)


def publish_model(parameter: dict):
    _logger.info(f"Publishing the Model {parameter['datamodel_name']}")
    endpoint, headers = get_endpoint('ecm')
    data = {
        "query": "mutation publishElasticube($elasticubeOid: UUID!) {\n  publishElasticube(elasticubeOid: $elasticubeOid)\n}\n",
        "variables": {
            "elasticubeOid": parameter['datamodel_oid']
        },
        "operationName": "publishElasticube"
    }
    response = requests.post(url=endpoint, json=data, headers=headers)
    response.raise_for_status()
    return response.status_code


def automate_cube_creation(parameter: dict):
    _logger.info("Automated Creation based on the parameters")
    parameter['datamodel_oid'] = create_live_cube(parameter)
    parameter['dataset_oid'] = create_live_dataset(parameter)
    add_table(parameter)
    publish_model(parameter)
