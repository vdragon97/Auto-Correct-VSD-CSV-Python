from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("autoCorrectCSV",  ["autoCorrectCSV.py"]),

#   ... all your modules that need be compiled ...
#   https://docs.python.org/2/extending/building.html
]

setup(
    name = 'Auto Correct CSV File',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)