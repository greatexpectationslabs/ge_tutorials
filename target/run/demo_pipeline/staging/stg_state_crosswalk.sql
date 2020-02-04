
  
  create view "demo_db"."public"."stg_state_crosswalk__dbt_tmp" as (
    select 
	name as state,
	abbreviation as state_abbrev
from "demo_db"."public"."abbr-name-list"
  );
