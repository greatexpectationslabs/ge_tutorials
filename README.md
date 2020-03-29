# Great Expectations Pipeline Tutorial
This is a typical end-to-end project with dbt, GE, airflow for the purpose of demonstrating how to implement Great Expectations alongside dbt and airflow. The purpose of this tutorial is to show how the individual components work together. Therefore, both the dbt and the Great Expectations components are kept fairly trivial, but hopefully realistic.

**Please note** This tutorial is a proof of concept and (as of March 2020) still new/work in progress. Feel free to provide *feedback via Slack, a GitHub issue, or just fork it and show us your own implementation*, we'll be happy to answer questions and iterate on the content to make it more useful for the community!

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
* `export GE_TUTORIAL_PIPELINE_ROOT_PATH=your_project_path`


## Pipeline overview

The pipeline will look familiar to lots of data teams working with ELT pattern. 
It loads data from files into a database and then transforms it.


This repo contains two implementations of this data pipeline:
* before Great Expectations was added - in `pipeline_without_great_expectations` folder
* after Great Expectations was added - in `pipeline_with_great_expectations` folder 

### Without Great Expectations

![The airflow DAG](images/pipeline_airflow_dag_without_ge.png)
 
1. Load the source files to a postgres database using SQLAlchemy
2. Run the dbt DAG to create a simple analytical table, see the dbt DAG snapshot below:
![The dbt DAG](images/dbt_dag.png)


### With Great Expectations

![The airflow DAG](images/pipeline_airflow_dag_with_ge.png)

1. Use GE to validate the input CSV files. Stop if they do not meet our expectations 
2. Load the source files to a postgres database using SQLAlchemy
3. Use GE to validate that the data was loaded into the database successfully
4. Run the dbt DAG to create a simple analytical table, see the dbt DAG snapshot below:
5. Use GE to validate the analytical result.
6. If the analytical result is valid, publish (promote) the analytical table to a "prod" table by renaming it


## Running the pipeline

You can run each individual task in the airflow DAG with `airflow test ge_tutorials_dag <task_name>`.
In order to run the entire DAG, use `airflow backfill ge_tutorials_dag -s <start_date> -e <end_date>`.

