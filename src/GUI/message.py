import PySimpleGUI as sg

def message(message):
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text(message)],
                [sg.Button('Ok')]
            ]

    # Create the Window
    window = sg.Window('Message', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Ok': # if user closes window or clicks cancel
            break

    window.close()
