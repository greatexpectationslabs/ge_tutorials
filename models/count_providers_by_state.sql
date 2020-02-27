select 
	state_name,
	count(distinct npi) as count_providers
from {{ ref('npi_with_state') }} n
group by state_name
