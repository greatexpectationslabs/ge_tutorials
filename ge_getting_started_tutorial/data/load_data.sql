-- A simple SQL script to create a table in postgres and load the
-- taxi data to those tables.
-- Needs to be run from this directory,  or adjust the file paths.
-- Feel free to use your own method, this is just provided for convenience.

create table yellow_tripdata_sample_2019_01 (
  vendor_id text,
  pickup_datetime timestamp,
  dropoff_datetime timestamp,
  passenger_count numeric,
  trip_distance numeric,
  rate_code_id text,
  store_and_fwd_flag text,
  pickup_location_id numeric,
  dropoff_location_id numeric,
  payment_type text,
  fare_amount numeric,
  extra numeric,
  mta_tax numeric,
  tip_amount numeric,
  tolls_amount numeric,
  improvement_surcharge numeric,
  total_amount numeric,
  congestion_surcharge numeric
);

\copy yellow_tripdata_sample_2019_01 from '/tmp/yellow_tripdata_sample_2019-01.csv' with delimiter ',' csv header;

-- Create the "staging" table as a copy of the first one and load the February data into it
create table yellow_tripdata_staging as table yellow_tripdata_sample_2019_01 with no data;
\copy yellow_tripdata_staging from '/tmp/yellow_tripdata_sample_2019-02.csv' with delimiter ',' csv header;
