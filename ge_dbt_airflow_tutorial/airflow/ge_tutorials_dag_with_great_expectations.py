from datetime import datetime
import airflow
from airflow import AirflowException
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
import os
import pandas as pd
from sqlalchemy import create_engine
import great_expectations as ge


# Global variables that are set using environment varaiables
GE_TUTORIAL_DB_URL = os.getenv('GE_TUTORIAL_DB_URL')
GE_TUTORIAL_ROOT_PATH = os.getenv('GE_TUTORIAL_ROOT_PATH')

great_expectations_context_path = os.getenv('GE_TUTORIAL_GE_CONTEXT_PATH') or os.path.join(GE_TUTORIAL_ROOT_PATH, "great_expectations_projects", "final", "great_expectations")


default_args = {
    "owner":` "Airflow",
    "start_date": airflow.utils.dates.days_ago(1)
}


# The DAG definition
dag = DAG(
    dag_id='ge_tutorials_dag_with_ge',
    default_args=default_args,
    schedule_interval=None,
)


def load_files_into_db(ds, **kwargs):
    """
        A method to simply load CSV files into a database using SQLAlchemy.
    """

    engine = create_engine(GE_TUTORIAL_DB_URL)

    with engine.connect() as conn:
        conn.execute("drop table if exists npi_small cascade ")
        conn.execute("drop table if exists state_abbreviations cascade ")

        df_npi_small = pd.read_csv(os.path.join(GE_TUTORIAL_ROOT_PATH, "data", "npi_small.csv"))
        column_rename_dict = {old_column_name: old_column_name.lower() for old_column_name in df_npi_small.columns}
        df_npi_small.rename(columns=column_rename_dict, inplace=True)
        df_npi_small.to_sql("npi_small", engine,
                            schema=None,
                            if_exists='replace',
                            index=False,
                            index_label=None,
                            chunksize=None,
                            dtype=None)

        df_state_abbreviations = pd.read_csv(os.path.join(GE_TUTORIAL_ROOT_PATH, "data", "state_abbreviations.csv"))
        df_state_abbreviations.to_sql("state_abbreviations", engine,
                                      schema=None,
                                      if_exists='replace',
                                      index=False,
                                      index_label=None,
                                      chunksize=None,
                                      dtype=None)

    return 'Loaded files into the database'


def validate_source_data(ds, **kwargs):

    context = ge.data_context.DataContext(great_expectations_context_path)

    batch_kwargs_file = {"path": os.path.join(GE_TUTORIAL_ROOT_PATH, "data", "npi_small.csv"),
                         'datasource': 'input_files'}

    batch_file = context.get_batch(batch_kwargs_file, 'npi_small_file.critical')


    results = context.run_validation_operator(
        "action_list_operator",
        assets_to_validate=[batch_file],
        run_id="airflow:" + kwargs['dag_run'].run_id + ":" + str(kwargs['dag_run'].start_date))

    if not results["success"]:
        raise AirflowException("Validation of the source data is not successful ")


def validate_source_data_load(ds, **kwargs):

    # Data Context is a GE object that represents your project.
    # Your project's great_expectations.yml contains all the config
    # options for the project's GE Data Context.
    context = ge.data_context.DataContext(great_expectations_context_path)

    datasource_name_file = "input_files"
    expectation_suite_name_file = "npi_small_file.critical"
    batch_kwargs_file = {"path": os.path.join(GE_TUTORIAL_ROOT_PATH, "data", "npi_small.csv"),
                         'datasource': 'input_files'}
    batch_file = context.get_batch(batch_kwargs_file, expectation_suite_name_file)

    expectation_suite_name_db = "npi_small_db_table.critical"
    datasource_name_file_db = "datawarehouse"

    # If you would like to validate an entire table or view in your database's default schema:
    batch_kwargs_db = {'table': "npi_small", 'datasource': datasource_name_file_db}

    # # If you would like to validate an entire table or view from a non-default schema in your database:
    # batch_kwargs = {'table': "YOUR_TABLE", "schema": "YOUR_SCHEMA", 'datasource': datasource_name}

    # If you would like to validate the result set of a query:
    # batch_kwargs = {'query': 'SELECT YOUR_ROWS FROM YOUR_TABLE', 'datasource': datasource_name}

    batch_db = context.get_batch(batch_kwargs_db, expectation_suite_name_db)

    # Call a validation operator to validate the batch.
    # The operator will evaluate the data against the expectations
    # and perform a list of actions, such as saving the validation
    # result, updating Data Docs, and firing a notification (e.g., Slack).
    run_id = datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ")
    run_id = "airflow:" + kwargs['dag_run'].run_id + ":" + str(kwargs['dag_run'].start_date)
    results = context.run_validation_operator(
        "action_list_operator",
        assets_to_validate=[batch_file, batch_db],
        run_id=run_id)  # e.g., Airflow run id or some run identifier that your pipeline uses.

    if not results["success"]:
        raise AirflowException("Validation of the source data loading is not successful ")



def validate_analytical_output(ds, **kwargs):

    # Data Context is a GE object that represents your project.
    # Your project's great_expectations.yml contains all the config
    # options for the project's GE Data Context.
    context = ge.data_context.DataContext(great_expectations_context_path)

    datasource_name = "datawarehouse"  # a datasource configured in your great_expectations.yml

    # Tell GE how to fetch the batch of data that should be validated...

    # ... from the result set of a SQL query:
    # batch_kwargs = {"query": "your SQL query", "datasource": datasource_name}

    # ... or from a database table:
    batch_kwargs = {"table": "count_providers_by_state", "datasource": datasource_name}

    # ... or from a file:
    # batch_kwargs = {"path": "path to your data file", "datasource": datasource_name}

    # ... or from a Pandas or PySpark DataFrame
    # batch_kwargs = {"dataset": "your Pandas or PySpark DataFrame", "datasource": datasource_name}

    # Get the batch of data you want to validate.
    # Specify the name of the expectation suite that holds the expectations.
    expectation_suite_name = "count_providers_by_state.critical"  # this is an example of
    # a suite that you created
    batch = context.get_batch(batch_kwargs, expectation_suite_name)

    # Call a validation operator to validate the batch.
    # The operator will evaluate the data against the expectations
    # and perform a list of actions, such as saving the validation
    # result, updating Data Docs, and firing a notification (e.g., Slack).
    run_id = datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ")
    run_id = "airflow:" + kwargs['dag_run'].run_id + ":" + str(kwargs['dag_run'].start_date)
    results = context.run_validation_operator(
        "action_list_operator",
        assets_to_validate=[batch],
        run_id=run_id)  # e.g., Airflow run id or some run identifier that your pipeline uses.

    if not results["success"]:
        raise AirflowException("The analytical output does not meet the expectations in the suite: {0:s}".format(expectation_suite_name))


def publish_to_prod():
    """
        A method to simply "promote' a table in a database by renaming it using SQLAlchemy.
    """
    engine = create_engine(GE_TUTORIAL_DB_URL)

    with engine.connect() as conn:
        conn.execute("drop table if exists prod_count_providers_by_state")
        conn.execute("alter table count_providers_by_state rename to prod_count_providers_by_state")


task_validate_source_data = PythonOperator(
    task_id='task_validate_source_data',
    python_callable=validate_source_data,
    provide_context=True,
    dag=dag)

task_load_files_into_db = PythonOperator(
    task_id='task_load_files_into_db',
    provide_context=True,
    python_callable=load_files_into_db,
    dag=dag,
)

task_validate_source_data_load = PythonOperator(
    task_id='task_validate_source_data_load',
    python_callable=validate_source_data_load,
    provide_context=True,
    dag=dag)

task_transform_data_in_db = BashOperator(
    task_id='task_transform_data_in_db',
    bash_command='dbt run --project-dir {}'.format(os.path.join(GE_TUTORIAL_ROOT_PATH, 'dbt')),
    dag=dag)


task_validate_analytical_output = PythonOperator(
    task_id='task_validate_analytical_output',
    python_callable=validate_analytical_output,
    provide_context=True,
    dag=dag)


task_publish = PythonOperator(
    task_id='task_publish',
    python_callable=publish_to_prod,
    dag=dag)


# DAG dependencies
task_validate_source_data >> task_load_files_into_db >> task_validate_source_data_load >> task_transform_data_in_db >> task_validate_analytical_output >> task_publish
