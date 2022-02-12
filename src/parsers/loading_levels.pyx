import pyximport # импоритурем Cython
pyximport.install() # инициализируем его
# файл для загрузки уровней.

def load_level(filename_e):
    '''парсер для 3агрузки'''
    poses = [] # список с позициями
    with open(filename_e) as f: # открываем файл с позициями врага
        for line in f: # читаем каждые линии в файле
            if line.startswith('# '): # если написали решётку(обычно это означает комментарий)
                pass # просто пропускаем действие
            else :
                poses.append(line) # добавляем в счписок позиций позицию очередного врага

    return poses # возвращаем позиции
