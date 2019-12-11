# DBMS_Fall19_project

ITWS DBMS Fall '19 final project

Team:
Gaurang Prasad
Satej Sawant

# Python Dependencies

If you already have python3 installed, you can install all python dependencies by running:

python3 -m pip install -r requirements.txt

# What datasets we've used

1. [Adult Arrest in New York](https://data.ny.gov/Public-Safety/Adult-Arrests-by-County-Beginning-1970/rikd-mt35)
2. [Liquor Authority Quarterly List of Active Licenses](https://data.ny.gov/Economic-Development/Liquor-Authority-Quarterly-List-of-Active-Licenses/hrvs-fxs2)
3. [Food Service Establishment Inspections](https://health.data.ny.gov/Health/Food-Service-Establishment-Inspections-Beginning-2/2hcc-shji)
4. [Unemployment Insurance Beneficiaries and Benefit Amounts Paid](https://data.ny.gov/Economic-Development/Unemployment-Insurance-Beneficiaries-and-Benefit-A/xbjp-8sra)

# What each query is about

## Locations with Liquor Licenses In New York State
### Filters
- County
- License Type Codes
```sql
select premise_name,doing_business_as,address,zipcode, license_type_name 
from liquor_license, license_types 
where county ilike 'ALBANY' 
AND liquor_license.license_type_code = license_types.license_type_code 
AND license_types.license_type_code IN ('D','MI','CF')
```

## Search for food operators in a specific county that hold a liquor license and have food service violations in a specific date range
### Filters
- County
- Start Date for Inspection
- End Date for Inspection
```sql
select liquor_license.doing_business_as, food_service_violations.violation_description,liquor_license.county,date_of_inspection
                    from food_service_operator,
                        liquor_license,
                        food_service_inspections,
                        food_service_violations
                    WHERE
                    food_service_operator.operation_name = liquor_license.premise_name
                    AND
                    food_service_operator.nys_health_operation_id = food_service_inspections.nys_health_operation_id
                    AND
                    food_service_inspections.violation_item NOT IN ('None')
                    AND
                    food_service_inspections.date_of_inspection >= %s AND
                        food_service_inspections.date_of_inspection <= %s
                    AND
                    food_service_violations.violation_item = food_service_inspections.violation_item
                    AND
                    liquor_license.county ilike %s 
```

