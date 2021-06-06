import PySimpleGUI as sg

# интерфейс окна. Посмтрите, как легко его сделать с помощью инструмента  PySimpleGUI!
layout_direction = [
    [sg.Text('----МЕНЮ----')],
    [sg.Text('Esc - закрыть окно, выйти/Close window, exit')],
    [sg.Text('----ИГРА----')],
    [sg.Text('Esc - закрыть игру, открыть меню/Close game, open menu')],
    [sg.Text('Left Button - повернуть дроид в лево/turn droid left')],
    [sg.Text('Right Button - повернуть дроид в право.turn droid right')],
    [sg.Text('A - повернуть камеру в лево/turn camera left')],
    [sg.Text('D - повернуть камеру в право/turn camera right')],
    [sg.Text('Space - выстрел/shot')],
    [sg.Text('S - достать фонарик/get a flashlight')],
    [sg.Text('W - убрать оружие/remove weapon')],
    [sg.Text('P - показаь прицел/show sight')],
    [sg.Text('G - кинуть гранату/throw a grenade')],
    [sg.Text('F - полный разгон двигателя корабля/full acceleration of the engine')],
    [sg.Text('0 - огнетушительная система/fire extinguishing system')],
    [sg.Text('F3 - полигольный режим/polygons mode')],
    [sg.Text('R - режим RPG/RPG Mode')]

    ]

# главный цикл
def mainloop_direction():
    window = sg.Window('Direction', layout_direction) # создаём окно с уже записанным интерйесом
    while True:             
        event, values = window.read() # читаем окно на нажатия и вводы
        if event in (sg.WIN_CLOSED, 'Cancel'): # учим окно нормально закрыватся
            break # завершаем цикл

    window.close() # закроем окно
