# Great Expectations Pipeline Tutorial
This is a typical end-to-end project with dbt, GE, airflow for the purpose of demonstrating how to implement Great Expectations alongside dbt and airflow. The purpose of this tutorial is simply to show how the individual components work together. Therefore, both the dbt and the Great Expectations components are kept fairly trivial, but hopefully realistic.

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
* `export GE_TUTORIAL_PROJECT_PATH=your_project_path`


## Pipeline overview

The pipeline will look familiar to lots of data teams working with ELT pattern. It loads data from files into a database and then transforms it. 
The pipeline simply takes two data input files and processes them in a WAP (write - audit - publish) type pattern:
1. Use GE to validate the input CSV files. Stop if they do not meet our expectations 
2. Load the source files to a postgres database using SQLAlchemy
3. Use GE to validate that the data was loaded into the database successfully
4. Run the dbt DAG to create a simple analytical table, see the dbt DAG snapshot below:
![The dbt DAG](images/dbt_dag.png)
5. Use GE to validate the analytical result.
6. If the analytical result is valid, publish (promote) the analytical table to a "prod" table by renaming it

The entire pipeline is orchestrated with the following airflow DAG:
![The airflow DAG](images/airflow_dag.png)

## Running the pipeline

You can run each individual task in the airflow DAG with `airflow test ge_tutorials_dag <task_name>`.
In order to run the entire DAG, use `airflow backfill ge_tutorials_dag -s <start_date> -e <end_date>`.


```
airflow@f780ca38c898:~/great_expectations/notebooks$ jupyter notebook --allow-root --notebook-dir=. --ip=0.0.0.0 --port=8888 --no-browser
[I 23:13:56.380 NotebookApp] Writing notebook server cookie secret to /usr/local/airflow/.local/share/jupyter/runtime/notebook_cookie_secret
[I 23:13:56.696 NotebookApp] Serving notebooks from local directory: /usr/local/airflow/great_expectations/notebooks
[I 23:13:56.697 NotebookApp] The Jupyter Notebook is running at:
[I 23:13:56.698 NotebookApp] http://f780ca38c898:8888/?token=3759714dd219e6bd2a9ee266d5b55a353785f6dc1ea4e7fe
[I 23:13:56.698 NotebookApp]  or http://127.0.0.1:8888/?token=3759714dd219e6bd2a9ee266d5b55a353785f6dc1ea4e7fe
[I 23:13:56.699 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 23:13:56.707 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///usr/local/airflow/.local/share/jupyter/runtime/nbserver-27198-open.html
    Or copy and paste one of these URLs:
        http://f780ca38c898:8888/?token=3759714dd219e6bd2a9ee266d5b55a353785f6dc1ea4e7fe
```

Should be a Separate PR, beginnings of Airflow Plugin for great expectation
https://stackoverflow.com/questions/56461918/airlfow-serving-static-html-directory
https://airflow.apache.org/docs/stable/plugins.html#example
