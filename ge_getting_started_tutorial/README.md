# Getting started with Great Expectations tutorial

This repository contains the final version of the "Getting started with Great Expectations" tutorial in the Great Expectations docs. It provides both the relevant data in a local Postgres database, as well as as a set of Expectation suites and Checkpoints to explore Great Expectations. This repo can be used for two things:
1. Run through the Great Expectations tutorial from scratch
2. Use the repo as a demo and to explore a complete Great Expectations deploy

## 1. How to run through the tutorial
[Please follow the tutorial in our docs for instructions!](https://docs.greatexpectations.io/en/latest/guides/tutorials/getting_started.html)

## 2. How to use this repo to explore and demo Great Expectations

### About the Docker image
The tutorial assumes you are using a local installation of Great Expectations (`pip install great-expectations`). We provide the sample data in a Postgres database as a Docker image to save you the data loading step. In order to run the Postgres server, do the following:
- Make sure you have Docker and docker-compose installed on your machine
- In a terminal, run `docker-compose up`, which will start up the Postgres server on `localhost` (on a non-default port, so it won't clash with any existing Postgres servers you might be running)
- The great_expectations.yml in this tutorial is already configured to connect to this Postgres database, so you won't need to do anything else
- In order to shut down the container, run `ctrl+c` and then `docker-compose down` to remove the container

### About the local Postgres database in the image
You shouldn't need to do anything with the Postgres database, but in case you want to connect to the database and inspect or modify the data, the credentials and port can be found in the docker-compose.yml in this directory.

### The `great_expectations` directory
Currently, this demo contains the following:
* A great_expectations.yml that's configured to connect to the local Postgres database. You will not need to set up anything to get it to work.
* A single Expectation Suite, `taxi.demo`, containing a handful of simple Expectations
    * You can explore the validation output of this suite by running the `validation_playground` notebook in `great_expectations/notebooks/sql/`
    * The Expectation Suite will pass when run against the January data, and fail when run against the February data in the staging table (due to the messy data we introduced)
* A Checkpoint `taxi.demo.staging.chk` that is set up to run the suite against the staging table
* If you want the Slack webhook to work, drop a webhook URL into the respective section for demo purposes, or create an uncommitted/config_variables.yml file and drop the following in there: `slack_webhook: https://hooks.slack.com/services/my_slack_webhook_url`

### The `data` directory

#### About the NYC taxi data

The CSV files in the data directory are yellow taxi trip data that have been downloaded from the NYC taxi data website:
* Data: https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
* Data dictionary: https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

We created 10,000 row samples (using the pandas sample function) from original CSV files for convenience and manually added some breaking changes (0s in the passenger_count column) to demonstrate potential data issues. 

In a future version of this tutorial, we might use "naturally occurring" data bugs :)

#### About the load script
The SQL load script is a simple script to load the provided data tables to a Postgres database. They're provided for convenience, you can also use a different backend and your own method to make the data available for this demo.

#### About the analysis
This is a very simple Jupyter notebook that creates histograms of the passenger count variable in the data. We created this for the purpose of this demo.

