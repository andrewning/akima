#!/usr/bin/env python
# encoding: utf-8
"""
akima.py

Created by Andrew Ning on 2013-12-17.
"""

import _akima
import numpy as np


def akima_interp(xpt, ypt, x):
    """convenience method for those who don't want derivatives
    and don't want to evaluate the same spline multiple times"""

    p0, p1, p2, p3 = _akima.setup(xpt, ypt, delta_x=0.0)

    npt = len(xpt)
    zeros = np.zeros((npt-1, npt))

    y, dydx, dydxpt, dydypt = _akima.interp(x, xpt, p0, p1, p2, p3,
        zeros, zeros, zeros, zeros, zeros, zeros, zeros, zeros)

    return y



class Akima(object):
    """class for evaluating Akima spline and its derivatives"""


    def __init__(self, xpt, ypt, delta_x=0.1):
        """setup akima spline

        Parameters
        ----------
        xpt : array_like
            x discrete data points
        ypt : array_like
            x discrete data points
        delta_x : float, optional
            half-width of the smoothing interval added in the valley of absolute-value function
            this allows the derivatives with respect to the data points (dydxpt, dydypt)
            to also be C1 continuous.
            set to parameter to 0 to get the original Akima function (but only if
            you don't need dydxpt, dydypt)

        """

        xpt = np.array(xpt)
        ypt = np.array(ypt)

        self.xpt = xpt
        self.delta_x = delta_x

        n = len(xpt)
        xptd = np.vstack([np.eye(n), np.zeros((n, n))])
        yptd = np.vstack([np.zeros((n, n)), np.eye(n)])

        self.p0, p0d, self.p1, p1d, self.p2, p2d, self.p3, p3d = \
            _akima.setup_dv(xpt, xptd, ypt, yptd, delta_x=delta_x)
        self.dp0_dxpt = p0d[:n, :].T
        self.dp0_dypt = p0d[n:, :].T
        self.dp1_dxpt = p1d[:n, :].T
        self.dp1_dypt = p1d[n:, :].T
        self.dp2_dxpt = p2d[:n, :].T
        self.dp2_dypt = p2d[n:, :].T
        self.dp3_dxpt = p3d[:n, :].T
        self.dp3_dypt = p3d[n:, :].T





    def interp(self, x):
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
        dydx : nd_array
            the derivative of y w.r.t. x at each point
        dydxpt : 2D nd_array (only returned if delta_x != 0.0)
            dydxpt[i, j] the derivative of y[i] w.r.t. xpt[j]
        dydypt : 2D nd_array (only returned if delta_x != 0.0)
            dydypt[i, j] the derivative of y[i] w.r.t. ypt[j]

        """

        x = np.asarray(x)

        try:
            len(x)
            isFloat = False
        except TypeError:  # if x is just a float
            x = np.array([x])
            isFloat = True

        if x.size == 0:  # error check for empty array
            y = np.array([])
            dydx = np.array([])
            dydxpt = np.array([])
            dydypt = np.array([])
        else:
            y, dydx, dydxpt, dydypt = _akima.interp(x,
                self.xpt, self.p0, self.p1, self.p2, self.p3,
                self.dp0_dxpt, self.dp1_dxpt, self.dp2_dxpt, self.dp3_dxpt,
                self.dp0_dypt, self.dp1_dypt, self.dp2_dypt, self.dp3_dypt)

        if isFloat:
            y = y[0]
            dydx = dydx[0]
            dydxpt = dydxpt[0, :]
            dydypt = dydypt[0, :]

        if self.delta_x == 0.0:
            return y, dydx
        else:
            return y, dydx, dydxpt, dydypt
