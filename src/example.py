#!/usr/bin/env python
# encoding: utf-8
"""
example.py

Created by Andrew Ning on 2013-12-17.
"""

import numpy as np
from akima import Akima

# setup spline based on fixed points
xpt = np.array([1.0, 2.0, 4.0, 6.0, 10.0, 12.0])
ypt = np.array([5.0, 12.0, 14.0, 16.0, 21.0, 29.0])
spline = Akima(xpt, ypt)

# interpolate  (extrapolation will work, but beware the results may be silly)
n = 50
x = np.linspace(0.0, 13.0, n)
y, dydx, dydxpt, dydypt = spline.interp(x)

# compare derivatives w.r.t. x to finite differencing
xstep = x + 1e-6  # can do all steps at same time b.c. they are independent
ystep, _, _, _ = spline.interp(xstep)
fd = (ystep - y)/1e-6


import matplotlib.pyplot as plt
plt.plot(xpt, ypt, 'o')
plt.plot(x, y, '-')

plt.figure()
plt.plot(x, dydx)
plt.plot(x, fd)
plt.show()
