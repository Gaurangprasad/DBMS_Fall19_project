from pymongo import MongoClient
import re
import pandas


class InsuranceData:

    def __init__(self, host='localhost', port=27017, db="dbms", collection="insuranceBeneficiaries"):
        self.client = MongoClient(host, port)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def is_connected(self):
        return True if self.client else None

    class InsuranceQuery:

        def __init__(self, insurance):
            self.insurance = insurance
            self.query = {}

        def county(self, text):
            self.query.update({"County": re.compile(text, re.IGNORECASE)})
            return self

        def region(self, category):
            self.query.update({"Region": re.compile(category, re.IGNORECASE)})
            return self

        def max_year(self, max_year):
            self.query.update({"Year": {"$lte": max_year}})
            return self
        
        def min_year(self, min_year):
            self.query.update({"Year": {"$gte": min_year}})
            return self
        
        def year(self, year):
            self.query.update({"Year": year})
            return self
        
        def month(self, month):
            self.query.update({"Month": month})
            return self
        
        def max_month(self, max_month):
            self.query.update({"Month": {"$lte": max_month}})
            return self
        
        def min_month(self, min_month):
            self.query.update({"Month": {"$gte": min_month}})
            return self

        def run(self):
            df = pandas.DataFrame(list(self.insurance.collection.find(self.query)))
            return df.loc[:, df.columns != '_id']

        def show(self):
            return self.query

    def query(self):
        return self.InsuranceQuery(self)