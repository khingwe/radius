# -*- coding: utf-8 -*-
"""
.. :module: MYSQL Wrapper
   :platform: Linux
   :synopsis: Distance module containing all distance related API's.
.. moduleauthor:: Kamlesh Hingwe <kkhingwe@gmail.com> (June 14, 2020)
"""
import json
import pymysql
import random
import math
import itertools

CONFIG = "config.json"
OULTINE = "table_column.json"

class MYSQLConnect(object):
    """
    Mysql conectivity
    """
    def __init__(self, dbname):
        with open(CONFIG, 'r') as f:
            conf = json.load(f)
        conf = conf.get('mysql')
        user = conf.get('user')
        password = conf.get('password')
        host = conf.get('host')
        self.client = pymysql.connect(user=user,
                                      password=password,
                                      host=host,
                                      port = 3306,
                                      db=dbname)

    def __del__(self):
        self.client.close()

    def insert_data(self, table, data):
        """
        Insert data in table
        @input: table name
                @data: dict contain columname: val
        @output: True if insert successfull else false
        """
        try:
            #import pdb; pdb.set_trace()
            if self.is_table_exist(table) is not True:
                self.create_table(table)
            columns = ', '.join(data.keys())
            values = ', '.join(str(x) for x in data.values())
            query = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table, columns, values)
            cursor = self.client.cursor()
            cursor.execute(query)
            self.client.commit()
            return True
        except Exception as e:
            raise e

    def get_data_dict(self, query, keys, isobj=False):
        """
        Query on mysql and return data in dict
        @input: query (in this query always contain id)
                keys contain list of key for dict
        @output: Returns the result in dictionary
        """
        query_resp = dict()
        cursor = self.client.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if isobj:
            return result
        for row in result:
            for x in range(len(keys)):
                if x is 0:
                    query_resp[row[x]] = {}
                else:
                    query_resp[row[0]][keys[x]] = row[x]
        return query_resp

    def is_table_exist(self, tablename):
        """
        Check Table exist or not
        @input: tablename table name to check
        @output: True if table exist else false
        """
        try:
            cursor = self.client.cursor()
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format(tablename.replace('\'', '\'\'')))
            if cursor.fetchone()[0] == 1:
                return True
            return False
        except Exception as ex:
            raise ex

    def create_table(self, tablename):
        """
        Create New table if table not exist
        @input: tablename to create table
        """
        try:
            cursor = self.client.cursor()
            with open(OULTINE, 'r') as f:
                conf = json.load(f)
            columns = conf.get(tablename, None)
            if columns is not None:
                query = "CREATE TABLE " + tablename + " (" + ', '.join(columns) + " )"
                cursor.execute(query)
                self.client.commit()
                return True
            else:
                return False
        except Exception as e:
            return False

    def get_id(self):
        """
        Get last inserted id of a table
        """
        try:
            cursor = self.client.cursor()
            query = "SELECT LAST_INSERT_ID()"
            cursor.execute(query)
            result = cursor.fetchone()[0]
            return result
        except Exception as ex:
            raise ex
'''
obj = MYSQLConnect("radius")

r = 0.5

x0 = 23.231662
y0 = 77.447403

for i in range(1,1):                 #Choose number of Lat Long to be generated

  u = float(random.uniform(0.0,1.0))
  v = float(random.uniform(0.0,1.0))
  #print(u,v, r)

  w = r * math.sqrt(u)
  t = 2 * math.pi * v
  x = w * math.cos(t)
  y = w * math.sin(t)
  #print(x,y)
  lat = format(x + x0, '.6f')
  long = format(y + y0, '.6f')
  data = {
  "latitude" : format(x + x0, '.6f'),
  "longitude" : format(y + y0, '.6f'),
  "min_budget" : random.randint(750, 1000),
  "max_budget" : random.randint(751, 3000),
  "min_bedrooms" : random.randint(1,2),
  "max_bedrooms" : random.randint(3,4),
  "min_bathrooms" : random.randint(1,2),
  "max_bathrooms" : random.randint(3,4)
  }
  obj.insert_data("requirements_testing",data)
  print(obj.get_id())
#obj.insert_data("requirements_testing", { "latitude": 23.123456, "longitude": 77.123456, "max_budget": 2000, "max_bedrooms": 3, "max_bathrooms": 3})
#print(obj.create_table("prop_req_assoc_test1"))
#obj.insert_data("properties", { "ID": 7, "latitude": 23.123456, "longitude": 77.123456, "price": 1000, "bedroom": 2, "bathroom": 2})
#print(obj.get_data_dict("SELECT * FROM properties", ['id','lat','long','room','bathroom']))
'''
