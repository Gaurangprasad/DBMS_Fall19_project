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
        if(int(parser['query']) == 1 ):
            county = input('Enter county: ')
            query = """ select premise_name,doing_business_as,address,zipcode, license_type_name from liquor_license, license_types
    where county ilike '""" + county + """' AND
    liquor_license.license_type_code = license_types.license_type_code
    AND
    license_types.license_type_code IN ('D','MI','CF') """
            # Looking for estabishments that have the word BUFFET in their name and are in ALBANY
            print(fd_vio.directQuery(query))

        
        