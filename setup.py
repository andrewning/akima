# setup.py
# only if building in place: ``python setup.py build_ext --inplace``

from setuptools import setup
from numpy.distutils.core import setup, Extension


setup(
    name='akima',
    version='1.0.0',
    description='Akima spline interpolation (and derivatives)',
    author='S. Andrew Ning',
    package_dir={'': 'src'},
    py_modules=['akima'],
    license='Apache License, Version 2.0',
    ext_modules=[Extension('_akima', ['src/akima.f90'], extra_compile_args=['-O2'])]
)
