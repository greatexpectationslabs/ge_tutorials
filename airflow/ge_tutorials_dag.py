from datetime import datetime

import airflow
from airflow import AirflowException
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow import DAG

from great_expectations import DataContext
from great_expectations.datasource.types import BatchKwargs

default_args = {
    "owner": "Airflow",
    "start_date": airflow.utils.dates.days_ago(1)
}

dag = DAG(
    dag_id='ge_tutorials_dag',
    default_args=default_args,
    schedule_interval=None,
)

task_dbt = BashOperator(
    task_id='run_dbt',
    bash_command='cd /Users/sam/code/ge_tutorials/; dbt run', # maybe we should pass in --project-dir <project_dir>
    dag=dag)


def validate(expectation_suite_name, batch_kwargs):
    """
    Perform validations of the previously defined data assets according to their respective expectation suites.
    """
    context = DataContext()
    batch = context.get_batch(batch_kwargs, expectation_suite_name)
    run_id=datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ")
    validation_result = batch.validate(run_id=run_id)
    if not validation_result["success"]:
        raise AirflowException(str(validation_result))


# Validation task - this is a v1 to only run one suite on a single batch
# I would probably make a single task to validate all staging tables and generate batch kwargs
task_validation = PythonOperator(
    task_id='validation',
    python_callable=validate,
    op_kwargs={
        'expectation_suite_name': 'stg_npi.warning',
        'batch_kwargs': BatchKwargs(
            table='stg_npi',
            schema='public',
            datasource='ge_tutorials',
        )
    },
    dag=dag,
)


# Dependencies
task_dbt >> task_validation
