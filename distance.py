# -*- coding: utf-8 -*-
"""
.. :module: distance api's
   :platform: Linux
   :synopsis: Distance module containing all distance related API's.
.. moduleauthor:: Kamlesh Hingwe <kkhingwe@gmail.com> (June 14, 2020)
"""

import math

EARTH_RADIUS =  3958.8
class Distance(object):
    """
    Distance  Class
    """

    def find_distance(self, source, destination):
        """
        Calculate the distance between two coredinates
        coredinates are in lattitude and longitude
        @input: source a tuple of lattitude and longitude
                destination a tuple of lattitude and longitude
        @output: distance in miles
        """
        try:
            source_lat = math.radians(source[0])
            source_long = math.radians(source[1])
            dest_lat = math.radians(destination[0])
            dest_long = math.radians(destination[1])

            dist_lat = dest_lat - source_lat
            dist_long = dest_long - source_long

            a = math.sin(dist_lat / 2)**2 + math.cos(source_lat) * \
                math.cos(dest_lat) * math.sin(dist_long / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = EARTH_RADIUS * c
            return distance
        except Exception as ex:
            raise ex

    def get_range(self, lat, long):
        """
        Get the range for query
        """
        try:
            max_lat = format(lat + 0.15, '.6f')
            min_lat = format(lat - 0.15, '.6f')
            max_long = format(long + 0.17, '.6f')
            min_long = format(long - 0.17, '.6f')
            lat_range = (min_lat, max_lat)
            long_range = (min_long, max_long)
            if max_lat < min_lat:
                lat_range = (max_lat, min_lat)
            if max_long < min_long:
                long_range = (max_long, min_long)
            return lat_range, long_range
        except Exception as ex:
            raise ex

    def raw_point_dist(self, distance):
        """
        Calculate Raw Points
        """
        point = 100;
        if distance <= 2:
            return point;
        else:
            point = point - ((distance - 2) * 10);
        return point
