
# Боты
import pyximport # импоритурем Cython
pyximport.install() # инициализируем его
import random


def bot(enemy, dt):
    # по разному...
    if random.randrange(0, 1):
        enemy.setX(enemy, 1 * dt ) # перемещаем врага

    return enemy.getPos() # возвращаем позицию врага
