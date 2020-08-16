
  
  create view "ge_tutorials"."public"."stg_taxonomy__dbt_tmp" as (
    select 
	medicare_specialty_code,
	medicare_provider_supplier_type_description,
	provider_taxonomy_code,
	provider_taxonomy_description
from "ge_tutorials"."public"."healthcare_provider_taxonomy"
  );
