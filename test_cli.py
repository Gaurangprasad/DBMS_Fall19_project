# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 23:25:40 2019

@author: GaurangPrasadML
"""
import warnings
import argparse
import itertools
from psql_structure import FoodViolationData
from json_structure import InsuranceData

def query1():
    county = input('Enter county: ')
            # license_codes = input('Enter license codes')
    query = """ select premise_name,doing_business_as,address,zipcode, license_type_name from liquor_license, license_types
    where county ilike '""" + county + """' AND
    liquor_license.license_type_code = license_types.license_type_code
    AND
    license_types.license_type_code IN ('D','MI','CF') """
            # Looking for estabishments that have the word BUFFET in their name and are in ALBANY
    print(fd_vio.directQuery(query))

def query2():
    start_date = input('Enter start date(DD/MM/YYYY):')
    end_date = input('Enter end date(DD/MM/YYYY):')
    query = """select liquor_license.county,date_of_inspection,food_service_violations.violation_description, liquor_license.doing_business_as
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
                        food_service_inspections.date_of_inspection >= '""" + start_date + """' AND
                            food_service_inspections.date_of_inspection <= '""" + end_date + """'
                        AND
                        food_service_violations.violation_item = food_service_inspections.violation_item;
                        """
    print(fd_vio.directQuery(query))

def query3():
    print("Hello")
    start_date = input('Enter start date(DD/MM/YYYY):')
    end_date = input('Enter end date(DD/MM/YYYY):')
    yearOfArrest = input('Adult Arrests Year')
    minViolations = input('Min Violations')
    query = """
        select csm.county, cs, property_misdemanors  from (select county,sum(total_critical_violations+ total_critical_violations) as cs
        from food_service_inspections
        where
        total_critical_violations + total_noncritical_violations > '""" + minViolations + """'
        AND
        date_of_inspection between '""" + start_date + """' AND '""" + end_date + """'
        AND
        violation_item IN ('14A','12E','1B','8F','3B','23','62')
        GROUP BY county) as csm, (select county, sum(property_misdemeanor) as property_misdemanors from adult_arrests
        where year = '""" + yearOfArrest + """'
        group by county
        ) as ad
        where upper(csm.county) = upper(ad.county);
        """
    print(fd_vio.directQuery(query))


if __name__ == "__main__":
    
    # Handling command line arguments
    arg = argparse.ArgumentParser()
    fd_vio = FoodViolationData("host='localhost' dbname='test5' user='test5' password='test5'")
    ins = InsuranceData()
    #print(ins.is_connected())
    arg.add_argument("--view",
                     help="True to view all available queries.")
    arg.add_argument("--query",
                     help="Pass corresponding query number from query list (which can be viewed using the --view argument).")
    parser = vars(arg.parse_args())
    
    if(parser['view']):
        print("Here are the list of queries supported by the application. To run a query, do python test_cli.py --query QUERY_NUM \nwhere QUERY_NUM is the number in the following list: ")
        print()
        print()
        print("1. Allow user to enter county and type of business. Demonstrates a basic join and the IN operator")
    
    if(parser['query'] is not None):
        queryNumber = int(parser['query'])
        if(queryNumber == 1 ):
            query1()
        elif(queryNumber == 2):
            query2()
        elif(queryNumber == 3):
            query3()




        
        