import pyximport # импоритурем Cython
pyximport.install() # инициализируем его
import PySimpleGUI as sg

def message(message):
    sg.theme('DarkAmber')   
    
    layout = [  [sg.Text(message)],
                [sg.Button('Ok')]
            ]

    
    window = sg.Window('Message', layout)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Ok': 
            break

    window.close()
