from pathlib import Path

from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator,
)

from airflow.decorators import dag
from airflow.operators.bash_operator import BashOperator
from airflow.providers.airbyte.operators.airbyte import (
    AirbyteTriggerSyncOperator,
)
from airflow.utils.dates import days_ago


# Default DAG args
default_args = {
    "owner": "airflow",
    "catch_up": False,
}
BASE_DIR = Path(__file__).parent.parent.parent.absolute()
GE_ROOT_DIR = Path(BASE_DIR, "great_expectations")
DBT_ROOT_DIR = Path(BASE_DIR, "dbt_transforms")


@dag(
    dag_id="dataops",
    description="DataOps workflows.",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=["dataops"],
)
def dataops():
    """DataOps workflows."""
    # Extract + Load
    extract_and_load_projects = AirbyteTriggerSyncOperator(
        task_id="extract_and_load_projects",
        airbyte_conn_id="airbyte",
        connection_id="15ae1306-bfc6-4117-a59d-f28ee9f427df",
        asynchronous=False,
        timeout=3600,
        wait_seconds=3,
    )
    extract_and_load_tags = AirbyteTriggerSyncOperator(
        task_id="extract_and_load_tags",
        airbyte_conn_id="airbyte",
        connection_id="0367d38e-fa1b-4703-94a8-d0d6065f5a02",
        asynchronous=False,
        timeout=3600,
        wait_seconds=3,
    )
    validate_projects = GreatExpectationsOperator(
        task_id="validate_projects",
        checkpoint_name="projects",
        data_context_root_dir=GE_ROOT_DIR,
        fail_task_on_validation_failure=True,
    )
    validate_tags = GreatExpectationsOperator(
        task_id="validate_tags",
        checkpoint_name="tags",
        data_context_root_dir=GE_ROOT_DIR,
        fail_task_on_validation_failure=True,
    )

    # Transform
    transform = BashOperator(task_id="transform", bash_command=f"cd {DBT_ROOT_DIR} && dbt run && dbt test")
    validate_transforms = GreatExpectationsOperator(
        task_id="validate_transforms",
        checkpoint_name="labeled_projects",
        data_context_root_dir=GE_ROOT_DIR,
        fail_task_on_validation_failure=True,
    )

    # Define DAG
    extract_and_load_projects >> validate_projects
    extract_and_load_tags >> validate_tags
    [validate_projects, validate_tags] >> transform >> validate_transforms


# Run DAGs
do = dataops()
