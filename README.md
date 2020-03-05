# Great Expectations Pipeline Tutorial
This is a typical end-to-end project with dbt, GE, airflow for the purpose of demonstrating how to implement Great Expectations alongside dbt and airflow. The purpose of this tutorial is simply to show how the individual components work together. Therefore, both the dbt and the Great Expectations components are kept fairly trivial, but hopefully realistic.

## Setup

In order to run this project, you will need to go through some basic setup steps.

### Database setup
For the purpose of this demo, we assume you have a relational database available that can be accessed using a SQLAlchemy connection URL. We developed the tutorial using a postgres database. Of course, this can be replaced by any other DBMS when working on a real pipeline.

### Install and configure tools
* airflow - run `airflow initdb`, set up `$AIRFLOW_HOME` and point the dags_folder in airflow.cfg to the project path
* dbt - set up your database connection in the dbt_profile.yml (see the example_dbt_profile.yml in this project)
* great_expectations - no further setup needed

### Environment variables

The pipeline's configuration variables are passed using environment variables. Set the following variables:
* `export GE_TUTORIAL_DB_URL=postgresql://your_user:your_password@your_dh_host:5432/your_db_name`
* `export GE_TUTORIAL_PROJECT_PATH=your_project_path`


## Pipeline overview

The pipeline simply takes two data input files and processes them in a WAP (write - audit - publish) type pattern:
1. Load the source files to a postgres database using SQLAlchemy
2. Validate the source data files with Great Expectations
3. Run the dbt DAG to create a simple analytical table, see the dbt DAG snapshot below:
![The dbt DAG](images/dbt_dag.png)
4. Validate the analytical result
5. Publish (promote) the analytical table to a "prod" table by renaming it

The entire pipeline is orchestrated with the following airflow DAG:
![The airflow DAG](images/airflow_dag.png)

## Running the pipeline

You can run each individual task in the airflow DAG with `airflow test ge_tutorials_dag <task_name>`.
In order to run the entire DAG, use `airflow backfill ge_tutorials_dag -s <start_date> -e <end_date>`.

