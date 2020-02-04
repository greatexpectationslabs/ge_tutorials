select 
	n.*,
	t.provider_taxonomy_description,
	s.state as state_name
from {{ ref('stg_npi') }} n
left join {{ ref('stg_taxonomy') }} t
	on n.taxonomy_code = t.provider_taxonomy_code
left join {{ ref('stg_state_crosswalk') }} s
	on n.state = s.state_abbrev
