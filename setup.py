# setup of game/установка игры
from src.settings import * # импортируем настройки
from colorama import init, Fore, Back, Style # импортируем цветовую систему
import sys # система
from setuptools import setup # модуль для сетапа
from Cython.Build import cythonize # ситон(пайтон с расшерениями С)

init(autoreset=True)

# приветствие
def welcome():
    print(Fore.BLACK + Back.GREEN + Style.DIM + f'Welcome to {NAME} version {VERSION}') # печатаем черный текст на зеленом фоне


def go_or_no():
    print(f'Now you can install {NAME}') # поехали
    go = input('Go?[Y/n]') # поехали?
    if go == None or go == '':
        setup(
            ext_modules=cythonize("game.pyx"),
        ) # компилим

    elif go.lower() == 'y':
        setup(
            ext_modules=cythonize("game.pyx"),
        ) # компилим


    else:
        print('Ok, bye!')
        print(f'Exiting from {NAME}...')
        sys.exit()


welcome()
go_or_no()
