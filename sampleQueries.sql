-- Query 1
-- Allow user to enter county and type of business
-- demonstrates a basic join and the IN operator
select premise_name,doing_business_as,address,zipcode, license_type_name from liquor_license, license_types
where county ilike 'Albany' AND
liquor_license.license_type_code = license_types.license_type_code
AND
license_types.license_type_code IN ('D','MI','CF');

-- Query 2
-- Allow the user to enter the date of inspection and maybe county? and maybe violation items
-- Join on 4 tables from 2 datasets,  use of date comparison, NOT IN
select liquor_license.county,date_of_inspection,food_service_violations.violation_description, liquor_license.doing_business_as, food_service_operator.operation_name, liquor_license.premise_name
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
food_service_inspections.date_of_inspection >= '01/01/2018' AND
      food_service_inspections.date_of_inspection <= '12/31/2018'
AND
food_service_violations.violation_item = food_service_inspections.violation_item;

-- Query 3
-- Is there a corelation between food service inspections finding unhygenic conditions and property misdemanors?LOL

select csm.county, cs, property_misdemanors  from (select county,sum(total_critical_violations+ total_critical_violations) as cs
from food_service_inspections
where
total_critical_violations + total_noncritical_violations > 10
AND
date_of_inspection between '01/01/2018' AND '12/31/2018'
AND
violation_item IN ('14A','12E','1B','8F','3B','23','62')
GROUP BY county) as csm, (select county, sum(property_misdemeanor) as property_misdemanors from adult_arrests
where year = 2018
group by county
) as ad
where upper(csm.county) = upper(ad.county);
