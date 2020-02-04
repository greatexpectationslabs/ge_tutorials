
  
  create view "demo_db"."public"."stg_npi__dbt_tmp" as (
    select 
	*
from "demo_db"."public"."npi_small_2019"
  );
