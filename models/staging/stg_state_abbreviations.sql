select 
	name as state_name,
	abbreviation as state_abbreviation
from {{ ref('state_abbreviations') }}
