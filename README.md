# Great Expectations Pipeline Tutorial
This is a typical end-to-end project with dbt, GE, airflow for the purpose of demonstrating how to implement Great Expectations alongside dbt and airflow.

## Setup

In order to run this project, you will need to go through some basic setup steps.

### Postgres database setup
For the purpose of this demo, we work with a postgres database. Make sure to have access to a postgres server. If desired, create a new, empty database for this tutorial.

### Install and configure tools
* airflow - run `airflow initdb` and set up $AIRFLOW_HOME and point the dags_modules in airflow.cfg to the project path
* dbt - set up your database connection in the dbt_profile.yml (see the example_dbt_profile.yml in this project)
* great_expectations - no further setup needed

### Environment variables

The pipeline's configuration variables are passed using env variables. Set the following variables:
* `export GE_TUTORIAL_DB_URL=postgresql://your_user:your_password@your_dh_host:5432/your_db_name`
* `export GE_TUTORIAL_PROJECT_PATH=/Users/your_project_path`


## Pipeline overview

The pipeline simply takes two data input files and processes them in a WAP (write - audit - publish) type pattern:
1. Load the source files to a postgres database using SQLAlchemy
2. Validate the source data files with Great Expectations
3. Run the dbt DAG to create a simple analytical table, see the dbt DAG snapshot below.
4. Validate the analytical result
5. Publish (promote) the analytical table to a "prod" table by renaming it

![The dbt DAG][dbt_dag.png]

![The airflow DAG][airflow_dag.png]

**The purpose of this tutorial is simply to show how the individual components work together. Therefore, both the dbt and the Great Expectations components are kept fairly trivial, but hopefully realistic.**