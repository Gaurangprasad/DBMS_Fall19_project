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
from datetime import datetime

# https://stackoverflow.com/a/37045601/4759033
def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def validateInteger(inputIntString):
    try:
        inputIntString = int(inputIntString)
        return True
    except ValueError:
        print("^ Not an Integer value.")
        return False
    

def query1():
    county = input('Enter county: ')
    license_string = input('Enter license codes separated by a space: ')
    lic_arr = license_string.split()
    query = """select premise_name,doing_business_as,address,zipcode, license_type_name from liquor_license, license_types where county ilike %s AND liquor_license.license_type_code = license_types.license_type_code AND license_types.license_type_code IN %s"""
    cursor.execute(query, (county, tuple(lic_arr)))
    print(pandas.DataFrame(cursor.fetchall()))

def query2():
    start_date = input('Enter start date (DD/MM/YYYY):')
    if(validate(start_date) == False):
        print("Invalid date")
        return
    end_date = input('Enter end date (DD/MM/YYYY):')
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
                        food_service_inspections.date_of_inspection >= %s AND
                            food_service_inspections.date_of_inspection <= %s
                        AND
                        food_service_violations.violation_item = food_service_inspections.violation_item
                        """
    cursor.execute(query, (start_date, end_date))
    print(pandas.DataFrame(cursor.fetchall()))

def query3():
    start_date = input('Enter start date (DD/MM/YYYY):')
    if(validate(start_date) == False):
        print("Invalid date")
        return
    end_date = input('Enter end date (DD/MM/YYYY):')
    if(validate(end_date) == False):
        print("Invalid date")
        return

    yearOfArrest = input('Adult Arrests Year: ')
    if(validateInteger(yearOfArrest) == False):
        return
    
    minViolations = input('Min Violations: ')
    if(validateInteger(minViolations) == False):
        return
    
    license_string = input('Enter violation codes separated by a space: ')
    lic_arr = license_string.split()
    
    #  '14A','12E','1B','8F','3B','23','62'
    query = """
        select csm.county, cs, property_misdemanors  from (select county,sum(total_critical_violations+ total_critical_violations) as cs
        from food_service_inspections
        where
        total_critical_violations + total_noncritical_violations > %s
        AND
        date_of_inspection between %s AND %s
        AND
        violation_item IN (%s)
        GROUP BY county) as csm, (select county, sum(property_misdemeanor) as property_misdemanors from adult_arrests
        where year = %s
        group by county
        ) as ad
        where upper(csm.county) = upper(ad.county)
        """

    cursor.execute(query, (minViolations, start_date, end_date, tuple(lic_arr), yearOfArrest))
    print(pandas.DataFrame(cursor.fetchall()))

def query4():

    searchRegionType = input("Do you wanna search by county (ex: Albany) or region (ex: Capital Region)? Enter 'county' or 'region': ")
    baseQuery = "ins.query()"
    if(searchRegionType.casefold() == "county"):
        baseQuery = baseQuery + ".county("
    elif(searchRegionType.casefold() == "region"):
        baseQuery = baseQuery + ".region("
    else:
        print("Invalid Entry")
        return
    print()
    regionVal = input("Enter " + searchRegionType + " to search: ")
    baseQuery = baseQuery + "'{}')"
            
    year = input("Enter year: ")
    if(validateInteger(year) == False):
        return
    else:
        year = int(year)
        if year < 1:
            print('Invalid year')
            return
        elif year > 2019:
            print('Invalid year')
            return
    baseQuery = baseQuery + ".year({})"
    
    month = input("Enter month number: ")
    if(validateInteger(month) == False):
        return
    else:
        month = int(month)
        if month < 1:
            print('Invalid month')
            return
        elif month > 12:
            print('Invalid month')
            return

    baseQuery = baseQuery + ".month({})"
        
    baseQuery = baseQuery + ".run()"
    print()
    print()
    print(eval(baseQuery.format(regionVal, year, month)))


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
        print("2. Does something")
        print("3. Something else")
    
    if(parser['query'] is not None):
        queryNumber = int(parser['query'])
        if(queryNumber == 1 ):
            query1()
        elif(queryNumber == 2):
            query2()
        elif(queryNumber == 3):
            query3()
        elif(queryNumber == 4):
            query4()
        else:
            print('Invalid Query. Use --view True argument to view the queries supported by the application.')




        
        