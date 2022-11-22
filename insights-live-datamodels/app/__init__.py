import os


selection = {
        "prod": {
            "us": ['us-east-1', "https://insights.us.anls.syncroncloud.com"],
            "eu": ['eu-west-1', "https://insights.eu.anls.syncroncloud.com"],
            "ap": ['ap-northeast-1', "https://insights.ap.anls.syncroncloud.com"]
        },

        "stage": {
            "us": ['us-east-1', "https://insights.us.anls.syncroncloud.io"],
            "eu": ['eu-west-1', "https://insights.eu.anls.syncroncloud.io"],
            "ap": ['ap-northeast-1', "https://insights.ap.anls.syncroncloud.io"]
        },

        "dev": {
            "us": ['us-east-1', "https://insights.us.anls.syncroncloud.team"],
            "eu": ['eu-west-1', "https://insights.eu.anls.syncroncloud.team"],
        },

        "demo": {
            "us": ['us-east-1', "https://insights-demo.us.anls.syncroncloud.team"]
        },

        "test": {
            "us": ['us-east-1', "https://insights-test.us.anls.syncroncloud.team"]
        }
    }

env = input("Enter the environment (prod/ stage/ dev/ demo/ test): ")
region = input("Enter the region (us/ eu/ ap): ")

temp_region, temp_hostname = selection[env][region]

hostname = os.getenv('HOSTNAME', temp_hostname)
aws_region = os.getenv('AWS_REGION', temp_region)
prefix = os.getenv('PREFIX', 'insights')
token_expiry = os.getenv('TOKEN_EXPIRY', 15)
pid = os.getenv('PID', 1928)
api_key = os.getenv('API_KEY', 'd5e6b79384f3ca278eb2cd34a596f352')
password_url = os.getenv('PASSWORD_URL', "https://passwords.syncron.team")
port_num = os.getenv('PORT_NUMBER', '5439')