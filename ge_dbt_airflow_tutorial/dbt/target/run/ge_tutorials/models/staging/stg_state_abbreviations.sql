
  create view "airflow"."public"."stg_state_abbreviations__dbt_tmp" as (
    select 
	name as state_name,
	abbreviation as state_abbreviation
  from "airflow"."public"."state_abbreviations"
  );
