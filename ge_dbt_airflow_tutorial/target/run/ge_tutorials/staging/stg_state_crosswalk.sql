
  
  create view "ge_tutorials"."public"."stg_state_crosswalk__dbt_tmp" as (
    select 
	name as state,
	abbreviation as state_abbrev
from "ge_tutorials"."public"."state_abbreviations"
  );
