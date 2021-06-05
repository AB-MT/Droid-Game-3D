import PySimpleGUI as sg

def site(site):
    sg.popup('You connect to game site : ' + site)

    return site

if __name__ == '__main__':
    site('github.com')
