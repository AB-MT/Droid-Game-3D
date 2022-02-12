import PySimpleGUI as sg

layout = [
    [sg.Text('Write enemy pos')],
    [sg.Text('X :'), sg.InputText('', key='X')],
    [sg.Text('Y :'), sg.InputText('', key='Y')],
    [sg.Text('Z :'), sg.InputText('', key='Z')],
    [sg.Button('Ok')]
        ] # элементы окна

window = sg.Window('Level editor').Layout(layout) # создаём окно

def return_pos():
    while True:
        event, values = window.read() # читаем окно
        if event == sg.WIN_CLOSED or event == 'Ok': # если пользователь нажал на кнопку закрытия, закрываем окно
            pos = [values['X'], values['Y'], values['Z']] # записываем в список всю позицию противника
            return pos # возвращаем список позицию
        
            break # останавливаем цикл

    window.close() # закрываем окно


if __name__ == '__main__':
    pos = return_pos() # вызываем функцию где работает главный цикл для интерфейса и т. д.
    print(pos)    
    print('Writing pos ' + str(pos) + '...') # пишем сообщение в консоль о том, что пишем позицию
    with open("./save.txt", "w+") as pos2: # открываем файл
        pos2.write(pos[0] + '\n') # пишем X позицию противника
        pos2.write(pos[1] + '\n') # пишем Y позицию противника
        pos2.write(pos[2]) # пишем Z позицию противник
