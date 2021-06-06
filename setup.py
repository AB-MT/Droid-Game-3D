# запуск с оптимизацией
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("game.pyx"),
) # запускаем игру
