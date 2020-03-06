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
-- due to the nature of the data some state abbreviations are not valid
-- which results in state names being null  - in this case,
-- switch to inner join
inner join {{ ref('stg_state_abbreviations') }} s
	on n.state_abbreviation = s.state_abbreviation
