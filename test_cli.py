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
import psycopg2
import psycopg2.extras
import pandas

# https://stackoverflow.com/a/37045601/4759033
def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def query1():
    county = input('Enter county: ')
    license_string = input('Enter license codes separated by a space: ')
    lic_arr = license_string.split()
    query = """select premise_name,doing_business_as,address,zipcode, license_type_name from liquor_license, license_types where county ilike %s AND liquor_license.license_type_code = license_types.license_type_code AND license_types.license_type_code IN %s"""
    cursor.execute(query, (county, tuple(lic_arr)))
    print(pandas.DataFrame(cursor.fetchall()))

def query2():
    start_date = input('Enter start date(DD/MM/YYYY):')
    if(validate(start_date) == False):
        print("Invalid date")
        return
    end_date = input('Enter end date(DD/MM/YYYY):')
    if(validate(end_date) == False):
        print("Invalid date")
        return
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
    start_date = input('Enter start date(DD/MM/YYYY):')
    if(validate(start_date) == False):
        print("Invalid date")
        return
    end_date = input('Enter end date(DD/MM/YYYY):')
    if(validate(end_date) == False):
        print("Invalid date")
        return
    yearOfArrest = input('Adult Arrests Year')
    minViolations = input('Min Violations')
    license_string = input('Enter violation codes separated by a space: ')
    lic_arr = license_string.split()
    licQuery = ""
    first = 1
    for licID in lic_arr:
        if (first == 1):
            licQuery = "'"+ licID + "'"
            first = 0
        else:
            licQuery = licQuery + ",'"+ licID + "'"
    #  '14A','12E','1B','8F','3B','23','62'
    query = """
        select csm.county, cs, property_misdemanors  from (select county,sum(total_critical_violations+ total_critical_violations) as cs
        from food_service_inspections
        where
        total_critical_violations + total_noncritical_violations > '""" + minViolations + """'
        AND
        date_of_inspection between '""" + start_date + """' AND '""" + end_date + """'
        AND
        violation_item IN (""" + licQuery + """)
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
    conn = psycopg2.connect("host='localhost' dbname='test5' user='test5' password='test5'")
    cursor = conn.cursor()
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




        
        