# Getting started with Great Expectations tutorial - v3 (Batch Request) API

This repository contains the final version of the "Getting started with Great Expectations" tutorial in the Great 
Expectations docs. This repo can be used as a demo and to explore a complete Great Expectations deploy.

**THIS VERSION WAS CREATED WITH THE V3 (BATCH REQUEST) GREAT EXPECTATIONS API**, which is available in Great Expectations 
version 0.13.x and above. 

## 1. How to run through the tutorial
[Please follow the tutorial in our docs for instructions!](https://docs.greatexpectations.io/en/latest/guides/tutorials/getting_started_v3_api.html)

## 2. How to use this repo to explore and demo Great Expectations

### The `data` directory

The CSV files in the data directory are yellow taxi trip data that have been downloaded from the NYC taxi data website:
* [TLC trip record data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
* [Data dictionary](https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)

We created 10,000 row samples (using the Pandas ``sample`` function) from teh original CSV files for convenience and manually added some breaking changes (0s in the passenger_count column) to demonstrate potential data issues. 

In a future version of this tutorial, we might use "naturally occurring" data bugs :)

### The `great_expectations` directory
Currently, this demo contains the following:
* A `great_expectations.yml` file that's configured to use the top-level `data` directory as a Datasource. You will not need to set up anything to get it to work.
* A single Expectation Suite, `taxi.demo`, containing a handful of simple Expectations
* A Checkpoint `my_chk` that is set up to run the suite against the February data set
