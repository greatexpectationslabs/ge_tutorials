from datetime import datetime

import airflow
from airflow import AirflowException
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
import os
import pandas as pd
from sqlalchemy import create_engine


from great_expectations import DataContext
from great_expectations.datasource.types import BatchKwargs


GE_TUTORIAL_DB_URL = os.getenv('GE_TUTORIAL_DB_URL')
GE_TUTORIAL_PROJECT_PATH = os.getenv('GE_TUTORIAL_PROJECT_PATH')


default_args = {
    "owner": "Airflow",
    "start_date": airflow.utils.dates.days_ago(1)
}

dag = DAG(
    dag_id='ge_tutorials_dag',
    default_args=default_args,
    schedule_interval=None,
)


def load_files_into_db(ds, **kwargs):

    engine = create_engine(GE_TUTORIAL_DB_URL)

    with engine.connect() as conn:
        conn.execute("drop table if exists npi_small cascade ")
        conn.execute("drop table if exists state_abbreviations cascade ")

        df_npi_small = pd.read_csv(os.path.join(GE_TUTORIAL_PROJECT_PATH, "data/npi_small.csv"))
        column_rename_dict = {old_column_name: old_column_name.lower() for old_column_name in df_npi_small.columns}
        df_npi_small.rename(columns=column_rename_dict, inplace=True)
        df_npi_small.to_sql("npi_small", engine,
                            schema=None,
                            if_exists='replace',
                            index=False,
                            index_label=None,
                            chunksize=None,
                            dtype=None)

        df_state_abbreviations = pd.read_csv(os.path.join(GE_TUTORIAL_PROJECT_PATH, "data/state_abbreviations.csv"))
        df_state_abbreviations.to_sql("state_abbreviations", engine,
                                      schema=None,
                                      if_exists='replace',
                                      index=False,
                                      index_label=None,
                                      chunksize=None,
                                      dtype=None)

    return 'Loaded files into the database'


task_load_files_into_db = PythonOperator(
    task_id='task_load_files_into_db',
    provide_context=True,
    python_callable=load_files_into_db,
    dag=dag,
)


task_dbt = BashOperator(
    task_id='task_dbt',
    bash_command='dbt run --project-dir {}'.format(GE_TUTORIAL_PROJECT_PATH),
    dag=dag)


def publish_to_prod():
    engine = create_engine(GE_TUTORIAL_DB_URL)

    with engine.connect() as conn:
        conn.execute("drop table if exists prod_count_providers_by_state")
        conn.execute("alter table count_providers_by_state rename to prod_count_providers_by_state")


task_publish = PythonOperator(
    task_id='task_publish',
    python_callable=publish_to_prod,
    dag=dag)

# def validate(expectation_suite_name, batch_kwargs):
#     """
#     Perform validations of the previously defined data assets according to their respective expectation suites.
#     """
#     context = DataContext()
#     batch = context.get_batch(batch_kwargs, expectation_suite_name)
#     run_id=datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ")
#     validation_result = batch.validate(run_id=run_id)
#     if not validation_result["success"]:
#         raise AirflowException(str(validation_result))
#

# Validation task - this is a v1 to only run one suite on a single batch
# I would probably make a single task to validate all staging tables and generate batch kwargs
# task_validate = PythonOperator(
#     task_id='task_validate',
#     python_callable=validate,
#     op_kwargs={
#         'expectation_suite_name': 'stg_npi.warning',
#         'batch_kwargs': BatchKwargs(
#             table='stg_npi',
#             schema='public',
#             datasource='ge_tutorials',
#         )
#     },
#     dag=dag,
# )

task_validate_source_data_load = BashOperator(
    task_id='task_validate_source_data_load',
    bash_command='', 
    dag=dag)

task_validate_analytical_output = BashOperator(
    task_id='task_validate_analytical_output',
    bash_command='', 
    dag=dag)

# Dependencies
task_load_files_into_db >> task_validate_source_data_load >> task_dbt >> task_validate_analytical_output >> task_publish
