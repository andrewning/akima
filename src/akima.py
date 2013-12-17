#!/usr/bin/env python
# encoding: utf-8
"""
akima.py

Created by Andrew Ning on 2013-12-17.
"""

import _akima
import numpy as np


class Akima(object):


    def __init__(self, xpt, ypt):
        """setup akima spline

        Parameters
        ----------
        xpt : array_like
            x discrete data points
        ypt : array_like
            x discrete data points

        """

        xpt = np.array(xpt)
        ypt = np.array(ypt)

        self.p0, self.p1, self.p2, self.p3 = _akima.setup(xpt, ypt)
        self.xpt = xpt


    def interp(self, x, derivatives=False):
        """interpolate at new values

        Parameters
        ----------
        x : array_like
            x values to sample spline at
        derivatives : boolean (optional)
            True if you want to return derivatives (dydx) in addition to function values

        Returns
        -------
        y : nd_array
            interpolated values y = fspline(x)
        dydx : nd_array (only returned if derivatives=True)
            the derivative of y w.r.t. x at each point

        """

        x = np.array(x)
        y, dydx = _akima.interp(self.xpt, self.p0, self.p1, self.p2, self.p3, x)

        if derivatives:
            return y, dydx
        else:
            return y
