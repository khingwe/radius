# -*- coding: utf-8 -*-
"""
.. :module: Agent APP
   :platform: Linux
   :synopsis: Agent module containing all agent related function.
.. moduleauthor:: Kamlesh Hingwe <kkhingwe@gmail.com> (June 21, 2020)
"""
from mysql import MYSQLConnect
from price import Price
from bedroom import Bedroom
from bathroom import Bathroom
from distance import Distance
from query_gen import MysqlQueryGen

PROP = ['ID','latitude', 'longitude', 'price',
        'bedroom', 'bathroom']
REQ = ['ID','latitude', 'longitude', 'min_budget',
       'max_budget', 'min_bedrooms', 'max_bedrooms',
       'min_bathrooms','max_bathrooms']

class RadiusAgent(object):
    """
    Class radius agent
    """

    def cal_match(self, distance, prop, req):
        """
        Calculate the match percentage
        """
        dist_obj = Distance()
        price_obj = Price()
        bath_obj = Bathroom()
        bed_obj = Bedroom()

        dist = dist_obj.raw_point_dist(distance) * 30/100
        price = price_obj.raw_point_price(prop.get("price"),
                                          max=req.get("max_budget", None),
                                          min=req.get("min_budget", None)) * 30/100
        bed = bed_obj.raw_point_bed(prop.get("bedroom"),
                                    max=req.get("max_bedrooms", None),
                                    min=req.get("min_bedrooms", None)) * 20/100
        bath = bed_obj.raw_point_bed(prop.get("bathroom"),
                                     max=req.get("max_bathrooms", None),
                                     min=req.get("min_bathrooms", None)) * 20/100

        print(distance, prop, req)
        print(dist, price,bed,bath)
        return dist + price + bed + bath

    def get_data(self, table_name, id):
        """
        getting the requirement from as argument
        @input: data a dict related to rquirement
        """
        try:
            query_table = ""
            mysql_obj = MYSQLConnect('radius')
            columns = ""
            final_list = list()
            if table_name == "requirements_testing":
                query_table = "properties"
                q_columns = PROP
                columns = ["prop_id","match_per"]
                col = "prop_id, match_per"
                q_col = ','.join(q_columns)
                query = "SELECT {0} from prop_req_assoc_test1 WHERE req_id = {1}".format(col, id)
            elif table_name == "properties":
                query_table = "requirements_testing"
                columns = ["req_id","match_per"]
                col = "req_id, match_per"
                q_columns = REQ
                q_col = ','.join(q_columns)
                query = "SELECT {0} from prop_req_assoc_t WHERE prop_id = {1}".format(col, id)
            query_resp = mysql_obj.get_data_dict(query,columns, isobj=True)
            for row in query_resp:
                _id = row[0]
                match_per = row[1]
                import pdb; pdb.set_trace()
                query = "SELECT {0} from {1} WHERE ID = {2}".format(q_col,
                                                                    query_table,
                                                                    _id)
                resp = mysql_obj.get_data_dict(query,q_columns)
                key = resp.keys()[0]
                resp[key]['match_per'] = match_per
                final_list.append(resp)
            return final_list
        except Exception as e:
            raise e


    def update_property_db(self, data):
        """
        Update the mysql db for property
        @input: data a dict related to property
        @output: If success return updated ID with DBNAME else None
        """
        mysql_obj = MYSQLConnect()
        if mysql_obj.insert_data("properties", data):
            return "properties", mysql_obj.get_id()
        return None

    def update_requirment_db(self, data):
        """
        Update the mysql db for requirmentdb
        @input: data a dict related to requirement
        @output: If success return updated ID with DBNAME else None
        """
        try:
            mysql_obj = MYSQLConnect()
            if mysql_obj.insert_data("requirements_testing", data):
                return "requirements_testing", mysql_obj.get_id()
            return None
        except Exception as ex:
            raise ex


    def generate_mapping(self, table, id):
        """
        Generate Mapping for requirement to property and store to other DB
        @input: table - mysql table name for which input
                id- primary key for input table
        @output: True if all updates successful else will raise exception
        """
        try:
            mysql_obj = MYSQLConnect('radius')
            dist_obj = Distance()
            budget = Price()
            query_gen = MysqlQueryGen()
            import pdb; pdb.set_trace()
            if table == "properties":
                columns = PROP
                col = ','.join(columns)
                get_query = "SELECT {0} from properties WHERE ID = {1}".format(col, id)
                query_resp = mysql_obj.get_data_dict(get_query,columns)
                lat, long = dist_obj.get_range(query_resp[id].get("latitude"),
                                               query_resp[id].get("longitude"))
                budget_range = budget.get_price_range(query_resp[id].get("price"))
                query = query_gen.get_requirements(lat, long, budget_range)
                columns = REQ
                resp = mysql_obj.get_data_dict(query, columns)
                source = (query_resp[id].get("latitude"),
                          query_resp[id].get("longitude"))
                for _id in resp.keys():
                    dest = (resp[_id].get('latitude'),
                            resp[_id].get('longitude'))
                    distance = dist_obj.find_distance(source, dest)
                    if distance <= 10:
                        match = self.cal_match(distance, query_resp[id],resp[_id])
                        data = {
                            "prop_id": id,
                            "req_id": _id,
                            "match_per": int(match)
                        }
                        try:
                            assert mysql_obj.insert_data("prop_req_assoc_t",data)
                        except Exception as e:
                            print("Insertion Failed")
                        print(distance)
                print(resp)
            elif table == "requirements_testing":
                import pdb; pdb.set_trace()
                columns = REQ
                col = ','.join(columns)
                get_query = "SELECT {0} from requirements_testing WHERE ID = {1}".format(col, id)
                req_resp = mysql_obj.get_data_dict(get_query,columns)
                lat, long = dist_obj.get_range(req_resp[id].get("latitude"),
                                               req_resp[id].get("longitude"))
                budget_range = budget.get_price_range(min=req_resp[id].get("min_budget"),
                                                      max=req_resp[id].get("max_budget"))
                query = query_gen.get_property(lat, long, budget_range)
                columns = PROP
                prop_resp = mysql_obj.get_data_dict(query, columns)
                source = (req_resp[id].get("latitude"),
                          req_resp[id].get("longitude"))
                for _id in prop_resp.keys():
                    dest = (prop_resp[_id].get('latitude'),
                            prop_resp[_id].get('longitude'))
                    distance = dist_obj.find_distance(source,dest)
                    if distance <= 10:
                        match = self.cal_match(distance, prop_resp[_id],req_resp[id])
                        data = {
                            "prop_id": _id,
                            "req_id": id,
                            "match_per": int(match)
                        }
                        try:
                            assert mysql_obj.insert_data("prop_req_assoc_t",data)
                        except Exception as e:
                            print("Insertion Failed")

                        print(distance)
                print(prop_resp)
                return True
        except Exception as e:
            raise e
