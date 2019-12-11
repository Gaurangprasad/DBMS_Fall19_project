# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 22:37:58 2019

@author: GaurangPrasadML
"""

import psycopg2
import psycopg2.extras
import pandas


class PSQLInterfaceClass:

    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)

    def run(self, query, params = None):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, params)
            return pandas.DataFrame(cursor.fetchall())

    def show(self, query):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            return cursor.mogrify(query)
    
    def viewAllLiquorCodes(self):
        query = """select * from license_types """
        return self.run(query)
    
    def viewAllFoodViolations(self):
        query = """select * from food_service_violations """
        return self.run(query)
        
    def query1(self, params):
    # Basic join and using IN operator
        
        query = """select premise_name,doing_business_as,address,zipcode, license_type_name from liquor_license, license_types where county ilike %s AND liquor_license.license_type_code = license_types.license_type_code AND license_types.license_type_code IN %s"""
        return self.run(query, params)
    
    def query2(self, params):
        query = """select liquor_license.doing_business_as, food_service_violations.violation_description,liquor_license.county,date_of_inspection
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
                    """
        return self.run(query, params)
    
    def query3(self, params):
        query = """
        select csm.county, cs, property_misdemanors  from (select county,sum(total_critical_violations+ total_critical_violations) as cs
        from food_service_inspections
        where
        total_critical_violations + total_noncritical_violations > %s
        AND
        date_of_inspection between %s AND %s
        AND
        violation_item IN %s
        GROUP BY county) as csm, (select county, sum(property_misdemeanor) as property_misdemanors from adult_arrests
        where year = %s
        group by county
        ) as ad
        where upper(csm.county) = upper(ad.county)
        """
        return self.run(query, params)
        
    def query4(self):
    
        query = """
        SELECT dsa.*
        FROM (select county,operation_name,food_service_inspections.nys_health_operation_id, count(violation_item) as vi from food_service_inspections, food_service_operator
        where food_service_operator.nys_health_operation_id = food_service_inspections.nys_health_operation_id
        group by food_service_inspections.nys_health_operation_id, county, operation_name) as dsa
        LEFT JOIN (select county,nys_health_operation_id, count(violation_item) as vi from food_service_inspections
        group by nys_health_operation_id, county) as dsa2
            ON dsa.county = dsa2.county AND dsa.vi < dsa2.vi
        WHERE dsa2.vi is NULL
        ORDER BY dsa.county ASC ;
        """
        return self.run(query)
    
    
    def query6(self, params):
        query = "select * from adult_arrests where county ilike %s and year = %s"
        return self.run(query, params)
    