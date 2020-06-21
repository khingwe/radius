# -*- coding: utf-8 -*-
"""
.. :module: Bedroom Utils
   :platform: Linux
   :synopsis: Bedroom module containing all Bedroom related API's.
.. moduleauthor:: Kamlesh Hingwe <kkhingwe@gmail.com> (June 14, 2020)
"""

class Bedroom(object):
    """
    Bedroom class
    """
    def raw_point_bed(self, no_bed, max=None, min=None):
        """
        Raw Point calculations for bedroom
        """
        try:
            points = 100
            if no_bed < max and no_bed > min:
                return points
            if max is None:
                points = points - (abs(no_bed - min) * 25)
            elif min is None:
                points = points - (abs(no_bed - max) * 25)
            if points > 10:
                return points
            return points
        except Exception as ex:
            raise ex
