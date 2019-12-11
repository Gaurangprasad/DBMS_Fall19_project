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
from food_service_operator,liquor_license,food_service_inspections, food_service_violations
WHERE
food_service_operator.operation_name = liquor_license.premise_name
AND
food_service_operator.nys_health_operation_id = food_service_inspections.nys_health_operation_id
AND
food_service_inspections.violation_item NOT IN ('None')
AND
food_service_inspections.date_of_inspection >= '2018-01-01' AND food_service_inspections.date_of_inspection <= '2018-12-31'
AND
food_service_violations.violation_item = food_service_inspections.violation_item
AND
liquor_license.county ilike 'Albany' 
```
## Is there a corelation between places with food violations and property misdemanors?
### Filters
- Start Date for Inspection
- End Date for Inspection
- List of Violation Items
- Year for Misdemanors
```sql
select csm.county, cs, property_misdemanors  from (select county,sum(total_critical_violations+ total_critical_violations) as cs
        from food_service_inspections
        where
        total_critical_violations + total_noncritical_violations > 10
        AND
        date_of_inspection between '2018-01-01' AND '2018-12-31'
        AND
        violation_item IN ('14A','12E','1B','8F','3B','23','62')
        GROUP BY county) as csm, (select county, sum(property_misdemeanor) as property_misdemanors from adult_arrests
        where year = '2018'
        group by county
        ) as ad
        where upper(csm.county) = upper(ad.county)
```

## What's the restaurant with the most number of violations consistently per county?

```sql
        SELECT dsa.*
        FROM (select county,operation_name,food_service_inspections.nys_health_operation_id, count(violation_item) as vi from food_service_inspections, food_service_operator
        where food_service_operator.nys_health_operation_id = food_service_inspections.nys_health_operation_id
        group by food_service_inspections.nys_health_operation_id, county, operation_name) as dsa
        LEFT JOIN (select county,nys_health_operation_id, count(violation_item) as vi from food_service_inspections
        group by nys_health_operation_id, county) as dsa2
            ON dsa.county = dsa2.county AND dsa.vi < dsa2.vi
        WHERE dsa2.vi is NULL
        ORDER BY dsa.county ASC ;
 ```
