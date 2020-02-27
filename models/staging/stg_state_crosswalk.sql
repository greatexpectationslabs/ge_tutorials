select 
	name as state,
	abbreviation as state_abbrev
from {{ ref('state_abbreviations') }}
