select 
	n.npi,
	n.entity_type_code,
	n.organization_name,
	n.last_name,
	n.first_name,
	n.taxonomy_code,
	n.state_abbreviation,
	s.state_name
from {{ ref('stg_npi') }} n
left join {{ ref('stg_state_abbreviations') }} s
	on n.state_abbreviation = s.state_abbreviation
