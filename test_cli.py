# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 23:25:40 2019

@author: GaurangPrasadML
"""
import warnings
import argparse
import itertools
from psql_structure import FoodViolationData
from psql_interface import PSQLInterfaceClass
from json_structure import InsuranceData
import psycopg2
import psycopg2.extras
import pandas
from datetime import datetime
from tabulate import tabulate

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
    
def validateYear(inputYearString):
    if(validateInteger(inputYearString) == False):
        return False
    else:
        if(int(inputYearString) < 0):
            print("Enter valid year.")
            return False
        else:
            return True

def query1():
    # Basic join and using IN operator
    print("1. Where can I get some alcohol around me?")
    print("Search for liquor stores in a specific county and by specific liquor license(s)")
    print()
    county = input('Enter county: ')
    viewAllCode = input('Do you want to see the list of all liquor license codes? Enter True or False: ')
    if(viewAllCode.casefold() == "true"):
        print(tabulate(psql_interface.viewAllLiquorCodes(), headers=["License Type Code","License Class Code","License Type Name"], tablefmt='fancy_grid'))
    print()
    license_string = input('Enter license codes separated by a space: ')
    # Sample values for breweries - 'D','MI','CF'
    lic_arr = license_string.upper().split()
    params = (county, tuple(lic_arr))
    outputDF = psql_interface.query1(params)
    
    print(tabulate(outputDF, headers=["Premise Name","Also Advertised As","Address","ZipCode", "License Type" ], tablefmt='fancy_grid'))

def query2():
    print("2. Food operators that are permitted to serve alcohol and have food service violations")
    print("Search for food operators in a specific county that hold a liquor license and have food service violations in a specific date range.")
    print()
    print("Provide date range (start date, end date)")
    start_date = input('Enter start date (YYYY-MM-DD): ')
    if(validate(start_date) == False):
        print("Invalid date")
        return
    end_date = input('Enter end date (YYYY-MM-DD): ')
    if(validate(end_date) == False):
        print("Invalid date")
        return
    county = input('Enter county: ')
    params = (start_date, end_date, county)
    outputDF = psql_interface.query2(params)
    print()
    print()
    # Standard pandas DF output looks way better than the tabulate for this
    print(outputDF)



def query3():
    start_date = input('Enter start date (YYYY-MM-DD):')
    if(validate(start_date) == False):
        print("Invalid date")
        return
    end_date = input('Enter end date (YYYY-MM-DD):')
    if(validate(end_date) == False):
        print("Invalid date")
        return

    yearOfArrest = input('Adult Arrests Year: ')
    if(validateYear(yearOfArrest) == False):
        return
    
    minViolations = input('Minimum number of Violations: ')
    if(validateInteger(minViolations) == False):
        return
    
    viewAllCode = input('Do you want to see all types of food violations? Enter True or False ')
    
    print()
    print()
    print()
    if(viewAllCode.casefold() == "true"):
        print(tabulate(psql_interface.viewAllFoodViolations(), headers=["Index","Violation Code", "Violation Description" ]))
    print()
    
    license_string = input('Enter violation codes separated by a space: ')
    lic_arr = license_string.upper().split()
    
    #  '14A','12E','1B','8F','3B','23','62'
    params = (minViolations, start_date, end_date, tuple(lic_arr), yearOfArrest)
    
    outputDF = psql_interface.query3(params)
    print()
    print()
    print(tabulate(outputDF, headers=["County","Total Violations", "Property Misdemeanors" ], tablefmt='fancy_grid'))


def query4():
    outputDF = psql_interface.query4()
    # Pretty printing
    print(tabulate(outputDF, headers=["County","Operation Name", "NYS ID", "Total Violations"], tablefmt='fancy_grid'))

    
def query5():

    searchRegionType = input("Do you wanna search by county (ex: Albany) or region (ex: Capital Region)? Enter 'county' or 'region': ")
    
    # Using Mongo interface to create a query string that we can eval() later
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
    if(validateYear(year) == False):
        return
    else:
        year = int(year)
       
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
    
def query6():
    county = input("Enter county: ")
    year = input("Enter year: ")
    if(validateYear(year) == False):
        return
    else:
        year = int(year)
    params = (county, year)
    adultArrestDF =  psql_interface.query6(params)
    jsonDF = ins.query().county(county).year(year).run()
    jsonDF = jsonDF.groupby(['County'])['County', 'Beneficiaries', 'Benefits'].sum()
    #combinedDF = adultArrdf.assign(Beneficiaries = [jsonDF.loc])
    #print( jsonDF['Beneficiaries'])
    #combinedDF = adultArrdf.assign(Beneficiaries = [jsonDF['Beneficiaries']])
    #adultArrdf['Total Num. of Beneficiaries'] = jsonDF['Beneficiaries']
    #adultArrdf['Total Benefits'] = jsonDF.loc[jsonDF['County'] == adultArrdf['0']]['Benefits']
    #print(adultArrdf.head())
    #print(jsonDF)
    print(adultArrestDF)
    print(jsonDF)


if __name__ == "__main__":
    
    # Handling command line arguments
    arg = argparse.ArgumentParser()
    conn = psycopg2.connect("host='localhost' dbname='test5' user='test5' password='test5'")
    cursor = conn.cursor()
    #fd_vio = FoodViolationData("host='localhost' dbname='test5' user='test5' password='test5'")
    psql_interface = PSQLInterfaceClass("host='localhost' dbname='test5' user='test5' password='test5'")
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
        print("1. Where can I get some alcohol around me?")
        print("2. Which pubs have received food service violations?")
        print("3. Is there a relation between bad food and property misdemeanor?")
        print("4. Who consistently causes 3am tummy aches?")
        print("5. Explore unemployment around you.")

    
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
        elif(queryNumber == 5):
            query5()
        elif(queryNumber == 6):
            query6()
        else:
            print('Invalid Query. Use --view True argument to view the queries supported by the application.')




        
        