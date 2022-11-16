from app.api.connect_password import password_details
from app.api.live_models import automate_cube_creation


def main():
    tenant = input("Enter the tenant name: ")
    case = input("Enter the use case: ")
    env = input("Enter the environment (dev/ test/ stage/ prod): ")
    model_name = input("(Note: this will be added at the last of the datamodel name) \nEnter the model name: ")
    region = input("Enter the region (US/ EU): ")
    choice = input("Choose the table number: \n1. sales \n2. npc \n3. plc\n")

    table: dict = {
        "sales": ["v_fact_sales_bi"],
        "npc": ["v_npcomparison_migration_fact_bi"],
        "plc": ["v_phcomparison_fact_bi"]
    }

    parameter = {
        "datamodel_name": f"{tenant}_{case}_{env}_{model_name}",
        "dataset_name": f"{tenant}_{case}_{env}_{model_name}",
        "provider": "RedShift",
        "table_list": table[choice]
    }

    parameter.update(password_details(tenant, case, env))

    automate_cube_creation(parameter)


main()