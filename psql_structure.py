# Keeping this class here for now (easy to test). Will move this to a separate .py file when we do code-cleanup/ submission

import psycopg2
import psycopg2.extras
import re
import pandas


class FoodViolationData:

    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
	
    def directQuery(self, query):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return pandas.DataFrame(cursor.fetchall())

    class FoodViolationQuery:

        def __init__(self, product_data):
            self.joins = []
            self.conditions = []
            self.parameters = {}
            self.product_data = product_data

            self.named_params = {}

        def __param_index(self, param_name):

            if param_name not in self.named_params:
                self.named_params.update({param_name: 0})
                return 0
            else:
                i = self.named_params[param_name] + 1
                self.named_params.update({param_name: i})
                return i

        def max_calories(self, max_calories):
            self.conditions.append("products.calories_100g <= %(max_calories)s")
            self.parameters.update({"max_calories": max_calories})
            return self

        def max_sugar(self, max_sugar):
            self.conditions.append("products.sugars_100g <= %(max_sugar)s")
            self.parameters.update({"max_sugar": max_sugar})
            return self

        def ingredient(self, ingredient):
            i = str(self.__param_index("ingredient"))
            self.joins.append(
                "JOIN product_ingredient as product_ingredient" + i + " on products.code = product_ingredient" + i + ".product JOIN ingredients as ingredients" + i + " on ingredients" + i + ".name = product_ingredient" + i + ".ingredient")
            self.conditions.append("LOWER(ingredients" + i + ".name) like LOWER(%(ingredient" + i + ")s)")
            self.parameters.update({"ingredient" + i: "%" + ingredient + "%"})
            return self

        def brand(self, brand):
            i = str(self.__param_index("brand"))
            self.conditions.append("LOWER(brands) like LOWER(%(brand" + i + ")s)")
            self.parameters.update({"brand" + i: "%" + brand + "%"})
            return self

        def category(self, category):
            i = str(self.__param_index("category"))
            self.joins.append(
                "JOIN product_category as product_category" + i + " on products.code = product_category" + i + ".product JOIN categories as categories" + i + " on categories" + i + ".name = product_category" + i + ".category")
            self.conditions.append("LOWER(categories" + i + ".name) like LOWER(%(category" + i + ")s)")
            self.parameters.update({"category" + i: "%" + category + "%"})
            return self

        def name(self, name):
            self.conditions.append("LOWER(products.name) like LOWER(%(name)s)")
            self.parameters.update({"name": name})
            return self
        
        def searchByCounty(self, name):
            i = str(self.__param_index("county"))
            
            self.conditions.append(""" "county" like %(county""" + i + ")s")
            #print(i)
            #print(name)
            #self.conditions.append(""" "COUNTY" like '%%""" + name + """%%' """)
            #print(self.conditions)
            self.parameters.update({"county" + i: "%" + name + "%"})
            #print(self.parameters)
            return self

        def searchByOperatorID(self, health_opID):
            i = str(self.__param_index("health_operation_id"))
            self.conditions.append(""" "nys_health_operation_id" = %(health_operation_id""" + i + ")s")
            #print(i)
            #print(name)
            #self.conditions.append(""" "COUNTY" like '%%""" + name + """%%' """)
            #print(self.conditions)
            self.parameters.update({"health_operation_id" + i: health_opID})
            #print(self.parameters)
            return self
        
        def searchByName(self, name):
            #query = """ select * from food_service_inspections JOIN food_service_operator_distinct on food_service_inspections."NYS HEALTH OPERATION ID" = food_service_operator_distinct."NYS HEALTH OPERATION ID" where "COUNTY" like '%%ALB%%' """
            i = str(self.__param_index("name"))
            self.joins.append(
                "JOIN food_service_operator as food_operator" + i + """ on food_service_inspections."nys_health_operation_id" = food_operator""" + i + """."nys_health_operation_id" """)
            self.conditions.append("food_operator" + i + """."operation_name" like %(name""" + i + ")s")
            self.parameters.update({"name" + i: "%" + name + "%"})
            return self
        '''
            print(query)
            with self.product_data.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                #print(query)
                cursor.execute(query, self.parameters)
                return pandas.DataFrame(cursor.fetchall())
            return self
        '''
        def getAllViolations(self):
            query = """select * from food_service_violations order by violation_item"""
            with self.product_data.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                #print(query)
                cursor.execute(query, self.parameters)
                return pandas.DataFrame(cursor.fetchall())
            return self

        def __compile(self):
            query = "SELECT DISTINCT * from food_service_inspections"
            query = query + " " + " ".join(self.joins) if self.joins else query
            query = query + " WHERE " + " AND ".join(self.conditions) if self.conditions else query
            #query += " ORDER BY food_service_inspections.code"
            return query

        def run(self):
            query = self.__compile()
            #query = """select * from food_service_inspections where "COUNTY" like 'ALB%%' limit 3"""
            with self.product_data.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                print(query)
                cursor.execute(query, self.parameters)
                return pandas.DataFrame(cursor.fetchall())

        def show(self):
            query = self.__compile()
            with self.product_data.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                return cursor.mogrify(query, self.parameters)

    def query(self):
        return self.FoodViolationQuery(self)