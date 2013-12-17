# Akima

1-Dimensional Akima spline implementation [1].  A polynomial spline method that avoids overshooting issues that are common with cubic spline methods, resulting in a more natural curve.  I find Akima splines to be particularly useful in optimization applications for defining distributions of design variables at a small number of points.  

Apparently, [many implementations](http://stackoverflow.com/questions/3502769/akima-interpolation-of-an-array-of-doubles/4637884#4637884) already exist in a variety of languages.  But, I wanted a version that also returned derivatives in addition to function values.  This implementation also separates the construction of the spline from the evaluation.  If the spline is evaluated at lots of different conditions, this adds some computational efficiency.

The code was written in Fortran and is also made available to Python as a extension.  A small wrapper was added around the extension (akima.py) to make its use more Pythonic.  The methodology is only defined for interpolation; however, if you specify a value outside the original bounds the current implementation will still work.  For out of bounds cases, the implementation just uses the polynomial definition for the nearest end section.  This will allow for a smooth continuation of the function value outside of the bounds, but using this for extrapolation (beyond very small extensions) is highly suspect.

[1]: Akima, H. (1970). A New Method of Interpolation and Smooth Curve Fitting Based on Local Procedures. Journal of the ACM, 17(4), 589-602. Association for Computing Machinery. [doi:10.1145/321607.321609](http:dx.doi.org/10.1145/321607.321609)

## Prerequisites

NumPy, Fortran compiler

## Installation

    $ python setup.py install

See example.py for Python usage and akima.py for the docstrings.  Refer to akima.f90 for direct Fortran usage.

