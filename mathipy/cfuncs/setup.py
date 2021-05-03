from distutils.core import setup, Extension
from Cython.Build import cythonize

cython_utils_dir = 'src/c/cython_utils.c'
trig = Extension(
                name='trigonometry',
                sources=['src/pyx/trigonometry.pyx', cython_utils_dir],
                )

exp = Extension(
                name='exponential',
                sources=['src/pyx/exponential.pyx', cython_utils_dir]
                )

setup(ext_modules=cythonize([trig, exp]))
