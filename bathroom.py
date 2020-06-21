# -*- coding: utf-8 -*-
"""
.. :module: Bathroom Utils
   :platform: Linux
   :synopsis: Bathroom module containing all Bathroom related API's.
.. moduleauthor:: Kamlesh Hingwe <kkhingwe@gmail.com> (June 14, 2020)
"""

class Bathroom(object):
    """
    Bathroom class
    """
    def raw_point_bed(self, no_bath, max=None, min=None):
        """
        Raw Point calculations for Bathroom
        """
        try:
            points = 100
            if no_bath < max and no_bath > min:
                return points
            if max is None:
                points = points - (abs(no_bath - min) * 20)
            elif min is None:
                points = points - (abs(no_bath - max) * 20)
            if points > 10:
                return points
            return points
        except Exception as ex:
            raise ex
