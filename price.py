# -*- coding: utf-8 -*-
"""
.. :module: Price Utils
   :platform: Linux
   :synopsis: Price module containing all Price related API's.
.. moduleauthor:: Kamlesh Hingwe <kkhingwe@gmail.com> (June 14, 2020)
"""

class Price(object):
    """
    Price class
    """
    def raw_point_price(self, price, max=None, min=None):
        """
        Raw Point calculations for Price
        if max and min present return 100 points
        if max is present cal calculate raw point with 1.5 factor(negative marking)
        if min is present cal calculate raw point with 1 factor
        @input : price , max and min budget
        @output: calculated raw points
        """
        try:
            points = 100
            if max is not None and min is not None and \
            price < max and price > min:
                return points
            if max is None:
                if(price < min):
                    return points
                else:
                    points = points - ((price - min) * 100) / min;
            elif min is None:
                if(price < max):
                    return points
                else:
                    points = points - (((price - max) * 100) / min) * 1.5;
            return points
        except Exception as ex:
            raise ex

    def get_price_range(self, min=None, max=None):
        """
        Get price range for perform query
        """
        if min is None and max is None:
            return None
        elif max is None:
            price_max = min + min * 25/100
            price_min = min - min * 25/100
        elif min is None:
            price_max = max + max * 25/100
            price_min = max - max * 25/100
        else:
            price_max = max + max * 25/100
            price_min = min - min * 25/100
        return price_min, price_max
