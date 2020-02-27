select 
	npi,
	entity_type_code,
	organization_name,
	last_name,
	first_name,
	state,
	taxonomy_code
from {{ ref('npi_small') }}
