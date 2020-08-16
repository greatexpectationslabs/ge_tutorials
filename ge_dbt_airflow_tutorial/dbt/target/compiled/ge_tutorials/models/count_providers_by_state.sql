select 
	state_name,
	count(distinct npi) as count_providers
from "airflow"."public"."npi_with_state" n
group by state_name