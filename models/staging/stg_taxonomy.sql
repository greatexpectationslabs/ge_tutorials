select 
	medicare_specialty_code,
	medicare_provider_supplier_type_description,
	provider_taxonomy_code,
	provider_taxonomy_description
from {{ ref('healthcare_provider_taxonomy') }}
