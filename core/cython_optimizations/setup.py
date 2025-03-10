from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize([
        "image_processing.pyx",
        "math_ops.pyx"
    ]),
    include_dirs=[numpy.get_include()]
)
