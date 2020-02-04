
  
  create view "demo_db"."public"."stg_taxonomy__dbt_tmp" as (
    select 
	*
from "demo_db"."public"."HEALTHCARE_PROVIDER_TAXONOMY"
  );
