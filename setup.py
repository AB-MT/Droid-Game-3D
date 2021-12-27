# компиляция в C код
from setuptools import setup # модуль для сетапа
from Cython.Build import cythonize # ситон(пайтон с расшерениями С)

setup(
    ext_modules=cythonize("game.pyx"),
) # компилим
