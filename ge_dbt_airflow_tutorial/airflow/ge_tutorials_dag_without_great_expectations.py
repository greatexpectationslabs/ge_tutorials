from datetime import datetime
import airflow
from airflow import AirflowException
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
import os
import pandas as pd
from sqlalchemy import create_engine


# Global variables that are set using environment varaiables
GE_TUTORIAL_DB_URL = os.getenv('GE_TUTORIAL_DB_URL')
GE_TUTORIAL_ROOT_PATH = os.getenv('GE_TUTORIAL_ROOT_PATH')


default_args = {
    "owner": "Airflow",
    "start_date": airflow.utils.dates.days_ago(1)
}


# The DAG definition
dag = DAG(
    dag_id='ge_tutorials_dag_no_ge',
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


task_load_files_into_db = PythonOperator(
    task_id='task_load_files_into_db',
    provide_context=True,
    python_callable=load_files_into_db,
    dag=dag,
)


task_transform_data_in_db = BashOperator(
    task_id='task_transform_data_in_db',
    bash_command='dbt run --project-dir {}'.format(os.path.join(GE_TUTORIAL_ROOT_PATH, 'dbt')),
    dag=dag)


# DAG dependencies
task_load_files_into_db >> task_transform_data_in_db
