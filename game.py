#!/usr/bin/env python
# -*- coding: utf_8 -*-

# Создано : 22 число, январь, 2021 год

# Импортируем все необходимые инструменты интерфейса

# Записываем все сообщения в файл logs.txt будут записыватся : имя уровня, время, само сообщение
import logging  # имортируем модуль, который будет записывать все проблемы в файл

from src.GUI.message import *  # импортируем интерфейс сообщений.

logging.basicConfig(
    filename="logs.txt",
    format="[%(levelname)s] %(asctime)s: %(message)s",
    level=logging.INFO,
)  # записываем все проблемы в файл


# только в случае ошибки
def only_for_error():
    global IP_USER_, DEFAULT_PORT_, VERSION_  # глобальные айпи, порт, версия

    IP_USER_ = ipgetter.myip()  # айпи
    DEFAULT_PORT_ = 9099  # порт
    VERSION_ = VERSION  # версия


try:
    from panda3d.core import *

    # встроенные в графических движка элементы
    from direct.gui import DirectGuiGlobals as DGG  # глобалы

    from direct.showbase.ShowBase import ShowBase  # инициализация графичиских элементов
    from direct.particles.ParticleEffect import ParticleEffect  # эффет партиклов(дым, пар, огонь, вода и т. д.)
    from direct.gui.OnscreenImage import OnscreenImage  # изображение на экране
    from direct.gui.OnscreenText import OnscreenText  # текст на экране
    from direct.interval.IntervalGlobal import *  # интервал вращение объекта

    from direct.gui.DirectScrolledList import DirectScrolledList  # прокручивающееся список
    from direct.gui.DirectScrolledList import DirectScrolledListItem  # элемент такого списка
    from direct.gui.DirectScrolledFrame import DirectScrolledFrame  # прокручивающающаяся рамка

    from direct.gui.DirectDialog import OkDialog  # диалог с кнопкой "ок"
    from direct.gui.DirectButton import DirectButton  # кнопка
    from direct.gui.DirectLabel import DirectLabel  # метка
    from direct.gui.DirectEntry import DirectEntry  # ввод
    from direct.gui.DirectSlider import DirectSlider  # слайдер
    from direct.gui.DirectCheckBox import DirectCheckBox  # галочка
    from direct.gui.DirectCheckButton import DirectCheckButton  # галочка с текстом

    from direct.distributed.PyDatagram import \
        PyDatagram  # PyDatagram - простой встроенный модуль в движок для создания онлайна

    # Ну, вот, импортируем panda3d(игр. движ.) ну и мой небольшой API к нему - marconit_engine(поддержка прекращена)
    from src.settings import *  # настройки
    import src.gui as gui  # все ГУИ(графический интерфейс пользователя)
    from src.GUI.message import  message
    from src.GUI.moderators import GUI as moderators_gui # интерфейс модераторов
    from src.GUI.developers import GUI as developers_gui # интерфейс разработчиков
    from src.GUI.privilege import GUI as privilege_gui # интерфейс привелегий
    from src.GUI.settings_gui import GUI as settings_gui # интерфейс настроек
    from src.GUI.user_profile import GUI as user_profile_gui # интерфейс профиля пользователя
    from src.parsers.loading_levels import *
    from src.sys.servers_sys import * # система серверов
    import src.audio as audio  # аудио
    import src.pbp as pbp  # pbr система
    import src.ipgetter as ipgetter  # получатель айпи
    import random  # рандом
    import sys  # система
    import time  # время
    from datetime import datetime  # время - 2
    import os  # модуль для терминальных команд
    import math  # математика....ААААААААААААААААААААААА!!
    from screeninfo import get_monitors  # модуль для получения информации об экране
    import socket  #  модуль для сервера
    import json  # читатель файлов(если есть аддоны)
    import requests  # запрсник
    import asyncio  # ассинхоность
    import select  # типа сокета, но лучше

    print('Normal importing modules [OK]')  # печатаем что нормально загрузились модули

    config = json.load(open("./RES/addon_config.json"))  # загружаем конфиг аддона
    addon_classes = []  # классы аддонов

    message(message=f'Welcome to Droid Game {VERSION}')  # сообщение
    # подключение к серверу
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем обьект портала для подключения
    s.connect((sites[0], DEFAULT_PORT))  # подключаемся к серверу
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # делаем коннект к серверу многоразовый
    s.send(
        f'Connected by Droid Game {VERSION} and IP {IP_USER}:{DEFAULT_PORT}'.encode())  # посылаем на сервер сообщение

    loadPrcFileData('', 'show-frame-rate-meter true')  # показываем количество кадров в секунду
    loadPrcFileData(
        "",
        "audio-library-name "
        + ("p3openal_audio" if sys.platform == "linux" else "p3fmod_audio"),
    )  # система звука в зависимости от вашей ОС
    loadPrcFileData("", "threading-model Cull/Draw")  # используем многопоточный рендер


    def load_profile(filename_p):
        '''загружаем профиль'''
        with open(filename_p, "r") as f:  # загружаем файл с профилем
            for line in f:  # читаем линии в файле
                return line  # возвращаем линию(-и)


    # функция для обновления файла
    def update_file(directory_, filename_p_, value, name):
        path = directory_ + '/' + filename_p_  # отдельная переменная для  всей директории файла

        open_file = open(str(path), "w+")  # открываем файл
        open_file.write(value)  # пишем новое значение
        open_file.close()  # закрываем файл

        return f"Normal update {name} [OK]"  # типа файл хорошо загрузился и обновился


    USERNAME = load_profile('./profile/username.txt') + str(random.randrange(0, 10000))  # загружаем имя пользователя
    RATING = int(load_profile('./profile/rating.txt'))  # загружаем рейтинг пользователя
    STATUS = load_profile('./profile/status.txt')  # загружаем статус пользователя


    # старт клиента
    def start_client():
        worldClient = Client(9099, ipgetter.myip())  # подключение к миру и получение айпи
        N = PlayerReg()  # регистрация игрока в мире
        keys = Keys()  # клавиши
        w = World()  # мир
        chatReg = chatRegulator(worldClient, keys)  # рега чата


    def receiveTextViaSocket(sock):
        '''Получает сообщение с сервера'''
        # получaeт текст через сокет
        encodedMessage = sock.recv(1024)

        # если мы ничего не получили то возвращаем ничего..
        if not encodedMessage:
            return None

        # расшифровываем полученное сообщение
        message = encodedMessage.decode('utf-8')

        # теперь пора отправить подтверждение
        # шифруем текст подтверждения
        encodedAckText = bytes(ACK_TEXT, 'utf-8')

        # отправляем шифрованный текст подтверждения
        sock.sendall(encodedAckText)

        return message  # возвращаем сообщение


    # проверка обновлений(с ассинхроностью)
    async def listening_updates(server_updates):
        while True:
            link = server_updates  # ссылка
            f = requests.get(link)  # получаем текст
            if True:  # текст будет либо True либо False
                update = 'it"s not work, sorry('
                vers  = '4/6'
                await message(f'''
                        UPDATE! Added: {update}
                                Number update: {vers}

                                    Thanks for playing :)
                        ''')  # сообщение об обновлении



    # отправка сообщения
    def sending(msg):
        '''отправляет сообщение'''
        s.send(str(msg).encode())  # отправка в байтах


    def showHelpInfo():
        # Говорим пользователю об использованиu
        print('Droid Game ' + VERSION + ' - ' + COPYRIGHT)  # информация о игре
        print('Использование(Usage):')  # использование
        print('-d \t\t\Режим разробoтчика(Developer mode)')  # тут всё написано
        print('-l \t\t\Скачать уровни(Download levels)')  # и тут тоже
        sys.exit()  # выходим


    # если пользователю интересно, как пользоватся программой, говорим ему об этом
    if "-h" in sys.argv or "/?" in sys.argv or "--help" in sys.argv:
        showHelpInfo()  # показываем нформацию

    # если пользователь указал аргумент режима разроботчика, вкл. его
    elif '-d' in sys.argv:
        DEVELOP_MODE = True

    # если пользователь указал аргумент скачивания уровней, скачиваем уровни
    elif '-l' in sys.argv:
        downloading()


    # запуск с ассинхроностью
    async def start():
        droid = DroidShooter()  # обьект игры
        await droid.run()  # let's start it!


    #  проверка на наличие модерки
    if USERNAME in MODS:
        sending(f'Moderator!  {IP_USER}:{DEFAULT_PORT}')  # отправляем на сервер сообщение


    # запуск всех задач с асинхроностью
    async def main():
        taskA = loop.create_task(start())  # основная игра
        taskB = loop.create_task(listening_updates(sites[0]))  # Проверяем обновления
        taskC = loop.create_task(check_receive())  # проверка полученых сообщений

        await asyncio.wait([taskA, taskB, taskC])  # запуск задач


    # режим захвата флага
    class Capture_flag():
        def __init__(self, player, base_1, base_2):
            self.player = player  # инициализируем игрока
            self.base_1 = base_1  # инициализируем первую базу
            self.base_2 = base_2  # инициализируем вторую базу

            self.player_pos = self.player.getPos()  # получаем позицию игрока
            self.base_1_pos = base_1.getPos()  # получаем позицию первой базы
            self.base_2_pos = base_2.getPos()  # получаем позицию второй базы

        def update(self):  # обновление захвата флага
            self.player_pos = self.player.getPos()  # получаем новую позицию игрока
            self.base_1_pos = self.base_1.getPos()  # получаем новую позицию первой базы
            self.base_2_pos = self.base_2.getPos()  # получаем новую позицию второй базы

            if self.player_pos == self.base_2_pos:  # если игрок находится на координатах второй базы, то...
                return True  # ...возвращаем True


    # Создадим главный класс нашей игры
    class DroidShooter(ShowBase):
        def __init__(self):
            ShowBase.__init__(self)  # Загружаем все селфы из direct
            self.speed = 100  # скорость двигателя
            self.GB = False  # НЕ чёрно-белый режим
            self.EN = False  # Не будем включать английский язык
            self.rust_effect = False  # Поставим, что дроид не ржавый
            self.basic_droid = True  # включаем стандартного дроида
            self.pod_droid = False  # не включаем большого дроида
            self.shield_droid = False  # не включаем щитного дроида
            self.pro_machine = False  # Не включаем проффесиональное управление
            self.single = False  # Не включаем одиночную игру
            self.sun_interval = 80  # Интервал солнца
            self.exiting = False  # Поставим, что ещё не выходили из игры
            self.another_camera = False  # не включаем вид от первого лица
            self.arg_username = 'd'  # аргументы игрока
            self.username = USERNAME  # имя игрока
            self.rating = RATING  # рейтинг игрока
            self.weapon_choosed = False  # поставим, что другое оружие не выбрано

            self.level = load_level(LEVEL1)  # уровень по умолчанию(первый)

            # проходимся по всем мониторам(у многих программистов их два, но если он у вас один, всё всё равно будет работать)
            for monitor in get_monitors():
                self.screen_width = monitor.width - 700  # делаем новый размер окна по ширине
                self.screen_height = monitor.height - 400  # делаем новый размер окна по высоте

            self.menu(False)  # зaпуск меню

        def weapon_menu___init__(self, cm, rootParent=None):

            '''Выбор оружия'''

            if cm:  # если заходим второй раз
                if self.weapon_choosed:  # другое оруужие не выбрано
                    self.pistol_weapon.destroy()  # удаляеем кнопку пистолета

                else:  # а если не выбрано
                    self.sniper_weapon.destroy()  # удаляем кнопку снайперки

            if not self.weapon_choosed:  # если другое оружие не выбрано...
                self.pistol_weapon = DirectButton(  # рисуем интерфейс кнопки с пистолетом
                    borderWidth=(0.2, 0.7),
                    frameColor=(0.9, 0.85, 0.876, 0.5),
                    frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                    hpr=LVecBase3f(0, 0, 0),
                    pos=LPoint3f(0.8, 0, 0.675),
                    scale=LVecBase3f(0.1, 0.1, 0.1),
                    text='Pistol',
                    text_align=TextNode.A_center,
                    text_scale=(0.5, 1.0),
                    text_pos=(0, 0),
                    text_fg=LVecBase4f(0, 0, 0, 1),
                    text_bg=LVecBase4f(0, 0, 0, 0),
                    text_wordwrap=None,
                    parent=rootParent,
                    pressEffect=1,
                    command=self.pistol_choosed
                )
                self.pistol_weapon.setTransparency(0)

            else:  # а если выбрано...
                self.sniper_weapon = DirectButton(  # рисуем интерфейс кнопки с снайперкой
                    borderWidth=(0.2, 0.7),
                    frameColor=(0.9, 0.85, 0.876, 0.5),
                    frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                    hpr=LVecBase3f(0, 0, 0),
                    pos=LPoint3f(0.8, 0, 0.675),
                    scale=LVecBase3f(0.1, 0.1, 0.1),
                    text='Sniper',
                    text_align=TextNode.A_center,
                    text_scale=(0.5, 1.0),
                    text_pos=(0, 0),
                    text_fg=LVecBase4f(0, 0, 0, 1),
                    text_bg=LVecBase4f(0, 0, 0, 0),
                    text_wordwrap=None,
                    parent=rootParent,
                    pressEffect=1,
                    command=self.sniper_choosed
                )
                self.sniper_weapon.setTransparency(0)

        def pistol_choosed(self):

            self.weapon.hide()  # удаляем прередущие оружие
            self.weapon = GameApi.object(self, './models/BasicDroid/pistol.egg', .5,
                                         self.weapon_pos)  # обновим оружие

            self.weapon_choosed = True  # поставим, что оружие выбрано другое
            self.weapon_menu___init__(True)  # открываем снова выбор оружия

        def sniper_choosed(self):

            self.weapon.hide()  # удаляем прередущие оружие
            self.weapon = GameApi.object(self, './models/BasicDroid/sniper.egg', .5,
                                         self.weapon_pos)  # обновим оружие

            self.weapon_choosed = False  # поставим, что оружие НЕ выбрано другое
            self.weapon_menu___init__(True)  # открываем снова выбор оружия

        def weapon_menu_show(self):
            '''показать меню оружий'''
            self.pg149.show()

        def weapon_menu_hide(self):
            '''скрыть меню оружий'''
            self.pg149.hide()

        def weapon_menu_destroy(self):
            '''удалить меню оружий'''
            self.pg149.destroy()

        def menu(self, menu, rootParent=None):

            # Настраиваем окно
            self.props = WindowProperties()  # класс настроек
            self.props.setTitle('Droid Game ' + VERSION)  # заголовок окна
            self.props.setUndecorated(True)  # убираем раму окна
            self.props.setSize(self.screen_width, self.screen_height)  # размер окна

            self.openDefaultWindow(props=self.props)  # Используем настройки

            base.enableParticles()  # инициализируем эффект дыма
            self.disableMouse()  # Отключаем перемещение через мышку

            self.win.setClearColor((0.2, 0.3
                                    , 0.6,
                                    1))  # Закрашиваем поверхность голубым. Дело в том, что по умолчанию в этом игровом движке поверхность закрашивается серым.
            self.font = loader.loadFont('./fonts/doom_font.ttf')  # загрузим шрифт из игры doom
            self.inst_font = loader.loadFont('./fonts/arial.ttf')  # загрузим шрифт arial
            self.ubunutu_inst_font = loader.loadFont('./fonts/UbuntuMono-BI.ttf') # загрузим шрифт UbunutuMono
            self.ia_inst_font = loader.loadFont('./fonts/iAWriterDuoS-Bold.ttf') # загрузим шрифт iAWriterDuos

            self.crackSound = audio.FlatSound('./sounds/glass-shatter1.ogg')  # звук взрыва корабля
            self.shotSound = audio.FlatSound('./sounds/sniper-rifle.ogg')  # звук выстрела
            self.errorSound = audio.FlatSound('./sounds/reload.ogg')  # звук запуска
            self.click_sound = audio.FlatSound('./sounds/click.ogg')  # звук нажатия
            self.command_sound = audio.FlatSound('./sounds/command.ogg')  # звук команды
            self.kamikaze_sound = audio.FlatSound('./sounds/kamikaze-special.ogg')  # звук опасности
            self.alarm_sound = audio.FlatSound('./sounds/alarm.ogg')  # звук опасности
            self.change_weapon_sound = audio.FlatSound('./sounds/change-weapon.ogg')  # звук перемены оружия
            self.shield_sound = audio.FlatSound('./sounds/shield.ogg')  # звук щита

            self.grenade_boom = audio.FlatSound('./sounds/grenade.ogg')  # звук гранаты
            self.grenade_boun = audio.FlatSound('./sounds/grenade-bounce.ogg')  # звук таймера гранаты
            self.grenade_launch = audio.FlatSound('./sounds/grenade-launch.ogg')  # звук взрыва гранаты

            self.BgSound = audio.FlatSound(
                "sounds/background.ogg", volume=.01)  # фоновая музыка в меню
            self.intro_sound = audio.FlatSound('./sounds/intro.ogg', volume=.01)  # звук интро

            # Планета
            if not menu:  # Если не входили в чат или инструменты рисуем планету.
                self.BgSound.play()  # играем звук запуска игры

                self.camera_distation = random.randrange(20,
                                                         30)  # дистанция камеры от планеты. генерируем её рандомно в диапозоне от 20 до 30
                self.globe = loader.loadModel("menu/Globe")  # загружаем модель планеты
                self.globe.reparentTo(render)  # инициализируем модель
                self.globe.setTransparency(TransparencyAttrib.MAlpha)  # прозрачность
                self.globe.setColor(Vec4(1, 1, 1, 0.6))  # цвет
                self.globe.setScale((1.5, 1.5, 1.5))
                self.globe.setTwoSided(True)  # двойная модель
                self.globe.setRenderModeWireframe()  # полигольный режим

                # Врашение планеты
                self.globe.hprInterval(300, (360, 360, 0)).loop()

                self.camera.setPos(0, -self.camera_distation, 0)  # камера

            # P. S. Это меню я не писал. Оно сделано на DirectGUIDesigner
            self.pg3083 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.675, 0, 0.15),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Войти',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=rootParent,
                command=self.load_game,
                pressEffect=1,
            )
            self.pg3083.setTransparency(0)
    
            
            self.pg8620 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.675, 0, 0.03),
                scale=LVecBase3f(.1, .1, .1),
                text='Выход',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=rootParent,
                command=self.easy_exit,
                pressEffect=1,
            )
            self.pg8620.setTransparency(0)

            self.pg19052 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(18.76, 0, 4.90),
                scale=LVecBase3f(1, 1, 1),
                text='ИвУД',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=self.pg8620,
                command=self.pro_system,
                pressEffect=1,
            )
            self.pg19052.setTransparency(0)

            self.pg27986 = DirectEntry(
                frameSize=(-0.1, 10.1, -0.3962500154972076, 1.087500011920929),
                hpr=LVecBase3f(0, 0, 0),
                initialText=self.username,
                pos=LPoint3f(-0.825, 0, -0.125),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text_align=TextNode.A_left,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=rootParent,
            )
            self.pg27986.setTransparency(0)

            self.pg28909 = DirectSlider(
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.3, 0, 0.85),
                text='Lifes Machine',
                value=0,
                text_align=TextNode.A_center,
                text_scale=(0.1, 0.1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                thumb_frameSize=(-0.05, 0.05, -0.08, 0.08),
                thumb_hpr=LVecBase3f(0, 0, 0),
                thumb_pos=LPoint3f(-0.949068, 0, 0),
                parent=rootParent,
                command=self.set_lifes
            )
            self.pg28909.setTransparency(0)

            
            self.pgSingle = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, -0.55),
                scale=LVecBase3f(0.2, 0.3, 0.2),
                text='Навигатор',
                text_align=TextNode.A_center,
                text_scale=(0.7, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=rootParent,
                command=self.open_navigator,
                pressEffect=1,
            )

            self.pg452 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0.111, 11, 1111),
                pos=LPoint3f(1, 0, 0.75),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Баг?',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.inst_font,
                parent=rootParent,
                pressEffect=0,
                command=self.bug_message,
            )
            self.pg452.setTransparency(0)

            self.accept("escape", sys.exit)  # При нажатии клавиши Esc выходим.

        def navigator_gui_destroy(self):
            self.pg10440.destroy()
            self.pg54414.destroy()
            self.pg55101.destroy()
            self.pg56428.destroy()
            self.pg57473.destroy()
            self.pg58545.destroy()
            self.pg128050.destroy()

        def open_navigator(self, rootParent=None):
            # Удаляем элементы меню
            self.pg3083.destroy()
            self.pg27986.destroy()
            self.pg28909.destroy()
            self.pg452.destroy()
            self.pg8620.destroy()
            self.pgSingle.destroy()
            self.pg19052.destroy()

            self.pg10440 = DirectLabel(
                frameSize=(-2.65, 2.65, -0.113, 0.725),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, 0.4),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Навигация',
                text0_align=TextNode.A_center,
                text0_scale=(1, 1),
                text0_pos=(0, 0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                parent=rootParent,
                text_font= self.ia_inst_font,
            )
            self.pg10440.setTransparency(0)

            self.pg54414 = DirectButton(
                frameSize=(-3.225, 3.225, -0.213, 0.825),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.425, 0, 0.175),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Разработчики',
                text0_align=TextNode.A_center,
                text0_scale=(1, 1),
                text0_pos=(0, 0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                text1_align=TextNode.A_center,
                text1_scale=(1, 1),
                text1_pos=(0, 0),
                text1_fg=LVecBase4f(0, 0, 0, 1),
                text1_bg=LVecBase4f(0, 0, 0, 0),
                text1_wordwrap=None,
                text2_align=TextNode.A_center,
                text2_scale=(1, 1),
                text2_pos=(0, 0),
                text2_fg=LVecBase4f(0, 0, 0, 1),
                text2_bg=LVecBase4f(0, 0, 0, 0),
                text2_wordwrap=None,
                text3_align=TextNode.A_center,
                text3_scale=(1, 1),
                text3_pos=(0, 0),
                text3_fg=LVecBase4f(0, 0, 0, 1),
                text3_bg=LVecBase4f(0, 0, 0, 0),
                text3_wordwrap=None,
                parent=rootParent,
                pressEffect=1,
                command=self.open_developers_gui,
                text_font= self.ubunutu_inst_font,
            )
            self.pg54414.setTransparency(0)

            self.pg55101 = DirectButton(
                frameSize=(-2.825, 2.825, -0.213, 0.825),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.05, 0, 0.05),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Модераторы',
                text0_align=TextNode.A_center,
                text0_scale=(1, 1),
                text0_pos=(0, 0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                text1_align=TextNode.A_center,
                text1_scale=(1, 1),
                text1_pos=(0, 0),
                text1_fg=LVecBase4f(0, 0, 0, 1),
                text1_bg=LVecBase4f(0, 0, 0, 0),
                text1_wordwrap=None,
                text2_align=TextNode.A_center,
                text2_scale=(1, 1),
                text2_pos=(0, 0),
                text2_fg=LVecBase4f(0, 0, 0, 1),
                text2_bg=LVecBase4f(0, 0, 0, 0),
                text2_wordwrap=None,
                text3_align=TextNode.A_center,
                text3_scale=(1, 1),
                text3_pos=(0, 0),
                text3_fg=LVecBase4f(0, 0, 0, 1),
                text3_bg=LVecBase4f(0, 0, 0, 0),
                text3_wordwrap=None,
                parent=rootParent,
                pressEffect=1,
                command=self.open_moderators_gui,
                text_font= self.ubunutu_inst_font,
            )
            self.pg55101.setTransparency(0)

            self.pg56428 = DirectButton(
                frameSize=(-2.825, 2.825, -0.213, 0.825),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0.375, 0, 0.175),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Привелегии',
                text0_align=TextNode.A_center,
                text0_scale=(1, 1),
                text0_pos=(0, 0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                text1_align=TextNode.A_center,
                text1_scale=(1, 1),
                text1_pos=(0, 0),
                text1_fg=LVecBase4f(0, 0, 0, 1),
                text1_bg=LVecBase4f(0, 0, 0, 0),
                text1_wordwrap=None,
                text2_align=TextNode.A_center,
                text2_scale=(1, 1),
                text2_pos=(0, 0),
                text2_fg=LVecBase4f(0, 0, 0, 1),
                text2_bg=LVecBase4f(0, 0, 0, 0),
                text2_wordwrap=None,
                text3_align=TextNode.A_center,
                text3_scale=(1, 1),
                text3_pos=(0, 0),
                text3_fg=LVecBase4f(0, 0, 0, 1),
                text3_bg=LVecBase4f(0, 0, 0, 0),
                text3_wordwrap=None,
                parent=rootParent,
                pressEffect=1,
                command=self.open_privilege_gui,
                text_font= self.ubunutu_inst_font,
            )
            self.pg56428.setTransparency(0)

            self.pg57473 = DirectButton(
                frameSize=(-2.5, 2.5, -0.213, 0.825),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.4, 0, -0.1),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Настройки',
                text0_align=TextNode.A_center,
                text0_scale=(1, 1),
                text0_pos=(0, 0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                text1_align=TextNode.A_center,
                text1_scale=(1, 1),
                text1_pos=(0, 0),
                text1_fg=LVecBase4f(0, 0, 0, 1),
                text1_bg=LVecBase4f(0, 0, 0, 0),
                text1_wordwrap=None,
                text2_align=TextNode.A_center,
                text2_scale=(1, 1),
                text2_pos=(0, 0),
                text2_fg=LVecBase4f(0, 0, 0, 1),
                text2_bg=LVecBase4f(0, 0, 0, 0),
                text2_wordwrap=None,
                text3_align=TextNode.A_center,
                text3_scale=(1, 1),
                text3_pos=(0, 0),
                text3_fg=LVecBase4f(0, 0, 0, 1),
                text3_bg=LVecBase4f(0, 0, 0, 0),
                text3_wordwrap=None,
                parent=rootParent,
                pressEffect=1,
                command=self.open_settings_gui,
                text_font= self.ubunutu_inst_font,
            )
            self.pg57473.setTransparency(0)

            self.pg58545 = DirectButton(
                frameSize=(-3.0, 3.0, -0.213, 0.825),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0.375, 0, -0.1),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Мой профиль',
                text0_align=TextNode.A_center,
                text0_scale=(1, 1),
                text0_pos=(0, 0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                text1_align=TextNode.A_center,
                text1_scale=(1, 1),
                text1_pos=(0, 0),
                text1_fg=LVecBase4f(0, 0, 0, 1),
                text1_bg=LVecBase4f(0, 0, 0, 0),
                text1_wordwrap=None,
                text2_align=TextNode.A_center,
                text2_scale=(1, 1),
                text2_pos=(0, 0),
                text2_fg=LVecBase4f(0, 0, 0, 1),
                text2_bg=LVecBase4f(0, 0, 0, 0),
                text2_wordwrap=None,
                text3_align=TextNode.A_center,
                text3_scale=(1, 1),
                text3_pos=(0, 0),
                text3_fg=LVecBase4f(0, 0, 0, 1),
                text3_bg=LVecBase4f(0, 0, 0, 0),
                text3_wordwrap=None,
                parent=rootParent,
                pressEffect=1,
                command=self.open_profile_gui,
                text_font=self.ubunutu_inst_font,
            )
            self.pg58545.setTransparency(0)

            self.pg128050 = DirectButton(
                frameSize=LVecBase4f(-1.525, 1.65, -0.2125, 0.825),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.875, 0, 0.675),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='<- Назад',
                text0_align=TextNode.A_center,
                text0_scale=(0.6, 1),
                text0_pos=(0, 0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                text1_align=TextNode.A_center,
                text1_scale=(0.7, 1),
                text1_pos=(0, 0),
                text1_fg=LVecBase4f(0, 0, 0, 1),
                text1_bg=LVecBase4f(0, 0, 0, 0),
                text1_wordwrap=None,
                text2_align=TextNode.A_center,
                text2_scale=(0.7, 1),
                text2_pos=(0, 0),
                text2_fg=LVecBase4f(0, 0, 0, 1),
                text2_bg=LVecBase4f(0, 0, 0, 0),
                text2_wordwrap=None,
                text3_align=TextNode.A_center,
                text3_scale=(0.6, 1),
                text3_pos=(0, 0),
                text3_fg=LVecBase4f(0, 0, 0, 1),
                text3_bg=LVecBase4f(0, 0, 0, 0),
                text3_wordwrap=None,
                text_font=self.inst_font,
                command=self.navigator_destroy,
                parent=rootParent,
                pressEffect=1,
            )
            self.pg128050.setTransparency(0)

            self.accept("escape", sys.exit)  # При нажатии клавиши Esc выходим.

        def navigator_destroy(self):
            # Удаляем элементы навигатора
            self.pg10440.destroy()
            self.pg54414.destroy()
            self.pg55101.destroy()
            self.pg56428.destroy()
            self.pg57473.destroy()
            self.pg58545.destroy()

        def settings_gui_destroy(self):
            # Удаляем элементы настроек
            self.pg4616.destroy()
            self.pg5474.destroy()
            self.pg6685.destroy()
            self.pg872.destroy()

            self.menu(False)

        def open_settings_gui(self, rootParent=None):
            self.navigator_gui_destroy() # удаляем элементы навигации

            self.pg4616 = DirectLabel(
                frameSize=(-3.15, 3.25, -0.113, 0.725),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.025, 0, 0.4),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Настройки',
                text0_align=TextNode.A_center,
                text0_scale=(1, 1),
                text0_pos=(0, 0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                parent=rootParent,
                text_font=self.ia_inst_font,
            )
            self.pg4616.setTransparency(0)

            self.pg5474 = DirectCheckButton(
                frameSize=(-3.775, 10.025, -0.312, 0.913),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.275, 0, 0.225),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Одиночная игра',
                indicator_hpr=LVecBase3f(0, 0, 0),
                indicator_pos=LPoint3f(-3.4, 0, 0.000500018),
                indicator_relief='sunken',
                indicator_text0_align=TextNode.A_center,
                indicator_text0_scale=(1, 1),
                indicator_text0_pos=(0, -0.2),
                indicator_text0_fg=LVecBase4f(0, 0, 0, 1),
                indicator_text0_bg=LVecBase4f(0, 0, 0, 0),
                indicator_text0_wordwrap=None,
                indicator_text1_align=TextNode.A_center,
                indicator_text1_scale=(1, 1),
                indicator_text1_pos=(0, -0.2),
                indicator_text1_fg=LVecBase4f(0, 0, 0, 1),
                indicator_text1_bg=LVecBase4f(0, 0, 0, 0),
                indicator_text1_wordwrap=None,
                text0_align=TextNode.A_left,
                text0_scale=(1, 1),
                text0_pos=(0, 0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                text1_align=TextNode.A_left,
                text1_scale=(1, 1),
                text1_pos=(0, 0),
                text1_fg=LVecBase4f(0, 0, 0, 1),
                text1_bg=LVecBase4f(0, 0, 0, 0),
                text1_wordwrap=None,
                text2_align=TextNode.A_left,
                text2_scale=(1, 1),
                text2_pos=(0, 0),
                text2_fg=LVecBase4f(0, 0, 0, 1),
                text2_bg=LVecBase4f(0, 0, 0, 0),
                text2_wordwrap=None,
                text3_align=TextNode.A_left,
                text3_scale=(1, 1),
                text3_pos=(0, 0),
                text3_fg=LVecBase4f(0, 0, 0, 1),
                text3_bg=LVecBase4f(0, 0, 0, 0),
                text3_wordwrap=None,
                parent=rootParent,
                command=self.single_player,
                text_font=self.ia_inst_font,
            )
            self.pg5474.setTransparency(0)

            self.pg6685 = DirectCheckButton(
                frameSize=(-3.775, 10.025, -0.312, 0.913),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.275, 0, 0.075),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Черно-белый режим',
                indicator_hpr=LVecBase3f(0, 0, 0),
                indicator_pos=LPoint3f(-3.4, 0, 0.000500018),
                indicator_relief='sunken',
                indicator_text0_align=TextNode.A_center,
                indicator_text0_scale=(1, 1),
                indicator_text0_pos=(0, -0.2),
                indicator_text0_fg=LVecBase4f(0, 0, 0, 1),
                indicator_text0_bg=LVecBase4f(0, 0, 0, 0),
                indicator_text0_wordwrap=None,
                indicator_text1_align=TextNode.A_center,
                indicator_text1_scale=(1, 1),
                indicator_text1_pos=(0, -0.2),
                indicator_text1_fg=LVecBase4f(0, 0, 0, 1),
                indicator_text1_bg=LVecBase4f(0, 0, 0, 0),
                indicator_text1_wordwrap=None,
                text0_align=TextNode.A_left,
                text0_scale=(1, 1),
                text0_pos=(-2.0, 0.0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                text1_align=TextNode.A_left,
                text1_scale=(1, 1),
                text1_pos=(-2.0, 0.0),
                text1_fg=LVecBase4f(0, 0, 0, 1),
                text1_bg=LVecBase4f(0, 0, 0, 0),
                text1_wordwrap=None,
                text2_align=TextNode.A_left,
                text2_scale=(1, 1),
                text2_pos=(-2.0, 0.0),
                text2_fg=LVecBase4f(0, 0, 0, 1),
                text2_bg=LVecBase4f(0, 0, 0, 0),
                text2_wordwrap=None,
                text3_align=TextNode.A_left,
                text3_scale=(1, 1),
                text3_pos=(-2.0, 0.0),
                text3_fg=LVecBase4f(0, 0, 0, 1),
                text3_bg=LVecBase4f(0, 0, 0, 0),
                text3_wordwrap=None,
                parent=rootParent,
                command=self.gb_mode,
                text_font= self.ia_inst_font,
            )
            self.pg6685.setTransparency(0)

            self.pg872 = DirectButton(
                frameSize=LVecBase4f(-1.525, 1.65, -0.2125, 0.825),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.525, 0, 0.4),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Меню',
                text0_align=TextNode.A_center,
                text0_scale=(1, 1),
                text0_pos=(0, 0),
                text0_fg=LVecBase4f(0, 0, 0, 1),
                text0_bg=LVecBase4f(0, 0, 0, 0),
                text0_wordwrap=None,
                text1_align=TextNode.A_center,
                text1_scale=(1, 1),
                text1_pos=(0, 0),
                text1_fg=LVecBase4f(0, 0, 0, 1),
                text1_bg=LVecBase4f(0, 0, 0, 0),
                text1_wordwrap=None,
                text2_align=TextNode.A_center,
                text2_scale=(1, 1),
                text2_pos=(0, 0),
                text2_fg=LVecBase4f(0, 0, 0, 1),
                text2_bg=LVecBase4f(0, 0, 0, 0),
                text2_wordwrap=None,
                text3_align=TextNode.A_center,
                text3_scale=(1, 1),
                text3_pos=(0, 0),
                text3_fg=LVecBase4f(0, 0, 0, 1),
                text3_bg=LVecBase4f(0, 0, 0, 0),
                text3_wordwrap=None,
                parent=rootParent,
                command=self.settings_gui_destroy,
                pressEffect=1,
                text_font= self.ubunutu_inst_font,
            )
            self.pg872.setTransparency(0)

            self.accept('esc', self.top_players_gui_destroy)  # при нажатии Esc - убираем это меню

        def open_top_gui(self):
            # Удаляем элементы меню
            self.pg3083.destroy()
            self.pg27986.destroy()
            self.pg28909.destroy()
            self.pg452.destroy()
            self.pgSingle.destroy()

            self.top_players_gui = GUI(USERNAME)  # загружаем интерфейс который прописан в файле

            self.accept('esc', self.top_players_gui_destroy)  # при нажатии E - убираем это меню

        def open_developers_gui(self):
            # Удаляем элементы меню
            self.navigator_gui_destroy()

            self.developers_gui = developers_gui(DEVELOPERS)  # загружаем интерфейс который прописан в файле

            self.accept('esc', self.developers_gui_destroy)  # при нажатии E - убираем это меню

        def open_moderators_gui(self):
            # Удаляем элементы меню
            self.navigator_gui_destroy()

            self.moderators_gui = moderators_gui(moders_list=MODS)  # загружаем интерфейс который прописан в файле

            self.accept('esc', self.moderators_gui_destroy)  # при нажатии E - убираем это меню

        def open_profile_gui(self):
            # Удаляем элементы меню
            self.navigator_gui_destroy()

            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды

            self.profile_gui = user_profile_gui(username=USERNAME, status=STATUS,
                                     rating=str(self.rating))  # загружаем интерфейс который прописан в файле

            self.accept('esc', self.profile_gui_destroy)  # при нажатии E - убираем это меню

        def open_privilege_gui(self):
            # Удаляем элементы меню
            self.navigator_gui_destroy()

            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды

            self.prvilege_gui = privilege_gui()  # загружаем интерфейс привелегий

        def profile_gui_destroy(self):
            self.profile_gui.destroy()  # убираем интерфейс профиля

            self.menu(False)  # открываем меню

        def moderators_gui_destroy(self):
            self.moderators_gui.destroy()  # убираем интерфейс модераторов

            self.menu(False)  # открываем меню

        def top_players_gui_destroy(self):
            self.top_players_gui.destroy()  # убираем интерфейс топовых игроков

            self.menu(False)  # открываем меню

        def developers_gui_destroy(self):
            self.developers_gui.destroy()  # убираем интерфейс разроботчиков

            self.menu(False)  # открываем меню

        def direction_show(self):
            '''показ управления'''
            gui.mainloop_direction()

        def chat_gui_destroy(self):
            self.pg1384.destroy()  # удаляем интерфейс чата
            self.pgpg10418.destroy()  # удаляем интерфейс чата

            self.menu(False)  # открываем меню

        def choose_level(self, rootParent=None):
            # выбор уровня
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды

            # сделаем одиночную игру.
            self.single = True

            # удаляем элемиенты меню
            self.pg3083.destroy()
            self.pg27986.destroy()
            self.pg28909.destroy()
            self.pg149.destroy()
            self.pg452.destroy()
            self.pg326.destroy()
            self.pgSingle.destroy()
            self.pgServers.destroy()

            self.pg149 = DirectLabel(
                frameSize=(-3.15, 3.25, -0.113, 0.725),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0.075, 0, 0.675),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Choose server',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=rootParent,
            )
            self.pg149.setTransparency(0)

            self.pg683 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-4.6, 0, -1.975),
                scale=LVecBase3f(1, 1, 1),
                text='1',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg149,
                command=self.one_level,
                pressEffect=1,
            )
            self.pg683.setTransparency(0)

            self.pg2663 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(3.45, 0, 0),
                scale=LVecBase3f(1, 1, 1),
                text='2',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg683,
                command=self.two_level,
                pressEffect=1,
            )
            self.pg2663.setTransparency(0)

            self.pg26632 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(6.90, 0, 0),
                scale=LVecBase3f(1, 1, 1),
                text='3',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg683,
                command=self.three_level,
                pressEffect=1,
            )
            self.pg2663.setTransparency(0)

        def one_level(self):
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды
            # включение первого уровня
            self.level = load_level(LEVEL1)
            # удаляем элементы
            self.pg149.hide()
            self.menu(False)  # включим menu

        def two_level(self):
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды
            # включение второго уровня
            self.level = load_level(LEVEL2)
            # удаляем элементы
            self.pg149.hide()
            self.menu(False)  # включим menu

        def three_level(self):
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды
            # включение третьего уровня
            self.level = load_level(LEVEL3)
            # удаляем элементы
            self.pg149.hide()
            self.menu(False)  # включим menu

        def bug_message(self, rootParent=None):
            # сообщение о баге

            # удаляем элемиенты меню
            self.pg3083.destroy()
            self.pg27986.destroy()
            self.pg28909.destroy()
            self.pg149.destroy()
            self.pg452.destroy()
            self.pg326.destroy()
            self.pgSingle.destroy()
            self.pgServers.destroy()

            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды

            # рисуем интерфейс
            self.pg149 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.6, 0, 0.175),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Send',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=rootParent,
                pressEffect=1,
                command=self.exit_menu4
            )
            self.pg149.setTransparency(0)

            self.pg438 = DirectEntry(
                frameSize=(-0.1, 10.1, -0.3962500154972076, 1.087500011920929),
                hpr=LVecBase3f(0, 0, 0),
                initialText='',
                pos=LPoint3f(-1.415, 0, -1.425),
                scale=LVecBase3f(1.5, 1, 1),
                text_align=TextNode.A_left,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg149,
            )
            self.pg438.setTransparency(0)

        def select_droid(self, rootParent=None):
            # Выбор дроида

            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды

            # удаляем элемиенты меню
            self.pg3083.destroy()
            self.pg27986.destroy()
            self.pg28909.destroy()
            self.pg149.destroy()
            self.pg452.destroy()
            self.pg326.destroy()
            self.pgSingle.destroy()
            self.pgServers.destroy()

            # Рисуем интерфейс
            self.pg188 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.825, 0, 0.3),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Basic',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=rootParent,
                command=self._basic_droid,
                pressEffect=1,
            )
            self.pg188.setTransparency(0)

            self.pg477 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(3.525, 0, 0),
                scale=LVecBase3f(1, 1, 1),
                text='Pod',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg188,
                command=self._pod_droid,
                pressEffect=1,
            )
            self.pg477.setTransparency(0)

            self.pg2183 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(6.975, 0, 0.025),
                scale=LVecBase3f(1, 1, 1),
                text='Shield',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg188,
                pressEffect=1,
                command=self._shield_droid
            )
            self.pg2183.setTransparency(0)

            self.pg4741 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.5, 0, 0.15),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='menu',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=rootParent,
                pressEffect=1,
                command=self.exit_menu2
            )
            self.pg4741.setTransparency(0)



        def update_chat(self):
            # читаем все сообщения, показывая их
            for message in messages:
                self.pg7119 = DirectScrolledListItem(
                    frameSize=LVecBase4f(-3.83125, 3.90625, -0.2125, 0.85),
                    hpr=LVecBase3f(0, 0, 0),
                    pos=LPoint3f(0, 0, 0),
                    scale=LVecBase3f(0.1, 0.1, 0.1),
                    state='disabled',
                    text=message,
                    text0_align=TextNode.A_center,
                    text0_scale=(1, 1),
                    text0_pos=(0, 0),
                    text0_fg=LVecBase4f(0, 0, 0, 1),
                    text0_bg=LVecBase4f(0, 0, 0, 0),
                    text0_wordwrap=None,
                    text1_align=TextNode.A_center,
                    text1_scale=(1, 1),
                    text1_pos=(0, 0),
                    text1_fg=LVecBase4f(0, 0, 0, 1),
                    text1_bg=LVecBase4f(0, 0, 0, 0),
                    text1_wordwrap=None,
                    text2_align=TextNode.A_center,
                    text2_scale=(1, 1),
                    text2_pos=(0, 0),
                    text2_fg=LVecBase4f(0, 0, 0, 1),
                    text2_bg=LVecBase4f(0, 0, 0, 0),
                    text2_wordwrap=None,
                    text3_align=TextNode.A_center,
                    text3_scale=(1, 1),
                    text3_pos=(0, 0),
                    text3_fg=LVecBase4f(0, 0, 0, 1),
                    text3_bg=LVecBase4f(0, 0, 0, 0),
                    text3_wordwrap=None,
                    text0_font=self.font,
                    parent=self.pg4898,
                    command=base.messenger.send,
                    extraArgs=['select_list_item_changed'],
                )
                self.pg7119.setTransparency(0)

                self.pg4898.addItem(self.pg7119)

        def send_message(self, value):
            global messages  # делаем переменную глобальной

            if RATING >= 1010:  # если рейтинг больше или равен 1010 - можно отправлять сообщение в чате
                sending(
                    f'Message "{value}" from chat by {USERNAME}. {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер.
                messages.append(value)  # добавляем в список сообщений сообщение
                self.open_chat()  # открываем чат

            else:  # если рейтинг ниже 1010
                sending(
                    f'{USERNAME} can"t send message "{value}" because haven"t 1010 rating {IP_USER}:{DEFAULT_PORT}')  # отарвляем сообщение на сервер
                self.open_chat()  # открываем чат

        def open_chat(self, rootParent=None):
            # Чат

            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды

            # удаляем элементы меню
            self.pg3083.destroy()
            self.pg27986.destroy()
            self.pg28909.destroy()
            self.pg149.destroy()
            self.pg452.destroy()
            self.pg326.destroy()
            self.pgSingle.destroy()
            self.pgServers.destroy()

            # Рисуем интерфейс
            self.pg1384 = DirectScrolledFrame(
                canvasSize=(-2.0, 2.0, -2.0, 100.0),
                frameColor=(1, 1, 1, 1),
                frameSize=(-1.0, 1.0, -0.3, 1.0),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, 0),
                scrollBarWidth=0.08,
                state='normal',
                horizontalScroll_borderWidth=(0.01, 0.01),
                horizontalScroll_hpr=LVecBase3f(0, 0, 0),
                horizontalScroll_pos=LPoint3f(0, 0, 0),
                horizontalScroll_decButton_borderWidth=(0.01, 0.01),
                horizontalScroll_decButton_frameSize=(-0.05, 0.05, -0.04, 0.04),
                horizontalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
                horizontalScroll_decButton_pos=LPoint3f(-0.96, 0, -0.26),
                horizontalScroll_incButton_borderWidth=(0.01, 0.01),
                horizontalScroll_incButton_frameSize=(-0.05, 0.05, -0.04, 0.04),
                horizontalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
                horizontalScroll_incButton_pos=LPoint3f(0.88, 0, -0.26),
                horizontalScroll_thumb_borderWidth=(0.01, 0.01),
                horizontalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
                horizontalScroll_thumb_pos=LPoint3f(-0.4976, 0, -0.26),
                verticalScroll_borderWidth=(0.01, 0.01),
                verticalScroll_hpr=LVecBase3f(0, 0, 0),
                verticalScroll_pos=LPoint3f(0, 0, 0),
                verticalScroll_decButton_borderWidth=(0.01, 0.01),
                verticalScroll_decButton_frameSize=(-0.04, 0.04, -0.05, 0.05),
                verticalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
                verticalScroll_decButton_pos=LPoint3f(0.96, 0, 0.96),
                verticalScroll_incButton_borderWidth=(0.01, 0.01),
                verticalScroll_incButton_frameSize=(-0.04, 0.04, -0.05, 0.05),
                verticalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
                verticalScroll_incButton_pos=LPoint3f(0.96, 0, -0.18),
                verticalScroll_thumb_borderWidth=(0.01, 0.01),
                verticalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
                verticalScroll_thumb_pos=LPoint3f(0.96, 0, 0.913661),
                parent=rootParent,
            )
            self.pg1384.setTransparency(0)

            self.pg10418 = DirectEntry(
                hpr=LVecBase3f(0, 0, 0),
                initialText='Write message here :)',
                pos=LPoint3f(-0.6, 0, 0),
                text_align=TextNode.A_left,
                text_scale=(0.1, 0.1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                command=self.send_message,
                parent=rootParent,
            )
            self.pg10418.setTransparency(0)

            self.pg10419 = DirectEntryScroll(
                frameColor=(0.0, 0.0, 0.0, 0.0),
                frameSize=(1.0, 1.0, 1.0, 1.0),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.2, 0, -0.05),
                scale=LVecBase3f(1, 0.7, 0.7),
                text_font=self.font,
                parent=rootParent,
                entry=self.pg10418,
            )
            self.pg10419.setTransparency(0)

            # Рисуем сообщения
            if not len(messages) == 0:  # если кол-во сообщений не равно 0, то
                for i in messages:  # печатаем все сообщения
                    coords = float(
                        f'0.{len(messages) + 1}')  # координаты сообщения у меня не было других идей, но это работает
                    DirectLabel(
                        frameColor=(1.0, 1.0, 1.0, 1.0),
                        frameSize=(-15.75, 3.45, -0.113, 0.725),
                        hpr=LVecBase3f(0, 0, 0),
                        pos=LPoint3f(0.575, 0, coords),
                        scale=LVecBase3f(0.1, 0.1, 0.1),
                        text=i,
                        text0_align=TextNode.A_center,
                        text0_scale=(1, 1),
                        text0_pos=(-5.75, 0.0),
                        text0_fg=LVecBase4f(0, 0, 0, 1),
                        text0_bg=LVecBase4f(0, 0, 0, 0),
                        text0_wordwrap=None,
                        text0_font=self.inst_font,
                        parent=self.pg1384,
                    ).setTransparency(0)

            self.accept('esc', self.chat_gui_destroy)  # при нажатии E - убираем это меню

        def choose_server(self, rootParent=None):
            # выбор сервера

            # удаляем элементы меню
            self.pg3083.destroy()
            self.pg27986.destroy()
            self.pg28909.destroy()
            self.pg149.destroy()
            self.pg452.destroy()
            self.pg326.destroy()
            self.pgSingle.destroy()
            self.pgServers.destroy()

            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды

            self.single = False  # отключаем одиночную игру, поскольку когда игрок выбирает сервер одиночная игра ему не нужна

            # рисуем интерфейс
            self.pg471 = DirectScrolledList(
                forceHeight=0.1,
                frameSize=(-0.5, 0.5, -0.01, 0.75),
                hpr=LVecBase3f(0, 0, 0),
                numItemsVisible=5,
                pos=LPoint3f(0.4, 0, 0.05),
                state='normal',
                text='Servers',
                decButton_borderWidth=(0.005, 0.005),
                decButton_hpr=LVecBase3f(0, 0, 0),
                decButton_pos=LPoint3f(-0.45, 0, 0.03),
                decButton_state='disabled',
                decButton_text='Prev',
                decButton_text_align=TextNode.A_left,
                decButton_text_scale=(0.05, 0.05),
                decButton_text_pos=(0, 0),
                decButton_text_fg=LVecBase4f(0, 0, 0, 1),
                decButton_text_bg=LVecBase4f(0, 0, 0, 0),
                decButton_text_wordwrap=None,
                incButton_borderWidth=(0.005, 0.005),
                incButton_hpr=LVecBase3f(0, 0, 0),
                incButton_pos=LPoint3f(0.45, 0, 0.03),
                incButton_text='Next',
                incButton_text_align=TextNode.A_right,
                incButton_text_scale=(0.05, 0.05),
                incButton_text_pos=(0, 0),
                incButton_text_fg=LVecBase4f(0, 0, 0, 1),
                incButton_text_bg=LVecBase4f(0, 0, 0, 0),
                incButton_text_wordwrap=None,
                itemFrame_frameColor=(1, 1, 1, 1),
                itemFrame_frameSize=(-0.47, 0.47, -0.5, 0.1),
                itemFrame_hpr=LVecBase3f(0, 0, 0),
                itemFrame_pos=LPoint3f(0, 0, 0.6),
                text_align=TextNode.A_center,
                text_scale=(0.1, 0.1),
                text_pos=(0, 0.015),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.inst_font,
                parent=rootParent,
            )
            self.pg471.setTransparency(0)

            self.pg820 = DirectScrolledListItem(
                frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, 0),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Admin fun server.',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=self.pg471,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg820.setTransparency(0)

            self.pg839 = DirectScrolledListItem(
                frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, -0.1),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Bosses of game',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=self.pg471,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg839.setTransparency(0)

            self.pg861 = DirectScrolledListItem(
                frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, -0.2),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Hahahahha',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=self.pg471,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg861.setTransparency(0)

            self.pg886 = DirectScrolledListItem(
                frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, -0.3),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Empty',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=self.pg471,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg886.setTransparency(0)

            self.pg914 = DirectScrolledListItem(
                frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, -0.4),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                state='disabled',
                text='Empty',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=self.pg471,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg914.setTransparency(0)

            self.pg2484 = DirectEntry(
                frameSize=(-0.1, 10.1, -0.3962500154972076, 1.087500011920929),
                hpr=LVecBase3f(0, 0, 0),
                initialText='Порт сервера',
                pos=LPoint3f(-13.4, 0, -3.225),
                scale=LVecBase3f(1.5, 1.5, 1),
                text_align=TextNode.A_left,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=self.pg914,
            )
            self.pg2484.setTransparency(0)

            self.pg3545 = DirectButton(
                frameSize=(-2.3, 2.3, -0.213, 0.825),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(7.825, 0, -1.25),
                scale=LVecBase3f(1, 1, 1),
                text='Подключится',
                text_align=TextNode.A_center,
                text_scale=(0.7, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.font,
                parent=self.pg2484,
                command=self.exit_menu3,
                pressEffect=1,
            )
            self.pg3545.setTransparency(0)

            self.pg945 = DirectScrolledListItem(
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, 0),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Empty',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                text_font=self.inst_font,
                parent=self.pg471,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg945.setTransparency(0)

            self.pg471.addItem(self.pg820)
            self.pg471.addItem(self.pg839)
            self.pg471.addItem(self.pg861)
            self.pg471.addItem(self.pg886)
            self.pg471.addItem(self.pg914)
            self.pg471.addItem(self.pg945)

        def _basic_droid(self):
            sending(f'Basic droid! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # Выбор обычного дроида. Он выбран по умолчанию
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()
            self.basic_droid = True
            self.pod_droid = False
            self.shield_droid = False

        def _pod_droid(self):
            sending(f'Pod droid! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # Выбор большого дроида.
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()
            self.pod_droid = True
            self.basic_droid = False
            self.shield_droid = False

        def _shield_droid(self):
            sending(f'Shield droid! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # Выбор дроида с щитом
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()
            self.basic_droid = False
            self.pod_droid = False
            self.shield_droid = True

        def single_player(self, value):
            # Одиночная игра
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды

            self.single = True

        def exit_menu(self):
            sending(f'Exit from chat! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # Выход в меню из чата.
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды
            # Удаляем элементы меню
            self.pg212.destroy()
            self.pg10591.destroy()
            self.pg561.destroy()

            self.menu(False)

        def exit_menu2(self):
            sending(f'Exit from droid choose! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # Выход в меню из из выбора дроида.
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды
            # Удаляем элементы меню
            self.pg188.destroy()
            self.pg4741.destroy()
            self.pg1254.destroy()

            self.menu(False)

        def exit_menu4(self):
            sending(f'Exit from bug sending! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # ВЫход в меню из отправки бага
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды

            # удаляем элементы меню
            self.pg149.destroy()

            self.menu(False)

        def exit_menu3(self):
            sending(f'Exit from server menu! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # ВЫход в меню из серверов
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды
            # Удаляем элементы меню
            self.pg471.destroy()

            self.load_game()  # открываем игру

        def set_lifes(self):
            self.state = self.pg28909.guiItem.getValue() * 100  # загрузим слайдерное значение умноженое на 100, да трачу оптимизацию но мне кажется многим плевать на оптимизацию меню, ибо такого понятия просто нету :)
            self.state_droid = int(self.state // 2)
            self.state = int(self.state // 1)

            sending('Set ' + str(self.state) + f' lifes! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер

        def gb_mode(self, value):
            '''включение чёрнобелого режима'''
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()
            self.GB = True

        def en_lang(self):
            '''Изменение языка на английский'''
            sending(f'EN mode! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()
            self.EN = True

        def pro_system(self):
            '''Проффесиональное управление'''
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()
            self.pro_machine = True  # включаем проффесиональное управление

        def load_game(self):
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук ввода команды

            sending(f'Lgged as {USERNAME}! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер

            # убираем элементы меню
            self.pg3083.destroy()
            self.pg27986.destroy()
            self.pg28909.destroy()
            self.pg438.destroy()
            self.pg326.destroy()
            self.pgSingle.destroy()
            self.pgServers.destroy()
            self.pg452.destroy()

            # все действия над сервером если не включена одиночная игра
            if not self.single:
                self.networking = PythonNetContext()  # сервер
                self.networking.bindSocket(DEFAULT_PORT)  # 'одеваем на сервер' его порт
                self.networking.connectToServer(self.arg_username, self.username)  # коннектим игрока к серверу
                self.networking.clientConnect(self.username)  #ещё коннектим, без аргументов
                self.networking.serverConnect(IP_USER)  # коннектим айпи игрока
                self.networking.addClient(self.username)  # добавляем клиента.
                self.networking.readTick()  # читаем сервер

            else:
                sending(f'Single player! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                s.close()  # закрываем сервер

            # если не выходили скроем глобус
            if not self.exiting:
                self.globe.hide()

            # Ксли включена одиночная игра - убираем кнопку чата
            if self.single:
                self.pg149.destroy()

            # if no single mode
            if not self.single:
                start_client()  # запуск клиента

            # удаляем глобус, если не выходили из игры
            if not self.exiting:
                del self.globe

            # меню оружий
            self.weapon_menu___init__(False)

            self.intro_sound.play()  # играем звук интро

            dt = globalClock.getDt()  # переменная, которая показывает, сколко времени прошло между кадрами

            # меняем настройки, чтобы пользователю казалось, что открыто новое окно
            self.props.setUndecorated(
                False)  # раму мы показываем, но потом полноэкранный режим включается. Зачем это? Просто в panda3d если ты не уберешь одну настройку то она останется и будет влиять на все остальные.
            self.props.setFullscreen(True)  # включаем полноэкранный режим
            self.openDefaultWindow(props=self.props)  # Используем настройки

            # включим специальные шейдеры
            self.sh_framework = pbp.ShadingFramework(self.render)

            self.keyMap = {
                "left": 0, "right": 0, "forward": 0, "cam-left": 0,
                "cam-right": 0}  # Создадим словарь кнопок, по их нажатию

            # Рисуем звёзды

            self.sky = loader.loadModel("./models/sky/solar_sky_sphere")  # загрузим модель космоса(это сфера)

            self.sky_tex = loader.loadTexture("./tex/stars_1k_tex.jpg")  # загрузим текстуру
            self.sky.setTexture(self.sky_tex, 1)  # зарендерим текстуру на небо
            self.sky.reparentTo(render)  # инициализируем небо
            self.sky.setScale(40000)  # расширим небо до максимальной величины panda3d

            self.environ = loader.loadModel("./models/world/falcon.egg")  # Загрузим уже созданный в blender мир.
            self.environ.reparentTo(render)  # Загружаем модель мира в окно

            self.droidStartPos = (-1, 0, 1.5)  # Загружаем стартовую позицию игрока в мире.
            self.enemyStartPos = LVecBase3f(float(self.level[0]), float(self.level[1]),
                                            float(self.level[2]))  # Загружаем позицию помощника-дроида.

            # Примечание : на первых версиях игры этот дроид был ед. врагом, но теперь я сделал его помщником. А имя переменой осталось.

            # если не включена другая камера, то:
            if not self.another_camera:
                if self.basic_droid:  # если включен стандартный дроид, то :
                    self.droid = GameApi.object(self, "./models/BasicDroid/BasicDroid.egg", 1,
                                                self.droidStartPos)  # Загружаем модель игрока
                elif self.pod_droid:  # если включен большой дроид, то :
                    self.droid = GameApi.object(self, "./models/pod/pod.egg", 0.5,
                                                self.droidStartPos)  # загружаем модель большого дроида игрока

                elif self.shield_droid:  # если включен дроид с щитом, то:
                    self.shield_sound.play()  # играем звук щита.
                    self.droid = GameApi.object(self, "./models/BasicDroid/BasicDroid-lowres.egg", 1,
                                                self.droidStartPos)  # Загружаем модель игрока с щитом.

            else:
                self.droid = render.attachNewNode("body")  # подключаем дроида к рендеру
                self.droid.setPos(self.droidStartPos)  # ставим стартовую позицию дроида
                base.cam.reparentTo(self.droid)  # перемещаем камеру в... САМОГО ДРОИДА?!...

            self.enemy = GameApi.object(self, "./models/pod/pod.egg", 0.5,
                                        self.enemyStartPos)  # Загружаем модель помощника (созданная в blender)
            if self.single:  # если включена одиночная игра - убираем дроида помощника
                self.enemy.hide()  # убираем

            self.weapon_pos = self.droid.getX(), self.droid.getY() + 0.7, 1  # Позиция пушки
            self.sword_pos = self.droid.getX(), self.droid.getY() + 0.1, 1  # Позиция мЕча

            self.weapon = GameApi.object(self, './models/BasicDroid/sniper.egg', .5, self.weapon_pos)  # загрузим оружие

            self.bullet = GameApi.object(self, './models/spike/spike.egg', .5, (0, 0, 0))  # Загрузим пулю
            self.flash = GameApi.object(self, './models/whishlyflash/handlamp.egg', .5, (0, 0, 0))  # Загрузим фонарик
            self.planet = GameApi.object(self, './models/pod/pod.egg', 50, (0, -1000, 0))  # загружаем большого дроида
            self.crosshair = GameApi.object(self, './models/crosshair/crosshair.egg', 1,
                                            (self.droidStartPos))  # закружаем щит
            self.grenade = GameApi.object(self, './models/grenade/Grenade.egg', 1, (3, 3, 0.3))  # загружаем гранату
            self.fragment = GameApi.object(self, './models/fragment/Fragment.egg', 1,
                                           (5, 3, 0.3))  # загрудаем фрагмент гранаты

            # вражеский истребитель
            self.fighter = GameApi.object(self, './models/fighter/fighter.egg', 1,
                                          (0, 90, 0))  # загрузим модельку истребителя

            self.cube = GameApi.object(self, './models/block/crate.egg', .7, (0, 0, 0))  # загружаем блок
            self.cube.hprInterval(1.5, (360, 360, 360)).loop()

            self.Intervalcube = self.cube.posInterval(13,
                                                      Point3(0, -1500, 0),
                                                      startPos=Point3(0, 10, 0))  # вращаем ящик(он слетает с корабля)

            self.Intervalcube.loop()  # делаем позу ящика вращением

            # Врашение планеты
            self.planet.hprInterval(550, (360, 360, 0)).loop()  # "поза" вращения планеты

            self.spotlight = camera.attachNewNode(Spotlight("spotlight"))  # Конфиги фонарика
            self.spotlight.node().setColor((.3, .3, .3, 1))  # цвет фонарика
            self.spotlight.node().setSpecularColor((0, 0, 0, 1))  # цвет отражения

            self.floater = NodePath(PandaNode("floater"))  # создаем нод
            self.floater.reparentTo(self.droid)  # подключаем нод к модели дроида игрока
            self.floater.setZ(
                2.0)  # глубина(если вы не понимайте, о чем я, прочитайте в википедии о левосторонней системе координат)

            self.accept("escape", self.exit)  # При нажатии клавиши Esc выходим.

            self.accept("arrow_left", self.setKey, ["left", True])  # При кнопке влево - поворачиваем игрока влево
            self.accept("arrow_right", self.setKey, ["right", True])  # При кнопке вправо - поворачиваем игрока вправо
            self.accept("arrow_up", self.setKey, ["forward", True])  # При кнопке вперёд - идём вперёд
            self.accept("a", self.setKey,
                        ["cam-left", True])  # При кнопке a - разворачиваем камеру вокруг нашей модельки
            self.accept("d", self.setKey,
                        ["cam-right", True])  # При кнопке s - разворачиваем камеру вокруг нашей модельки
            self.accept("arrow_left-up", self.setKey,
                        ["left", False])  # При кнопке вверх+влево - поворачиваем игрока влево и идём вперёд
            self.accept("arrow_right-up", self.setKey,
                        ["right", False])  # При кнопке вверх+право - поворачиваем игрока вправо и идём вперёд
            self.accept("arrow_up-up", self.setKey,
                        ["forward", False])  # При кнопке вверх+вверх - идём вперёд и идём вперёд
            self.accept("a-up", self.setKey,
                        ["cam-left", False])  # При кнопке a+вперёд - поворачиваем камеру влево и идём вперёд
            self.accept("d-up", self.setKey,
                        ["cam-right", False])  # При кнопке s+вперёд - поворачиваем камеру вправо и идём вперёд

            self.accept("space", self.shot)  # при пробеле стреляем
            self.accept("s", self.toggleLights, [[self.spotlight]])  # При кнопке s - включить фонарик
            self.accept("w", self.weapon_hide)  # при кнопке w - уберём оружие.
            self.accept("p", self.cursor)  # при кнопке p - покажем прицел снайпера
            self.accept("g", self.grenade_snade)  # при кнопке g - кидаем гранату

            base.enableParticles()  # Включаем инициализацию дыма
            self.p = ParticleEffect()  # Включим эффект дыма
            self.accept('f',
                        self.particle_start)  # при нажатии f(от force) -  загрузим файл дыма и переместим в конфиг чтобы именно эта анимация стала отображением дыма
            self.accept('0', self.fountain)  # при  нажатии кнопок f+o(fountain) включим пожаротушительную систему
            if self.single:  # если мы находимся в диночной игре, то можно включать полигольный режим.
                self.accept('f3', self.toggleWireframe)  # при нажатии f3 - включаем полигольный режим
            self.accept('r', base.useTrackball)  # если нажали r - делаем RPG режим.

            taskMgr.add(self.move, "moveTask")  # Добавляем задачу в наш движок

            self.capture_flag = Capture_flag(player=self.droid,
                                             base_1=self.environ,
                                             base_2=self.planet)  # запускаем режим захвата флага

            # задачи для нашего рендера, а именно :
            taskMgr.add(self.capture_flag_update, "CaptureFlagUpdating")  # общее обновление режима
            taskMgr.add(self.check_swipe, "CheckingSwipeOnDroid")  # проверка на удар
            taskMgr.add(self.engine_treshiny_check, "TreshinyWithEngineChecking")  # проверка на наличие трещин

            self.isMoving = False  # Ставим значение isMoving на False(Вы можете менять это значение) чтобы игрок изначально стоял.
            # Делаем так, чтобы свет был изначально выключен.
            self.camera.setPos(self.droid.getX(), self.droid.getY() + 1,
                               3)  # Ставим позицию камеры чуть больше позиции игрока

            if not self.EN:  # если язык не английский
                self.state_info = MenuApi.text(self, text='корабль :' + str(self.state), pos=(0.5, 0.8), scale=0.1,
                                               font=self.font)  # Напишем сообщение о состоянии корабля

            else:  # если янглийский язык
                self.state_info = MenuApi.text(self, text='machine :' + str(self.state), pos=(0.5, 0.8), scale=0.1,
                                               font=self.font)  # Напишем сообщение о состоянии корабля

            self.check_loss()  # Проверяем поражение
            self.hide_weapon = False  # Поставим, что оружие не убрано
            self.steam_pos = random.randrange(0, 5), random.randrange(0, 5) + self.speed, random.randrange(0, 5)
            self.fountain_pos = random.randrange(0, 5), random.randrange(0, 5), random.randrange(0, 1)

            self.motor_pos1 = 25.238849639892578, 8.962211608886719, 1.5  # позиция первого мотора
            self.motor_pos2 = -20.676218032836914, 10.55816650390625, 1.5  # позиция второго мотора

            self.motor1 = GameApi.loadParticleConfig(self, './special_effects/steam_critic+/fireish.ptf',
                                                     self.motor_pos1, self.environ)  # мотор 1
            self.motor2 = GameApi.loadParticleConfig(self, './special_effects/steam_critic+/fireish.ptf',
                                                     self.motor_pos2, self.environ)  # мотор 2

            self.state_info2 = MenuApi.text(self, text='', pos=(-0.8, 0.8), scale=0.1,
                                            font=self.font)  # Напишем сообщение о состоянии корабля
            self.state_droid_info = MenuApi.text(self, text=str(self.state_droid), pos=(-1.3, 0.8), scale=0.1,
                                                 font=self.font)  # Напишем сообщение о состоянии дроида

            self.force = False  # Поставим, что не разгонялись

            self.light()  # Свет

            # солнце(новая механика освещения БЫЛА В ФЕВРАЛЕ 2021...)
            GameApi.light(self)

            # списки с обьектами
            self.objects = [self.environ, self.droid,
                            self.enemy, self.weapon,
                            self.bullet, self.flash,
                            self.cube, self.crosshair]

            if cursor_e:  # если курсор показан..
                # все графические обьекты
                self.gui_objects = [self.state_info, self.state_droid_info, self.state_info2,
                                    self.cursor1, self.cursor2, cursor3, cursor4]

            else:  # если не показан
                self.gui_objects = [self.state_info, self.state_droid_info, self.state_info2]  # графические объекты

            # если не включили одиночную игру, добавляем в список графических обьектов кнопку чата
            if not self.single:
                self.gui_objects.append(self.pg149)

            self.enemies = [self.enemy]  # список врагов

            # Генерация врагов
            for e in range(0, 20):
                enemy = GameApi.object(self, './models/pod/pod.egg', 0.5,
                                       (-26 - random.randrange(e, 30), random.randrange(e - 10, e), 1.5))
                self.enemies.append(enemy)

            # если включена одиночная игра удаляем врагов
            for enemy in self.enemies:
                if self.single:
                    enemy.destroy()

            # список гранат
            self.grenades = [
                self.grenade]

            # список фрагментов от гранат
            self.fragments = [
                self.fragment]

            # все обьекты, не поддающиюся эффектам
            self.all_objects = self.objects + self.fragments + self.grenades + [self.sky, self.fighter, self.planet,
                                                                                self.weapon]

            self.rust_texture = loader.loadTexture('./tex/rust.png')  # загружаем текстуру ржавчины
            self.treshiny_texture = loader.loadTexture('./tex/treshiny.png')  # загружаем текстуру трещин

            # Шейдеры
            GameApi.shaders(self, vert="./shaders/realistic/bloom.glsl", frag="./shaders/realistic/blur.glsl")  # blur
            GameApi.shaders(self, vert="./shaders/realistic/outline.glsl",
                            frag="./shaders/realistic/repeat.glsl")  # шейдер для повторения
            GameApi.shaders(self, vert="./shaders/realistic/glow.glsl",
                            frag="./shaders/realistic/grayscale.glsl")  # грайскайл
            GameApi.shaders(self, vert="./shaders/realistic/shadow.frag",
                            frag="./shaders/realistic/shadow.vert")  # тени

            # Если  игрок захотел поиграть в чёрнобелую игру, проверим это
            if self.GB:
                sending(f'Start green-black mode! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                GameApi.shaders(self, "./shaders/lighting.vert", "./shaders/lighting.frag")  # чернобелые шейдеры

        def engine_treshiny_check(self, task):
            '''функция для проверки корабля на трещины'''
            if self.environ.getPos() == self.planet.getPos():  # если корабль врезался в планету...
                self.environ.setTexture(self.treshiny_texture)  # накладываем на него текстуру трещин

        def capture_flag_update(self, task):
            self.result = self.capture_flag.update()  # обновляем результат захвата флага
            if self.result:  # проверяем результат
                sending(f'WIN capture flag! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                print('You WIN!!!')  # печатаем результат
                self.rating += 10  # добавляем очки рейтинга
                update_file(directory_='./profile', filename_p_='rating.txt', value=str(self.rating), name='rating')
                self.start_new_game()  # запускаем новую игру

        def check_swipe(self, task):
            '''проверяем удар по дроиду'''

            if self.droid.getPos() == self.enemy.getPos():  # проверяем : если дроид игрока ударился об вражеского то...
                sending(f'Big swipe! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                if not self.EN:
                    self.state_info.getText('сильный удар!')  # сообщение об ударе
                else:
                    self.state_info.getText('swipe!')

                self.state_droid -= 5  # вычитаем очки из жизней дроида
                self.state_droid_info.setText(str(self.state_droid))  # обновление состояния дроида

        def start_new_game(self):
            sending(f'Started new game {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            '''запуск новой игры'''
            self.droid.setPos(self.droidStartPos)  # ставим обычную позицию дроида
            self.enemy.setPos(self.enemyStartPos)  # ставим обычную позицию врага

        def _grenade_boom(self):
            sending(f'Grenade is boom {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # играем звуки гранаты
            for l in range(0, 10):
                self.grenade_launch.play()  # играем звуки пикания в цикле, т. к. это и будет время чтобы убежать от нее
            self.grenade_boun.play()  # недовзрыв
            self.grenade_boom.play()  # взрыв xDDDDD

            # Добавляем в список гранат гранату(ЛОГИКА:))
            self.grenades.append(self.grenade)
            # Тоже самое со списком фрагментов
            self.fragments.append(self.fragment)

            # оптимизация
            if len(self.grenades) >= 30:
                for grenade in self.grenades:
                    grenade.hide()

            if len(self.fragments) >= 30:
                for fragment in self.fragments:
                    fragment.hide()
                    self.fragments.pop()

        def grenade_snade(self):
            sending(f'Grenade {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # Создаём обьект гранаты рядом с дроидом
            self.grenade = GameApi.object(self, 'models/grenade/Grenade.egg', 1,
                                          (self.droid.getX() - 1, self.droid.getY() - 2, 0))

            # эффект горения
            GameApi.loadParticleConfig(self, './special_effects/steam_critic+/fireish.ptf', self.grenade.getPos(),
                                       self.environ)

            # Создаём фрагмент железа
            self.fragment = GameApi.object(self, 'models/fragment/Fragment.egg', 1,
                                           (self.droid.getX(), self.droid.getY(), 0))
            self.fragment.hide()  # не показываем фрагмент

            # Проверка условия : Если дроид рядом с гранатой, то вылетает железный фрагмент : якобы от дооида.
            if (self.droid.getX() - self.fragment.getX()) < 1 or (self.droid.getY() - self.fragment.getY()) < 1:
                self.fragment.show()  # показываем фрагмент

            self._grenade_boom()  # взрываем гранату

        def light_shader(self):
            '''Включение шейдера горения'''  # *ОН ОЧЕНЬ КРАСИВЫЙ, И ИДЕТ ДАЖЕ НА RX 480 И ВСТРОЕННЫЙ В XEON ГП!*(у меня GTX 1650)
            sending(f'Started light pro shder {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            return Shader.make(Shader.SL_GLSL, vertex="""
                #version 120

                varying vec3 v_FragmentPosition;
                varying vec3 v_FragmentNormal;

                attribute vec2 p3d_MultiTexCoord0;
                attribute vec4 p3d_Vertex;
                attribute vec3 p3d_Normal;

                uniform mat4 p3d_ModelViewProjectionMatrix;

                void main( void )
                {
                    gl_Position    = p3d_ModelViewProjectionMatrix * p3d_Vertex;
                    gl_TexCoord[0].xy = p3d_MultiTexCoord0;

                    v_FragmentPosition  = p3d_Vertex.xyz;
                    v_FragmentNormal  = p3d_Normal;
                }

                """,

                               fragment="""
                #version 120

                uniform sampler2D p3d_Texture0;
                uniform vec3 pos_light;

                uniform mat4 p3d_ViewMatrixInverse;

                varying vec3 v_FragmentPosition;
                varying vec3 v_FragmentNormal;

                const vec4  k_LightColor = vec4(1.0, 0.6, 0.3, 1.0);
                const float k_Shininess = 64.0;

                const float k_ConstAttenuation = 0.5;
                const float k_LinearAttenuation = 0.05;
                const float k_QuadricAttenuation = 0.001;

                void main( void )
                {
                    vec3  L = pos_light - v_FragmentPosition;

                    // ** Used in the calculation of light extinction
                    float distance = length( L );

                    L = normalize( L );
                    vec3  N = normalize( v_FragmentNormal );

                    // ** The H vector is used to calculate the gloss (specularity) of a fragment
                    vec3  E = normalize( p3d_ViewMatrixInverse[3].xyz - v_FragmentPosition );
                    vec3  H = normalize( L + E ); // ** Half-vector

                    // ** The calculation coefficient. attenuations
                    float attenuation = 1.0 / ( k_ConstAttenuation + k_LinearAttenuation * distance + k_QuadricAttenuation * distance * distance );

                    float diffuse = clamp( dot( L, N ), 0.0, 1.0 );
                    float specular  = pow( clamp( dot( N, H ), 0.0, 1.0 ), k_Shininess );

                    if( diffuse <= 0.0 ){
                        specular = 0.0; 
                        }

                    vec4 diffuseColor  = diffuse * k_LightColor * attenuation;
                    vec4 specularColor = specular * k_LightColor * attenuation;
                    vec4 ambientColor = vec4(0.01, 0.01, 0.01, 0.01);
                    vec4 emissionColor = vec4(0.0, 0.0, 0.0, 0.0);

                    gl_FragColor = ( diffuseColor + specularColor + ambientColor + emissionColor) * texture2D(p3d_Texture0, gl_TexCoord[0].xy );
                }
                """)

        def particle_start(self):
            sending(f'Started particle {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            self.command_sound.play()  # играем звук  команды
            if not self.pro_machine:  # если не включено про управление
                self.force = True  # Поставим, что мы уже разгонялись

                self.state -= 1  # сделаем меньше очков
                self.state_info.destroy()  # удалим текстовые очки

                for i in range(len(self.objects)):
                    object = self.objects[i]
                    object.setY(object.getY() - self.speed)

                if self.state != 10 and self.state > 10:
                    self.state_info.destroy()  # убираем предедущее сообщение о жизнях корабля
                    self.state_info = MenuApi.text(self, text='корабль :' + str(self.state), pos=(0.5, 0.8), scale=0.1,
                                                   font=self.font)  # Напишем сообщение о состоянии корабля
                    self.check_loss()  # проверяем поражение
                    self.steam_pos = random.randrange(0, 5), random.randrange(0, 5) - (
                            self.speed - 100), random.randrange(0, 1)
                    GameApi.loadParticleConfig(self, 'special_effects/steam/steam.ptf', self.steam_pos, self.environ)
                    self.errorSound.play()  # играем звук ошибки
                    self.state_info2.destroy()  # убираем предедущее сообщение

                    if not self.EN:
                        self.state_info2 = MenuApi.text(self, text='двигатель неисправен', pos=(-0.8, 0.8), scale=0.1,
                                                        font=self.font)  # Напишем сообщение о состоянии корабля
                    else:
                        self.state_info2 = MenuApi.text(self, text='motor error', pos=(-0.8, 0.8), scale=0.1,
                                                        font=self.font)  # Напишем сообщение о состоянии корабля


                else:
                    self.state_info = MenuApi.text(self, text='корабль :' + str(self.state), pos=(0.5, 0.8), scale=0.1,
                                                   font=self.font)  # Напишем сообщение о состоянии корабля
                    self.check_loss()  # проверяем поражение
                    self.steam_pos = random.randrange(0, 5), random.randrange(0, 5) - (
                            self.speed - 100), random.randrange(0, 1)
                    GameApi.loadParticleConfig(self, 'special_effects/steam_critic/steam.ptf', self.steam_pos,
                                               self.environ)
                    self.errorSound.play()  # играем звук ошибки
                    self.state_info2.destroy()  # убираем предедущее сообщение

                    if not self.EN:
                        self.state_info2 = MenuApi.text(self, text='критическое состояние', pos=(-0.8, 0.8), scale=0.1,
                                                        font=self.font)  # Напишем сообщение о состоянии корабля
                    else:
                        self.state_info2 = MenuApi.text(self, text='critic state', pos=(-0.8, 0.8), scale=0.1,
                                                        font=self.font)  # Напишем сообщение о состоянии корабля

                if self.state < 10:
                    self.alarm_sound.play()
                    self.state_info.destroy()
                    self.state_info = MenuApi.text(self, text='корабль :' + str(self.state), pos=(0.5, 0.8), scale=0.1,
                                                   font=self.font)  # Напишем сообщение о состоянии корабля
                    self.check_loss()  # проверяем поражение
                    self.steam_pos = random.randrange(0, 5), random.randrange(0, 5) - (
                            self.speed - 100), random.randrange(0, 5)

                    GameApi.loadParticleConfig(self, 'special_effects/steam_critic+/fireish.ptf', self.steam_pos,
                                               self.environ)
                    self.errorSound.play()  # играем звук ошибки
                    self.state_info2.destroy()  # убираем предедущее сообщение

                    if not self.EN:
                        self.state_info2 = MenuApi.text(self, text='падаем!', pos=(-0.8, 0.8), scale=0.1,
                                                        font=self.font)  # Напишем сообщение о состоянии корабля
                    else:
                        self.state_info2 = MenuApi.text(self, text='fall!', pos=(-0.8, 0.8), scale=0.1,
                                                        font=self.font)  # Напишем сообщение о состоянии корабля

                    # Вращаем обьекты в колрабле и сам корабль
                    self.environ.hprInterval(50, (360, 360, 0)).loop()
                    self.droid.hprInterval(50, (360, 360, 0)).loop()
                    self.enemy.hprInterval(50, (360, 360, 0)).loop()

            else:
                if not self.EN:
                    self.pro_info = MenuApi.text(self, text='ПРОФИ!', pos=(-0.8, 0.8), scale=0.1,
                                                 font=self.font)  # Напишем сообщение о том что вы профи :)

                else:
                    self.pro_info = MenuApi.text(self, text='PRO!', pos=(-0.8, 0.8), scale=0.1,
                                                 font=self.font)  # Напишем сообщение о том что вы профи :)

                self.pro_machine_engine()

        def pro_machine_engine(self):
            '''Професиональная механика корабля'''
            sending(f'Started Djoystic {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # Тут нужен джойстик. Если его у вас нет, увы вы не сможете использовать этот режим.
            self.mgr = InputDeviceManager.get_global_ptr()
            for device in self.mgr.get_devices():
                self.gamepad = device

            MenuApi.text(self, text=str(self.gamepad), pos=(-1.6, -0.9), scale=0.05,
                         font=self.font)  # найденое устройство

            # Управление джойстиком
            taskMgr.add(self.moveTaskDjoystic, "moveTaskDjoystic")

        def reset(self):
            sending(f'Reseting camera position! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            self.camera.setPosHpr(0, -200, 10, 0, 0, 0)
            self.environ.setPosHpr(0, -200, 9, 0, 0, 0)

        def moveTaskDjoystic(self, task):
            sending(f'Started pro mode of control {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            dt = globalClock.getDt()

            strafe_speed = 85
            vert_speed = 50
            turn_speed = 100

            lstick = self.gamepad.findButton("lstick")
            if lstick.pressed:
                strafe_speed *= 2.0

            strafe = Vec3(0)
            left_x = self.gamepad.findAxis(InputDevice.Axis.left_x)
            left_y = self.gamepad.findAxis(InputDevice.Axis.left_y)
            strafe.x = left_x.value
            strafe.y = left_y.value

            if strafe.lengthSquared() >= 0.01:
                self.camera.setPos(self.camera, strafe * strafe_speed * dt)

            trigger_l = self.gamepad.findAxis(InputDevice.Axis.left_trigger)
            trigger_r = self.gamepad.findAxis(InputDevice.Axis.right_trigger)
            lift = trigger_r.value - trigger_l.value
            self.camera.setZ(self.camera.getZ() + (lift * vert_speed * dt))

            right_x = self.gamepad.findAxis(InputDevice.Axis.right_x)
            right_y = self.gamepad.findAxis(InputDevice.Axis.right_y)

            if abs(right_x.value) >= 0.1 or abs(right_y.value) >= 0.1:
                self.camera.setH(self.camera, turn_speed * dt * -right_x.value)
                self.camera.setP(self.camera, turn_speed * dt * right_y.value)

                self.camera.setR(0)

            return task.cont

        def fountain(self):
            self.state_info2.destroy()  # убираем текст опасности
            sending(f'Started fountain {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            if self.force:
                if self.state != 100:
                    self.state += 1
                    self.state_info.destroy()
                    self.state_info = MenuApi.text(self, text='корабль :' + str(self.state), pos=(0.5, 0.8), scale=0.1,
                                                   font=self.font)  # Напишем сообщение о состоянии корабля

                self.fountain_pos = random.randrange(0, 5), random.randrange(0, 5), random.randrange(0, 1)
                GameApi.loadParticleConfig(self, 'special_effects/fountain/fountain.ptf', self.fountain_pos,
                                           self.environ)
                if self.fountain_pos == self.droid.getPos():
                    self.rust_effect = True  # включаем эффект ржавчины
                    # если не включен английский язык
                    if not self.EN:
                        self.state_info.setText('РЖАВЧИНА!')  # сообщение на русском
                    # если включен английский язык
                    else:
                        self.state_info.setText('RUST!')  # сообщение на русском

                    self.state_droid -= 10  # отнимаем здоровье у дроида
                    self.state_droid_info.setText(str(self.state_droid))  # обновление состояния дроида

                    self.droid.setTexture(self.rust_texture)  # накладываем ржавчину на дроида
                    self.weapon.setTexture(self.rust_texture)  # накладываем ржавчину на оружие

            else:
                if self.state != 100:
                    self.state += 1
                    self.state_info.destroy()
                    if not self.EN:
                        MenuApi.text(self, text='корабль :' + str(self.state), pos=(0.5, 0.8), scale=0.1,
                                     font=self.font)  # Напишем сообщение о состоянии корабля
                    else:
                        MenuApi.text(self, text='machine :' + str(self.state), pos=(0.5, 0.8), scale=0.1,
                                     font=self.font)  # Напишем сообщение о состоянии корабля ON ENGLISH
                    #self.state_info = OnscreenText(text='корабль :' + str(self.state), pos=(0.5, 0.8), scale=0.1, fg=(1, 1, 1, 1), align=TextNode.ALeft, font=self.font) # Напишем сообщение о состоянии корабля

                self.fountain_pos = random.randrange(0, 5), random.randrange(0, 5), random.randrange(0, 1)
                GameApi.loadParticleConfig(self, 'special_effects/fountain/fountain.ptf', self.fountain_pos,
                                           self.environ)

        def light(self):
            # Окрущающее освещение
            ambientLight = AmbientLight("ambientLight")
            ambientLight.setColor((0.2, 0.2, 0.2, 1))
            # освещение, типа от солнца
            directionalLight = DirectionalLight("directionalLight")
            directionalLight.setDirection((-5, -5, -5))
            directionalLight.setColor((1, 1, 1, 1))
            directionalLight.setSpecularColor((1, 1, 1, 1))
            render.setLight(render.attachNewNode(ambientLight))
            render.setLight(render.attachNewNode(directionalLight))

        def weapon_hide(self):
            sending(f'Weapon hided! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # Убрать оружие
            self.change_weapon_sound.play()
            self.hide_weapon = True
            self.weapon.hide()

        def toggleLights(self, lights):
            # Специализированное освещение
            if self.hide_weapon:
                for light in lights:
                    if render.hasLight(light):
                        render.clearLight(light)
                    else:
                        render.setLight(light)

                self.flash.setPos(self.weapon_pos)
            else:
                return

        def shot(self):
            '''выстрел'''
            sending(f'Shot! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            dt = globalClock.getDt() + 0.5  # Cкорость движения
            if not self.hide_weapon:  # если оружие убрано то мы не можем стрелять
                self.shotSound.play()  # играем звук выстрела
                self.bullet.setPos(self.weapon_pos)  # Пуля будет спавнится внутри пушки
                self.bullet.setY(self.bullet, 100 * dt)  # Сдвигаем пулю на огромной скорости вперёд

                for object_ in self.objects:  # проверяем попадание пули по какому либо объекту
                    if object_ != self.droid and object_ != self.weapon and object_ != self.bullet:  # если обьект это не сам дроид не оружие и не сама пуля...
                        if self.bullet.getY() == object_.getY() or self.bullet.getX() == object_.getX():  # проверяем позицию
                            object_.hide()  # если попали - объект удаляется
            else:
                self.kamikaze_sound.play()  # а если оружия нет, включаем камикадзе

        def check_loss(self):
            if self.state == 0:  # если жизней у корабля не осталось
                self.weapon_hide()  # уберём оружие
                if not self.EN:
                    self.info = MenuApi.text(self, text='поражение', font=self.font,
                                             pos=(-1.3, -0.5), scale=0.3)  # напишем о поражении
                    sending(f'Loss! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                else:
                    sending(f'Loss! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                    self.info = MenuApi.text(self, text='LOSS', font=self.font,
                                             pos=(-1.3, -0.5), scale=0.3)  # напишем о поражении
                self.crackSound.play()  # играем звук взрыва

        def check_win(self):
            '''Проверка победы'''
            if (self.droid.getX(), self.droid.getY()) == (self.planet.getX(), self.planet.getY()):
                sending(f'Win! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                if not self.EN:
                    self.info = MenuApi.text(self, text='победа', font=self.font,
                                             pos=(-1.3, -0.5), scale=0.3)  # пишем о победе(на рус)

                    self.rating += 5  # добавляем рейтинга
                    update_file(directory_='./profile', filename_p_='rating.txt', value=str(self.rating),
                                name='rating')  # обновляем игровое значение рейтинга
                else:
                    self.info = MenuApi.text(self, text='WIN', font=self.font,
                                             pos=(-1.3, -0.5), scale=0.3)  # пишем о победе
                    self.rating += 5  # добавляем рейтинга
                    update_file(directory_='./profile', filename_p_='rating.txt', value=str(self.rating),
                                name='rating')  # обновляем игрвое значение рейтинга

        def cursor(self):
            global cursor1, cursor2, cursor3, cursor4, cursor_e  # делаем курсор глобальным
            sending(f'Started pro sniper! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # Рисуем прицел
            cursor1 = OnscreenText(text="||", style=1, fg=(1, 1, 1, 1), pos=(0.0, 0.03), align=TextNode.ARight,
                                   scale=.07)  # часть курсора 1
            cursor2 = OnscreenText(text="||", style=1, fg=(1, 1, 1, 1), pos=(0.0, -0.05), align=TextNode.ARight,
                                   scale=.07)  # часть курсора 2
            cursor3 = OnscreenText(text="==", style=1, fg=(1, 1, 1, 1), pos=(-0.03, 0.0), align=TextNode.ARight,
                                   scale=.07)  # часть курсора 3
            cursor4 = OnscreenText(text="==", style=1, fg=(1, 1, 1, 1), pos=(0.055, 0.0), align=TextNode.ARight,
                                   scale=.07)  # часть курсора 4

            # Перемещаем камеру рядом со снайпером
            self.camera.setPos(self.weapon.getX(), self.weapon.getY(), self.weapon.getZ())

            # курсор теперь есть
            cursor_e = True  # я же говорил, что есть!

            return

        def easy_exit(self):
            sending(f'Exited! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            # обычный выход(из меню)
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды
            sys.exit()  # просто системно выходим.

        def exit(self):
            # Выход из игры
            self.click_sound.play()  # играем звук клика
            self.command_sound.play()  # играем звук команды

            # проверим, включена ли одиночная игра
            if not self.single:
                self.networking.removeClient(self.username)  # удаляем игрока с сервера

            self.exiting = True  # поставим, что уже вышли из игры

            for o in self.all_objects:  # удаляем все модели(абсолютно все)
                o.hide()
            for g in self.gui_objects:  # удаляем все графuческие обьекты
                g.destroy()

            self.pistol_weapon.destroy()  # удаляем меню оружий

            self.menu(True)  # выходим в меню

        def setKey(self, key, value):
            sending(f'Keys complete! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            self.keyMap[key] = value  # Делаем мехaнuзм нажатия клавиш.

        def move(self, task):
            sending(f'Moving! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
            ''' Делаем фуцнкцию движения игрока '''

            dt = globalClock.getDt() - .005  # Cкорость движения

            # Поворот камеры влево и вправо

            if self.keyMap["cam-left"]:
                sending(f'Left camera! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                self.camera.setX(self.camera,
                                 -10 * dt)  # Меняем положеника камеры по икс. Таким образом получается илюзия поворота угла луча. Но на самом деле камера просто перемещается.
            if self.keyMap["cam-right"]:
                sending(f'Right camera! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                self.camera.setX(self.camera, + 10 * dt)  # Тоже самое, что и наверху.

            startpos = self.droid.getPos()  # Сделаем удобную переменную позиции игрока

            if self.keyMap["left"]:
                sending(f'Rotate left droid! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                if not self.rust_effect:
                    self.droid.setH(self.droid.getH() + 145 * dt)
                    self.crosshair.setH(self.crosshair.getH() + 145 * dt)
                    self.weapon.setH(self.weapon.getH() + 145 * dt)
                    self.enemy.setY(self.enemy, -1 * dt)
                    sending(self.droid.getPos())  # отправляем позицию дроида

                if self.rust_effect:  # если дроид заржавел, ...
                    sending(f'Rotate left droid with rust! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                    self.droid.setH(self.droid.getH() + 85 * dt)
                    self.crosshair.setH(self.crosshair.getH() + 85 * dt)
                    self.weapon.setH(self.weapon.getH() + 85 * dt)
                    self.enemy.setY(self.enemy, -1 * dt)
                    sending(self.droid.getPos())  # отправляем позицию дроида

                # движение врагов
                for e in self.enemies:
                    sending(f'Moving enemy {e}! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                    bot(enemy=e, dt=dt)

            if self.keyMap["right"]:
                sending(f'Rotate right droid! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                if not self.rust_effect:
                    self.droid.setH(self.droid.getH() - 145 * dt)
                    self.crosshair.setH(self.crosshair.getH() - 145 * dt)
                    self.weapon.setH(self.weapon.getH() - 145 * dt)
                    self.enemy.setY(self.enemy, -1 * dt)
                    sending(self.droid.getPos())  # отправляем позицию дроида

                if self.rust_effect:  # если дроид заржавел, ...
                    sending(f'Rotate right droid with rust! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                    self.droid.setH(self.droid.getH() - 85 * dt)
                    self.crosshair.setH(self.crosshair.getH() - 85 * dt)
                    self.weapon.setH(self.weapon.getH() - 85 * dt)
                    self.enemy.setY(self.enemy, -1 * dt)
                    sending(self.droid.getPos())  # отправляем позицию дроида

                # движение врагов
                for e in self.enemies:
                    bot(enemy=e, dt=dt)

            if self.keyMap["forward"]:
                sending(f'Forward moving droid! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                if not DEVELOP_MODE:
                    sending(
                        f'Forward moving droid without DEVELOP mode! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                    self.droid.setY(self.droid, -25 * dt)  # перемещаем дроида
                    self.crosshair.setY(self.crosshair, -25 * dt)  # перемещаем круг над дроидом
                    self.enemy.setX(self.enemy, 1 * dt)  # перемещаем врага
                    self.check_win()  # Проверяем победу
                    sending(self.droid.getPos())  # отправляем позицию дроида

                    if self.rust_effect:  # если дроид заржавел, ...
                        sending(
                            f'Forward moving droid with DEVELOP mode and rust effect! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                        self.droid.setY(self.droid, -10 * dt)  # перемещаем дроида
                        self.crosshair.setY(self.crosshair, -10 * dt)  # перемещаем круг над дроидом
                        self.enemy.setX(self.enemy, 1 * dt)  # перемещаем врага
                        self.check_win()  # Проверяем победу
                        sending(self.droid.getPos())  # отправляем позицию дроида

                else:
                    sending(
                        f'Forward moving droid with DEVELOP mode! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                    self.droid.setY(self.droid, -55 * dt)
                    self.crosshair.setY(self.crosshair, -55 * dt)
                    sending(self.droid.getPos())  # отправляем позицию дроида

                # движение врагов
                for e in self.enemies:
                    sending(f'Enemy moving {e}! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                    bot(enemy=e, dt=dt)

                # Сделаем специальное условие проверки убрано оружие или нет
                if not self.hide_weapon:
                    # sending(f'Update weapon position! {IP_USER}:{DEFAULT_PORT}') # отправляем сообщение на сервер
                    self.weapon_pos = self.droid.getX(), self.droid.getY() + 0.7, 3  # Позиция снайпера
                    self.weapon.setPos(self.weapon_pos)  # Обновляем позицию снайпера
                else:
                    sending(f'Update flash position! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
                    self.weapon_pos = self.droid.getX(), self.droid.getY() + 0.7, 3  # Снова вычесляем позицию снайпера
                    self.flash.setPos(self.weapon_pos)  # ставим фонарик на место снайпера

            if not self.another_camera:
                camvec = self.droid.getPos() - self.camera.getPos()  # вектор камеры
                camvec.setZ(0)  # 0 высота вектора
                camdist = camvec.length()  # дистанция камеры от дроида
                camvec.normalize()  # нормализируем вектор камеры
                if camdist > 10.0:  # если дистанция камеры больше 10, то смещаем камеру за дрооидом
                    self.camera.setPos(self.camera.getPos() + camvec * (camdist - 10))
                    camdist = 10.0  # теперь дистанция будет снова 10
                if camdist < 5.0:  # если дистагцтя камеры меньше 5, то...
                    self.camera.setPos(self.camera.getPos() - camvec * (5 - camdist))  # сдвигаем камеру
                    camdist = 5.0  # всё обновляем

                self.camera.lookAt(self.floater)  # вот и пригодился наш floater

            return task.cont  # возвращаем задачу

        # прочие важные функции движка
        def important_func(self):
            '''тут будет какая-то важная функция'''
            pass

    for addon_class in addon_classes:  # проходимся по всем аддонам
        sending(f'Loading addons! {IP_USER}:{DEFAULT_PORT}')  # отправляем сообщение на сервер
        exec("addon_class().run()")  # выполняем их

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()  # поза :)
        loop.run_until_complete(start())  # раним  задачи

except Exception as e:
    import src.ipgetter as ipgetter  # импорт получателя айпи
    from src.settings import *  # импорт настроек

    only_for_error()  # если ошибка
    message(f'''
            [EN] Droid Game {VERSION_}(running on {IP_USER_}:{DEFAULT_PORT_}) is down. 
            Restart the game and try again. If the error persists -
            go to the main menu of the game, and click "Bug?", in which describe the problem:
                1. When did the error occur?
                2. Your processor (number of threads, cores, frequency, model)
                3. Your video card (model name, memory size)
                4. Screenshot/video.
            After that, wait for an answer. Good luck!
            [RU] Droid Game {VERSION_}(работающий на {IP_USER_}:{DEFAULT_PORT_}) упал.
            Перезапустите программу и попробуйте снова. Если ошибка повторится - 
            зайдите в главное меню игры, и нажмите "Bug?", в котором опишите проблему:
                1. Когда произошла ошибка?
                2. Ваш процессор(кол-во потоков, ядер, частота, модель)
                3. Ваша видеокарта(название модели, объем памяти)
                4. Скриншот/видео.
            После этого ждите ответа. Желаем удачи!
            Error:
                {e}
            ''')  # выводим сообщение

