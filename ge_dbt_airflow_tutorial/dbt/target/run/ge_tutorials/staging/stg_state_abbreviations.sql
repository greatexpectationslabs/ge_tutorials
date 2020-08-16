
  
  create view "ge_tutorials"."public"."stg_state_abbreviations__dbt_tmp" as (
    select 
	name as state_name,
	abbreviation as state_abbreviation
  from "ge_tutorials"."public"."state_abbreviations"
  );
