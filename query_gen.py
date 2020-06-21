# -*- coding: utf-8 -*-
"""
.. :module: Query Generator
   :platform: Linux
   :synopsis: Query Generator module contains queries for MySQL
.. moduleauthor:: Kamlesh Hingwe <kkhingwe@gmail.com> (June 14, 2020)
"""

#from distance import Distance

class MysqlQueryGen(object):
    """
    Class for generate mysql queries
    """

    def get_property(self, latitude, longitude, price):
        """
        """
        sel_clause = "SELECT * from properties"
        lat_cond = "(latitude BETWEEN {0} AND {1}) ".format(*latitude)
        long_cond = "AND (longitude BETWEEN {0} AND {1}) ".format(*longitude)
        budget_cond = "AND (price BETWEEN {0} AND {1}) ".format(*price)
        query = sel_clause + " WHERE " + lat_cond + long_cond + budget_cond
        return query

    def get_requirements(self, latitude, longitude, price):
        """
        """
        sel_clause = "SELECT * from requirements_testing"
        lat_cond = "(latitude BETWEEN {0} AND {1}) ".format(*latitude)
        long_cond = "AND (longitude BETWEEN {0} AND {1}) ".format(*longitude)
        budget_cond = "AND ((min_budget BETWEEN {0} AND {1}) OR "\
        "(max_budget BETWEEN {0} AND {1}) OR (min_budget >= {0} AND "\
        "max_budget <={1}))".format(*price)
        query = sel_clause + " WHERE " + lat_cond + long_cond + budget_cond
        return query

'''
obj = MysqlQueryGen()
print(obj.get_property((23,24), (76,77),(1000,2000)))
print(obj.get_requirements((23,24), (76,77),(1000,2000)))
'''
