import os
import json
from dagster_dbt import DbtCliResource, dbt_assets
from dagster_airbyte import AirbyteResource
from dagster_airbyte import load_assets_from_airbyte_instance

resources = {
    "dbt": DbtCliResource(
        project_dir=os.getenv("DBT_PROJECT_DIR"),
        profiles_dir=os.getenv("DBT_PROFILES_DIR"),
    ),
    "airbyte_instance": AirbyteResource(
        host="localhost",
        port="8000",
        # If using basic auth, include username and password:
        username="airbyte",
        password=os.getenv("AIRBYTE_PASSWORD"),
    ),
}


@dbt_assets(
    manifest=json.load(
        open(os.path.join(os.getenv("DBT_PROJECT_DIR"), "target", "manifest.json"))
    ),
)
def dbt_assets():
    pass


airbyte_assets = load_assets_from_airbyte_instance(
    resources.get("airbyte_instance"), key_prefix=["raw_data"]
)
