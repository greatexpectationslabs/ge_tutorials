# Getting started with Great Expectations tutorial

This repository contains the relevant materials for the "Getting started with Great Expectations" tutorial in the Great Expectations docs. [Please follow the tutorials for instructions!](https://docs.greatexpectations.io/en/latest/guides/tutorials/getting_started.html)

## About the Docker image
The tutorial assumes you are using a local installation of Great Expectations (`pip install great_expectations`). We provide the sample data in a Postgres database as a Docker image to save you the data loading step. In order to run the Postgres server, do the following:
- Make sure you have Docker and docker-compose installed on your machine
- In a terminal, run `docker-compose up`, which will start up the Postgres server on `localhost` (on a non-default port, so it won't clash with any existing Postgres servers you might be running)
- The great_expectations.yml in this tutorial is already configured to connect to this Postgres database, so you won't need to do anything else
- In order to shut down the container, run `ctrl+c` and then `docker-compose down` to remove the container

## About the local Postgres database in the image
You shouldn't need to do anything with the Postgres database, but in case you want to connect to the database and inspect or modify the data, the credentials and port can be found in the docker-compose.yml in this directory.

