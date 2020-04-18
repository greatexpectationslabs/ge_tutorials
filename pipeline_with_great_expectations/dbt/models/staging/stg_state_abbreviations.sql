select 
	name as state_name,
	abbreviation as state_abbreviation
  from {{ source('source', 'state_abbreviations') }}
