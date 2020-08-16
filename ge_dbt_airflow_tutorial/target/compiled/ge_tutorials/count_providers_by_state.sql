select 
	state_name,
	count(distinct npi) as count_providers
from "ge_tutorials"."public"."npi_with_state" n
group by state_name