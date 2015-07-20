# Akima with Derivatives

1-Dimensional Akima spline implementation [1] with derivatives not only of the function, but also with respect to the original data points.  An Akima spline is a polynomial spline method that avoids overshooting issues common with many other splines (e.g., cubic splines), resulting in a more natural curve.  I find Akima splines to be particularly useful in optimization applications for defining distributions of design variables at a small number of points.  This type of spline more readily permits using bound constraints directly on the design variables, without worrying about excessive overshooting between them.

Apparently, [many implementations](http://stackoverflow.com/questions/3502769/akima-interpolation-of-an-array-of-doubles/4637884#4637884) for Akima splines already exist in a variety of languages.  But, I needed a version that returned analytic derivatives in addition to function values.  Computing analytic derivatives with respect to the function argument is straightforward, but I also needed derivatives of the function with respect to the original data points.  While the Akima formulation produces a  continuous curve, the derivatives with respect to the data points are actually not continuous due to the existence of an absolute value function.  This formulation replaces the absolute value function with a "smooth absolute value" function, in which the bottom of the valley is rounded off using a quadratic function.  The user may specify the half-width (``delta_x``) of this rounded section (defaults to 0.1).  In practice, a small delta_x produces only a very slight deviation from the original Akima (while still passing through all the data points exactly).  In exchange, the derivatives with respect to the original data points can be provided.  If these extra gradients are not needed (i.e., only function values and derivatives with respect to the function argument are needed), setting ``delta_x = 0`` produces the original Akima exactly.

This implementation separates the construction of the spline from the evaluation.  If the spline is evaluated at lots of different conditions, this adds some computational efficiency.  The code is written in Fortran and is also made available to Python as a extension.  A small wrapper was added around the extension (akima.py) to make its use more Pythonic.  Derivatives of the spline coefficients are computed via automatic differentiation using Tapenade, derivatives of the spline evaluation are straightforward and derived by hand.  The methodology is only defined for interpolation; however, if you specify a value outside the original bounds the current implementation will still work.  For out of bounds cases, the implementation just uses the polynomial definition for the nearest end section.  This will allow for a smooth continuation of the function value outside of the bounds, but using this for extrapolation (beyond very small extensions) is highly suspect.

[1]: Akima, H. (1970). A New Method of Interpolation and Smooth Curve Fitting Based on Local Procedures. Journal of the ACM, 17(4), 589-602. Association for Computing Machinery. [doi:10.1145/321607.321609](http:dx.doi.org/10.1145/321607.321609)

## Prerequisites

NumPy, Fortran compiler

## Installation

    $ python setup.py install

See example.py for Python usage and akima.py for the docstrings.  Refer to akima.f90 for direct Fortran usage.

