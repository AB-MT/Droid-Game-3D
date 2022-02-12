# Скрипт для установки уровней/Script for downloading levels
import pyximport # импоритурем Cython
pyximport.install() # инициализируем его
import os # импортируем модуль для использования терминала

# функция скачивания уровней(ня)
def downloading():
    repesitory = input('Github репозиторий(Github Repository) : ') # справшиваем репезиторий с уровнями с github.com
    os.system('git clone ' + repesitory) # скачиваем уровни

# если заупускают из этого файла, выполняем функцию скачивания
if __name__ == '__main__':
    downloading() # скачиваем
