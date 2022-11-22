from app.api.connect_password import password_details
from app.api.live_models import automate_cube_creation
import app


def main():
    tenant = input("Enter the tenant name: ")
    case = input("Enter the use case: ")
    env = input("Enter the environment (dev/ test/ prod) for schema: ")
    model_name = input("(Note: this will be added at the last of the datamodel name) \nEnter the model name: ")

    parameter = {
        "datamodel_name": f"{tenant}_{case}_{env}_{model_name}",
        "dataset_name": f"{tenant}_{case}_{env}_{model_name}_set",
        "provider": "RedShift",
    }

    parameter.update(password_details(tenant, case, env))
    automate_cube_creation(parameter)


main()