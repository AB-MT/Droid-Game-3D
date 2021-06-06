#!/usr/bin/env python
# -*- coding: utf_8 -*-

# Создано : 22 число, январь, 2021 год

# Импортируем все необходимые инструменты интерфейса

from direct.gui import DirectGuiGlobals as DGG

from direct.showbase.ShowBase import ShowBase
from direct.particles.ParticleEffect import ParticleEffect
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *

from direct.gui.DirectScrolledList import DirectScrolledList
from direct.gui.DirectScrolledList import DirectScrolledListItem
from direct.gui.DirectScrolledFrame import DirectScrolledFrame

from direct.gui.DirectDialog import OkDialog
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectSlider import DirectSlider

from direct.distributed.PyDatagram import PyDatagram # PyDatagram - простой встроенный модуль в движок для создания онлайна

# Ну, вот, импортируем panda3d(игр. движ.) ну и мой небольшой API к нему - marconit_engine
from online.client import *
from panda3d.core import *
from src.marconit_engine import *
from src.bot import bot
from src.net import *
from src.parsers.loading_levels import *
from src.parsers.download_levels import downloading
from src.settings import *
import src.gui as gui
from src.GUI.choose_server import *
from src.GUI.top_players import *
from src.GUI.developers import *
from src.GUI.moderators import *
from src.GUI.message import *
from src.GUI.choose_site import *
import src.audio as audio
import src.pbp as pbp
import src.ipgetter as ipgetter
import random
import sys
import time
from datetime import datetime
import os
import math
import simplepbr # simple PBR light.
import logging
from multiprocessing import Pool # хочу отметить этот модуль - он позволяет работать программе на разных потоках. Из-за этого игра достаточно оптимизирована
from screeninfo import get_monitors
import socket

# For addons
import json

sites = ['github.com', 'panda3d.org', 'a3p.sf.net']

config = json.load(open("./addon_config.json"))
addon_classes = []
for addon in config:
    if not config[addon]["disabled"]:
        exec("from addons." + addon + ".main  import *")
        addon_classes.append(config[addon]["main_class"])

message(message='For playing check you internet!') # message
# connect to site
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((site(sites[1]), 80))
s.send(b'Connected by Droid Game ')
s.close()

# Записываем все сообщения в файл logs.txt будут записыватся : имя уровня, время, само сообщение
logging.basicConfig(
    filename="logs.txt",
    format="[%(levelname)s] %(asctime)s: %(message)s",
    level=logging.INFO,
)

loadPrcFileData('', 'show-frame-rate-meter 1') # показываем количество кадров в секунду
loadPrcFileData(
    "",
    "audio-library-name "
    + ("p3openal_audio" if sys.platform == "linux" else "p3fmod_audio"),
) # система звука в зависимости от вашей ОС
loadPrcFileData("", "threading-model Cull/Draw") # используем Render Pipeline(https://github.com/tobspr/RenderPipeline) для большей риалистичности

def load_profile(filename_p):
    '''загружаем профиль'''
    with open(filename_p) as f: # загружаем файл с профилем
        for line in f: # читаем линии в файле
            return line + str(random.randrange(0, 1500)) # возвращаем имя игрока
        
USERNAME = load_profile('./RES/profile.txt') # загружаем профиль

# start client on server
def start_client():
    worldClient = Client(9099,ipgetter.myip())
    N = PlayerReg()
    keys = Keys()
    w = World()
    chatReg = chatRegulator(worldClient,keys)

def showHelpInfo():
    # Говорим пользователю об использованию
    print('Droid Game ' + VERSION + ' - ' + COPYRIGHT) # информация о игре
    print('Использование(Usage):') # использование
    print('-d \t\t\Режим разробтчика(Developer mode)') # тут всё написано
    print('-l \t\t\Скачать уровни(Download levels)') # и тут тоже
    sys.exit() # выходим

# если пользователю интересно, как пользоватся программой, говорим ему об этом
if "-h" in sys.argv or "/?" in sys.argv or "--help" in sys.argv:
    showHelpInfo() # показываем нформацию

# если пользователь указал аргумент режима разроботчика, вкл. его
elif '-d' in sys.argv:
    DEVELOP_MODE = True

# если пользователь указал аргумент скачивания уровней, скачиваем уровни
elif '-l' in sys.argv:
    downloading()

class Capture_flag():
    def __init__(self, player, base_1, base_2):
        self.player = player
        self.base_1 = base_1
        self.base_2 = base_2
        
        self.player_pos = self.player.getPos()
        self.base_1_pos = base_1.getPos()
        self.base_21_pos = base_2.getPos()

    def update(self):
        self.player_pos = self.player.getPos()
        self.base_1_pos = self.base_1.getPos()
        self.base_2_pos = self.base_2.getPos()

        if self.player_pos == self.base_2_pos:
            return True

        if self.player_pos == self.base_1_pos:
            return False
        

# Создадим главный класс нашей игры
class DroidShooter(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) # Загружаем все селфы из direct
        self.speed = 100 # скорость двигателя
        self.GB = False # НЕ чёрно-белый режим
        self.EN = False # Не будем включать английский язык
        self.basic_droid = True
        self.pod_droid = False
        self.shield_droid = False
        self.pro_machine = False # Не включаем проффесиональное управление
        self.single = False # Не включаем одиночную игру
        self.sun_interval = 80 # Интервал солнца
        self.exiting = False # Поставим, что ещё не выходили из игры
        self.another_camera = False # не включаем вид от первого лица
        self.arg_username = 'd' # аргументы игрока
        self.username = USERNAME # имя игрока

        self.level = load_level(LEVEL1) # уровень по умолчанию
        
        for monitor in get_monitors():
            self.screen_width = monitor.width - 700
            self.screen_height = monitor.height - 400

        self.menu(False) # зaпуск меню
        
    def menu(self, menu, rootParent=None):

        # Настраиваем окно
        self.props = WindowProperties() # класс настроек
        self.props.setTitle('Droid Game release ' + VERSION) # заголовок окна
        self.props.setUndecorated(True) # убираем раму окна
        self.props.setSize(self.screen_width, self.screen_height) # размер окна

        self.openDefaultWindow(props=self.props) # Используем настройки
        
        base.enableParticles() # инициализируем эффект дыма
        self.disableMouse() # Отключаем перемещение через мышку

        self.win.setClearColor((0.5, 0.5, 0.8, 1)) # Закрашиваем поверхность чёрным. Дело в том, что по умолчанию в этом игровом движке поверхность закрашивается серым.
        self.font = loader.loadFont('./fonts/doom_font.ttf') # загрузим шрифт из игры doom
        self.inst_font = loader.loadFont('./fonts/arial.ttf') # загрузим шрифт arial

        self.crackSound = audio.FlatSound('./sounds/glass-shatter1.ogg') # звук взрыва корабля
        self.shotSound = audio.FlatSound('./sounds/sniper-rifle.ogg') # звук выстрела
        self.errorSound = audio.FlatSound('./sounds/reload.ogg') # звук запуска
        self.click_sound = audio.FlatSound('./sounds/click.ogg') # звук нажатия
        self.command_sound = audio.FlatSound('./sounds/command.ogg') # звук команды
        self.kamikaze_sound = audio.FlatSound('./sounds/kamikaze-special.ogg') # звук опасности
        self.alarm_sound = audio.FlatSound('./sounds/alarm.ogg') # звук опасности
        self.change_weapon_sound = audio.FlatSound('./sounds/change-weapon.ogg') # звук перемены оружия
        self.shield_sound = audio.FlatSound('./sounds/shield.ogg') # звук щита

        self.grenade_boom = audio.FlatSound('./sounds/grenade.ogg') # звук гранаты
        self.grenade_boun = audio.FlatSound('./sounds/grenade-bounce.ogg') # звук таймера гранаты
        self.grenade_launch = audio.FlatSound('./sounds/grenade-launch.ogg') # звук взрыва гранаты
        
        self.BgSound = audio.FlatSound(
            "sounds/background.ogg", volume=.01) # фоновая музыка в меню
        self.intro_sound = audio.FlatSound('./sounds/intro.ogg', volume=.01) # звук интро

        self.BgSound.play() # играем звук запуска игры

        # Планета
        if not menu: # Если не входили в чат или инструменты рисуем планету.
            self.camera_distation = random.randrange(20, 30) # дистанция камеры от планеты. генерируем её рандомно в диапозоне от 20 до 30            
            self.globe = loader.loadModel("menu/Globe") # загружаем модель планеты
            self.globe.reparentTo(render) # инициализируем модель
            self.globe.setTransparency(TransparencyAttrib.MAlpha) # прозрачность
            self.globe.setColor(Vec4(1, 1, 1, 0.6)) # цвет
            self.globe.setTwoSided(True) # двойная модель
            self.globe.setRenderModeWireframe() # полигольный режим

            # Врашение планеты
            self.globe.hprInterval(200, (360, 360, 0)).loop()

            self.camera.setPos(0, -self.camera_distation, 0) # камера
            
        # P. S. Это меню я не писал. Оно сделано на DirectGUIDesigner
        self.pg3083 = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.675, 0, 0.15),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Login',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=rootParent,
            command=self.load_game,
            pressEffect=1,
        )
        self.pg3083.setTransparency(0)

        self.pg7785 = DirectLabel(
            frameSize=(-3.15, 3.25, -0.113, 0.725),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(2.9, 0, 3.025),
            scale=LVecBase3f(1, 1, 1),
            text='Droid Game',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg3083,
        )
        self.pg7785.setTransparency(0)

        self.pg8620 = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-2.95, 0, -4.2),
            scale=LVecBase3f(1, 1, 1),
            text='Quit',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg7785,
            command=self.easy_exit,
            pressEffect=1,
        )
        self.pg8620.setTransparency(0)

        self.pg19052 = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(10.075, 0, 2.425),
            scale=LVecBase3f(1, 1, 1),
            text='PRO',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
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

        self.pg29670 = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.625, 0, -0.45),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='EN',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg28909,
            pressEffect=1,
            command=self.en_lang,
        )
        self.pg29670.setTransparency(0)

        self.pg30019 = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.05, 0, -2.55),
            scale=LVecBase3f(1, 1, 1),
            text='GB',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg29670,
            command=self.gb_mode,
            pressEffect=1,
        )
        self.pg30019.setTransparency(0)

        self.pgServers = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(1.3, 0, -0.575),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Servers',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=rootParent,
            command=self.choose_server,
            pressEffect=1,
        )

        self.pg149 = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(1.3, 0, -0.675),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Chat',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=rootParent,
            command=self.open_chat,
            pressEffect=1,
        )
        self.pg149.setTransparency(0)

        self.pg438 = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -1.15),
            scale=LVecBase3f(1, 1, 1),
            text='Droid',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg149,
            command=self.select_droid,
            pressEffect=1,
        )
        self.pg438.setTransparency(0)
        self.pgSingle = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -1.15),
            scale=LVecBase3f(1, 1, 1),
            text='Single',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg438,
            command=self.single_player,
            pressEffect=1,
        )
        self.pg438.setTransparency(0)

        self.pg326 = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 4.500),
            scale=LVecBase3f(1, 1, 1),
            text='Help',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pgSingle,
            pressEffect=1,
            command=self.direction_show,
        )
        self.pg326.setTransparency(0)

        self.pgTutorial = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 5.500),
            scale=LVecBase3f(1, 1, 1),
            text='Tutorial',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pgSingle,
            pressEffect=1,
            command=self.choose_level,
        )
        self.pg326.setTransparency(0)

        self.pgTop = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 6.500),
            scale=LVecBase3f(1, 1, 1),
            text='Top',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pgSingle,
            pressEffect=1,
            command=self.open_top_gui,
        )
        self.pgTop.setTransparency(0)

        self.pgDevelopers = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 7.500),
            scale=LVecBase3f(1, 1, 1),
            text='Developers',
            text_align=TextNode.A_center,
            text_scale=(0.5, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pgSingle,
            pressEffect=1,
            command=self.open_developers_gui,
        )
        self.pgTop.setTransparency(0)

        self.pgModerators = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 8.500),
            scale=LVecBase3f(1, 1, 1),
            text='Moderators',
            text_align=TextNode.A_center,
            text_scale=(0.5, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pgSingle,
            pressEffect=1,
            command=self.open_moderators_gui,
        )
        self.pgTop.setTransparency(0)  

        self.pg452 = DirectButton(
            frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
            hpr=LVecBase3f(0.111, 11, 1111),
            pos=LPoint3f(0.725, 0, 0.65),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Bug?',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=rootParent,
            pressEffect=1,
            command=self.bug_message,
        )
        self.pg452.setTransparency(0)

        self.accept("escape", sys.exit) # При нажатии клавиши Esc выходим.

    def open_top_gui(self):
        # Удаляем элементы меню
        self.pg3083.destroy()
        self.pg27986.destroy()
        self.pg28909.destroy()
        self.pg149.destroy()
        self.pg452.destroy()
        self.pg326.destroy()
        self.pgSingle.destroy()
        self.pgServers.destroy()
        
        self.top_players_gui = GUI(USERNAME) # загружаем интерфейс который прописан в файле

        self.accept('e', self.top_players_gui_destroy) # при нажатии E - убираем это меню

    def open_developers_gui(self):
        # Удаляем элементы меню
        self.pg3083.destroy()
        self.pg27986.destroy()
        self.pg28909.destroy()
        self.pg149.destroy()
        self.pg452.destroy()
        self.pg326.destroy()
        self.pgSingle.destroy()
        self.pgServers.destroy()
        
        self.developers_gui = GUI_2() # загружаем интерфейс который прописан в файле

        self.accept('e', self.developers_gui_destroy) # при нажатии E - убираем это меню

    def open_moderators_gui(self):
        # Удаляем элементы меню
        self.pg3083.destroy()
        self.pg27986.destroy()
        self.pg28909.destroy()
        self.pg149.destroy()
        self.pg452.destroy()
        self.pg326.destroy()
        self.pgSingle.destroy()
        self.pgServers.destroy()

        self.moderators_gui = GUI_3() # загружаем интерфейс который прописан в файле
        
        self.accept('e', self.moderators_gui_destroy) # при нажатии E - убираем это меню        

    def moderators_gui_destroy(self):
        self.moderators_gui.hide() # убираем интерфейс модераторов

        self.menu(False) # открываем меню

    def top_players_gui_destroy(self):
        self.top_players_gui.destroy() # убираем интерфейс топовых игроков

        self.menu(False) # открываем меню
        
    def developers_gui_destroy(self):
        self.developers_gui.destroy() # убираем интерфейс разроботчиков

        self.menu(False) # открываем меню
        
    def direction_show(self):
        '''показ управления'''
        gui.mainloop_direction()
    
    def choose_level(self, rootParent=None):
        # выбор уровня

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

    def one_level(self):
        # включение первого уровня
        self.level = load_level(LEVEL1)
        # удаляем элементы
        self.pg149.hide()
        self.menu(False) # включим menu

    def two_level(self):
        # включение второго уровня
        self.level = load_level(LEVEL2)
        # удаляем элементы
        self.pg149.hide()
        self.menu(False) # включим menu
    
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
            parent=rootParent,
            pressEffect=1,
            command=self.exit_menu2
        )
        self.pg4741.setTransparency(0)

        self.pg1254 = OkDialog(
            frameSize=(-0.22899998878128827, 0.22899998878128827, -0.3417499961704016, 0.19224999830126763),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.075, 0.1, 0.025),
            state='normal',
            text='Default basic droid',
            Button0_text_align=TextNode.A_center,
            Button0_text_scale=(0.06, 0.06),
            Button0_text_pos=(0, 0),
            Button0_text_fg=LVecBase4f(0, 0, 0, 1),
            Button0_text_bg=LVecBase4f(0, 0, 0, 0),
            Button0_text_wordwrap=None,
            text_align=TextNode.A_left,
            text_scale=(0.05, 0.06),
            text_pos=(-0.21, -0.013),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=rootParent,
        )
        self.pg1254.setTransparency(0)

    def open_chat(self, rootParent=None):
            # Чат

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
            self.pg212 = DirectScrolledFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(-1.0, 0.0, -1.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0.2, 0, 0.475),
            scrollBarWidth=0.08,
            state='normal',
            horizontalScroll_borderWidth=(0.01, 0.01),
            horizontalScroll_frameSize=(-0.05, 0.05, -0.04, 0.04),
            horizontalScroll_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_pos=LPoint3f(0, 0, 0),
            horizontalScroll_decButton_borderWidth=(0.01, 0.01),
            horizontalScroll_decButton_frameSize=(-0.05, 0.05, -0.04, 0.04),
            horizontalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_decButton_pos=LPoint3f(-0.96, 0, -0.96),
            horizontalScroll_incButton_borderWidth=(0.01, 0.01),
            horizontalScroll_incButton_frameSize=(-0.05, 0.05, -0.04, 0.04),
            horizontalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_incButton_pos=LPoint3f(-0.12, 0, -0.96),
            horizontalScroll_thumb_borderWidth=(0.01, 0.01),
            horizontalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_thumb_pos=LPoint3f(-0.8326, 0, -0.96),
            verticalScroll_borderWidth=(0.01, 0.01),
            verticalScroll_frameSize=(-0.04, 0.04, -0.05, 0.05),
            verticalScroll_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_pos=LPoint3f(0, 0, 0),
            verticalScroll_decButton_borderWidth=(0.01, 0.01),
            verticalScroll_decButton_frameSize=(-0.04, 0.04, -0.05, 0.05),
            verticalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_decButton_pos=LPoint3f(-0.04, 0, -0.04),
            verticalScroll_incButton_borderWidth=(0.01, 0.01),
            verticalScroll_incButton_frameSize=(-0.04, 0.04, -0.05, 0.05),
            verticalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_incButton_pos=LPoint3f(-0.04, 0, -0.88),
            verticalScroll_thumb_borderWidth=(0.01, 0.01),
            verticalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_thumb_pos=LPoint3f(-0.04, 0, -0.1674),
            parent=rootParent,
            )
            self.pg212.setTransparency(0)

            self.pg3921 = DirectLabel(
                frameColor=(1.0, 1.0, 1.0, 1.0),
                frameSize=(-1.149999976158142, 1.25, -0.11250001192092896, 0.7250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.875, 0, 0),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Chat',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg212,
            )
            self.pg3921.setTransparency(0)

            self.pg5388 = DirectEntry(
                frameSize=(-0.1, 10.1, -0.396, 1.088),
                hpr=LVecBase3f(0, 0, 0),
                initialText='',
                pos=LPoint3f(-1.175, 0, -8.925),
                scale=LVecBase3f(0.9, 0.9, 0.7),
                text_align=TextNode.A_left,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg3921,
            )
            self.pg5388.setTransparency(0)

            self.pg10591 = DirectButton(
                frameSize=(-1.5249999523162843, 1.6499999523162843, -0.21250001192092896, 0.8250000238418579),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(-0.975, 0, 0.5),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='Exit',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=rootParent,
                command=self.exit_menu,
                pressEffect=1,
            )
            self.pg10591.setTransparency(0)

            self.pg561 = DirectScrolledList(
                forceHeight=0.1,
                frameSize=(-0.5, 0.5, -0.01, 0.75),
                hpr=LVecBase3f(0, 0, 0),
                numItemsVisible=5,
                pos=LPoint3f(0.725, 0, -0.3),
                state='normal',
                text='Connect',
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
                incButton_state='disabled',
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
                parent=rootParent,
            )
            self.pg561.setTransparency(0)

            self.pg1809 = DirectScrolledListItem(
                frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, 0),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                state='disabled',
                text='Marcim_HACKER',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg561,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg1809.setTransparency(0)

            self.pg1852 = DirectScrolledListItem(
                frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, -0.1),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='BOT',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg561,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg1852.setTransparency(0)

            self.pg1898 = DirectScrolledListItem(
                frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, -0.2),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='BOT',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg561,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg1898.setTransparency(0)

            self.pg1947 = DirectScrolledListItem(
                frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, -0.3),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='BOT',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg561,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg1947.setTransparency(0)

            self.pg1999 = DirectScrolledListItem(
                frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
                hpr=LVecBase3f(0, 0, 0),
                pos=LPoint3f(0, 0, -0.4),
                scale=LVecBase3f(0.1, 0.1, 0.1),
                text='System',
                text_align=TextNode.A_center,
                text_scale=(1, 1),
                text_pos=(0, 0),
                text_fg=LVecBase4f(0, 0, 0, 1),
                text_bg=LVecBase4f(0, 0, 0, 0),
                text_wordwrap=None,
                parent=self.pg561,
                command=base.messenger.send,
                extraArgs=['select_list_item_changed'],
            )
            self.pg1999.setTransparency(0)

            self.pg561.addItem(self.pg1809)
            self.pg561.addItem(self.pg1852)
            self.pg561.addItem(self.pg1898)
            self.pg561.addItem(self.pg1947)
            self.pg561.addItem(self.pg1999)

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

        self.single = False # отключаем одиночную игру, поскольку когда игрок выбирает сервер одиночная игра ему не нужна
        
        # рисуем интерфейс
        self.pg471 = DirectScrolledList(
            forceHeight=0.1,
            frameSize=(-0.5, 0.5, -0.01, 0.75),
            hpr=LVecBase3f(0, 0, 0),
            numItemsVisible=5,
            pos=LPoint3f(0.4, 0, 0.05),
            state='normal',
            text='CEPBEPA',
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
            parent=self.pg471,
            command=base.messenger.send,
            extraArgs=['select_list_item_changed'],
        )
        self.pg914.setTransparency(0)

        self.pg2484 = DirectEntry(
            frameSize=(-0.1, 10.1, -0.3962500154972076, 1.087500011920929),
            hpr=LVecBase3f(0, 0, 0),
            initialText='',
            pos=LPoint3f(-13.4, 0, -3.225),
            scale=LVecBase3f(1.5, 1.5, 1),
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg914,
        )
        self.pg2484.setTransparency(0)

        self.pg3545 = DirectButton(
            frameSize=(-2.3, 2.3, -0.213, 0.825),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(7.825, 0, -1.25),
            scale=LVecBase3f(1, 1, 1),
            text='Connect',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg2484,
            command=self.exit_menu3,
            pressEffect=1,
        )
        self.pg3545.setTransparency(0)

        self.pg945 = DirectScrolledListItem(
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='scrolled list item',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
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
        # Выбор обычного дроида. Он выбран по умолчанию
        self.click_sound.play() # играем звук клика
        self.command_sound.play()
        self.basic_droid = True
        self.pod_droid = False
        self.shield_droid = False

    def _pod_droid(self):
        # Выбор большого дроида.
        self.click_sound.play() # играем звук клика
        self.command_sound.play()
        self.pod_droid = True
        self.basic_droid = False
        self.shield_droid = False

    def _shield_droid(self):
        # Выбор дроида с щитом
        self.click_sound.play() # играем звук клика
        self.command_sound.play()
        self.basic_droid = False
        self.pod_droid = False
        self.shield_droid = True

    def single_player(self):
        # Одиночная игра
        self.click_sound.play() # играем звук клика
        self.command_sound.play() # играем звук команды
        
        self.single = True 
    
    def exit_menu(self):
        # Выход в меню из чата.
        self.click_sound.play() # играем звук клика
        self.command_sound.play() # играем звук команды
        # Удаляем элементы меню
        self.pg212.hide()
        self.pg10591.hide()
        self.pg561.hide()        

        self.menu(False)

    def exit_menu2(self):
        # Выход в меню из из выбора дроида.
        self.click_sound.play() # играем звук клика
        self.command_sound.play() # играем звук команды
        # Удаляем элементы меню
        self.pg188.hide()
        self.pg4741.hide()
        self.pg1254.hide()

        self.menu(False) 

    def exit_menu4(self):
        # ВЫход в меню из отправки бага
        self.click_sound.play() # играем звук клика
        self.command_sound.play() # играем звук команды

        # удаляем элементы меню
        self.pg149.hide()

        self.menu(False)

    def exit_menu3(self):
        # ВЫход в меню из серверов
        self.click_sound.play() # играем звук клика
        self.command_sound.play() # играем звук команды
        # Удаляем элементы меню
        self.pg471.destroy()

        self.load_game() # открываем игру

    def set_lifes(self):
        self.state = self.pg28909.guiItem.getValue() * 100 # загрузим слайдерное значение умноженое на 100, да трачу оптимизацию но мне кажется многим плевать на оптимизацию меню, ибо такого понятия просто нету :)
        self.state_droid = self.state / 2

    def gb_mode(self):
        '''включение чёрнобелого режима'''
        self.click_sound.play() # играем звук клика
        self.command_sound.play()
        self.GB = True

    def en_lang(self):
        '''Изменение языка на английский'''
        self.click_sound.play() # играем звук клика
        self.command_sound.play()
        self.EN = True

    def pro_system(self):
        '''Проффесиональное управление'''
        self.click_sound.play() # играем звук клика
        self.command_sound.play()
        self.pro_machine = True # включаем проффесиональное управление

    def load_game(self):
        self.click_sound.play() # играем звук клика
        self.command_sound.play() # играем звук ввода команды

        # убираем элементы меню
        self.pg3083.destroy()
        self.pg27986.destroy()
        self.pg28909.destroy()
        self.pg438.destroy()
        self.pg326.destroy()
        self.pgSingle.destroy()
        self.pgServers.destroy()
        self.pg452.destroy()
        
        self.pipeline = simplepbr.init() # initializating pbr light
        
        # все действия над сервером если не включена одиночная игра
        if not self.single:
            self.networking = PythonNetContext() # сервер
            self.networking.bindSocket(DEFAULT_PORT) # 'одеваем на сервер' его порт
            self.networking.connectToServer(self.arg_username, self.username) # коннектим игрока к серверу
            self.networking.clientConnect(self.username) #ещё коннектим, без аргументов
            self.networking.serverConnect(IP_USER) # коннектим айпи игрока
            self.networking.addClient(self.username) # добавляем клиента.
            self.networking.readTick() # читаем сервер
            #start_server() # то было локальной сетью, а теперь мы создаём сервер онлайна на своём компе              

        # если не выходили скроем глобус
        if not self.exiting:
            self.globe.hide()

        # Ксли включена одиночная игра - убираем кнопку чата
        if self.single:
            self.pg149.destroy()

        # if no single mode
        if not self.single:
            start_client() # starting client
        # удаляем глобус, если не выходили из игры
        if not self.exiting:
            del self.globe

        self.intro_sound.play() # играем звук интро

        dt = globalClock.getDt() # переменная, которая показывает, сколко ыремени прошло между кадрами

        # меняем настройки, чтобы пользователю казалось, что открыто новое окно
        self.props.setUndecorated(False) # раму мы показываем, но потом полноэкранный режим включается. Зачем это? Просто в panda3d если ты не уберешь одну настройку то она останется и будет влиять на все остальные.
        self.props.setFullscreen(True) # включаем полноэкранный режим
        self.openDefaultWindow(props=self.props) # Используем настройки

        # включим специальные шейдеры
        self.sh_framework = pbp.ShadingFramework(self.render)

        self.keyMap = {
            "left": 0, "right": 0, "forward": 0, "cam-left": 0, "cam-right": 0} # Создадим словарь кнопок, по их нажатию        

        # Рисуем звёзды

        self.sky = loader.loadModel("./models/sky/solar_sky_sphere") # загрузим модель космоса(это сфера)

        self.sky_tex = loader.loadTexture("./tex/stars_1k_tex.jpg") # загрузим текстуру
        self.sky.setTexture(self.sky_tex, 1) # зарендерим текстуру на небо
        self.sky.reparentTo(render) # инициализируем небо
        self.sky.setScale(40000) # расширим небо до максимальной величины panda3d

        self.environ = loader.loadModel("./models/world/falcon.egg") # Загрузим уже созданный в blender мир.
        self.environ.reparentTo(render) # Загружаем модель мира в окно

        droidStartPos = (-1, 0, 1.5 ) # Загружаем стартовую позицию игрока в мире.
        enemyStartPos = LVecBase3f(float(self.level[0]), float(self.level[1]), float(self.level[2])) # Загружаем позицию помощника-дроида.

        if not self.another_camera:
            if self.basic_droid:
                self.droid = GameApi.object(self, "./models/BasicDroid/BasicDroid.egg", 1, droidStartPos) # Загружаем модель игрока (созданная в blender)
            elif self.pod_droid :
                self.droid = GameApi.object(self, "./models/pod/pod.egg", 0.5, droidStartPos)

            elif self.shield_droid:
                self.shield_sound.play() # играем звук щита.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                self.droid = GameApi.object(self, "./models/BasicDroid/BasicDroid-lowres.egg", 1, droidStartPos)

        else:
            self.droid = render.attachNewNode("body")
            self.droid.setPos(droidStartPos)
            base.cam.reparentTo(self.droid)
                 
        self.enemy = GameApi.object(self, "./models/pod/pod.egg", 0.5, enemyStartPos) # Загружаем модель помощника (созданная в blender)
        if self.single:
            self.enemy.hide()

        self.weapon_pos = self.droid.getX(), self.droid.getY() + 0.7, 1 # Позиция пушки
        self.sword_pos = self.droid.getX(), self.droid.getY() + 0.1, 1 # Позиция пушки
        
        # Используем мультипроцесинг, чтобы оптимизировать нашу игру.
        with Pool(processes=6) as pool:
        
            self.weapon = GameApi.object(self, './models/BasicDroid/sniper.egg', .5, self.weapon_pos) # загрузим оружие
            
            self.bullet = GameApi.object(self, './models/spike/spike.egg', .5, (0, 0, 0)) # Загрузим пулю
            self.flash = GameApi.object(self, './models/whishlyflash/handlamp.egg', .5, (0, 0, 0)) # Загрузим фонарик
            self.planet = GameApi.object(self, './models/pod/pod.egg', 50, (0, -1000, 0))
            self.crosshair = GameApi.object(self, './models/crosshair/crosshair.egg', 1, (droidStartPos))
            self.grenade = GameApi.object(self, './models/grenade/Grenade.egg', 1, (3, 3, 0.3))
            self.fragment = GameApi.object(self, './models/fragment/Fragment.egg', 1, (5, 3, 0.3))

            # вражеский истребитель
            self.fighter = GameApi.object(self, './models/fighter/fighter.egg', 1, (0, 90 , 0)) # загрузим модельку истребителя

            self.cube = GameApi.object(self, './models/block/crate.egg', .7, (0, 0, 0)) # загружаем блок
            self.cube.hprInterval(1.5, (360, 360, 360)).loop()

        self.Intervalcube = self.cube.posInterval(13,
                                                   Point3(0, -1500, 0),
                                                   startPos=Point3(0, 10, 0))  # вращаем блок
        
        self.Intervalcube.loop() # делаем позу блока вращением

        # Врашение планеты
        self.planet.hprInterval(550, (360, 360, 0)).loop()
        
        self.spotlight = camera.attachNewNode(Spotlight("spotlight")) # Конфиги фонарика
        self.spotlight.node().setColor((.3, .3, .3, 1))
        self.spotlight.node().setSpecularColor((0, 0, 0, 1))

        self.floater = NodePath(PandaNode("floater")) 
        self.floater.reparentTo(self.droid)
        self.floater.setZ(2.0)

        self.accept("escape", self.exit) # При нажатии клавиши Esc выходим.
        
        self.accept("arrow_left", self.setKey, ["left", True]) # При кнопке влево - поворачиваем игрока влево
        self.accept("arrow_right", self.setKey, ["right", True]) # При кнопке вправо - поворачиваем игрока вправо
        self.accept("arrow_up", self.setKey, ["forward", True]) # При кнопке вперёд - идём вперёд
        self.accept("a", self.setKey, ["cam-left", True]) # При кнопке a - разворачиваем камеру вокруг нашей модельки
        self.accept("d", self.setKey, ["cam-right", True]) # При кнопке s - разворачиваем камеру вокруг нашей модельки
        self.accept("arrow_left-up", self.setKey, ["left", False]) # При кнопке вверх+влево - поворачиваем игрока влево и идём вперёд
        self.accept("arrow_right-up", self.setKey, ["right", False]) # При кнопке вверх+право - поворачиваем игрока вправо и идём вперёд
        self.accept("arrow_up-up", self.setKey, ["forward", False]) # При кнопке вверх+вверъ - идём вперёд и идём вперёд
        self.accept("a-up", self.setKey, ["cam-left", False]) # При кнопке a+вперёд - поворачиваем камеру влево и идём вперёд
        self.accept("d-up", self.setKey, ["cam-right", False]) # При кнопке s+вперёд - поворачиваем камеру вправо и идём вперёд

        self.accept("space", self.shot) # при пробеле стреляем
        self.accept("s", self.toggleLights, [[self.spotlight]]) # При кнопке s - включить фонарик
        self.accept("w", self.weapon_hide) # при кнопке w - уберём оружие.
        self.accept("p", self.cursor) # при кнопке p - покажем прмцел снафпера
        self.accept("g", self.grenade_snade) # при кнопке g - кидаем гранату

        base.enableParticles() # Включаем инициализацию дыма
        self.p = ParticleEffect() # Включим эффект дыма
        self.accept('f', self.particle_start) # при нажатии f(от force) -  загрузим файл дыма и переместим в конфиг чтобы именно эта анимация стала отображением дыма
        self.accept('0', self.fountain) # при  нажатии кнопок f+o(fountain) включим пожаротушительную систему
        self.accept('f3', self.toggleWireframe) # при нажатии f3 - включаем полигольный режим
        self.accept('r', base.useTrackball) # если нажали r - делаем RPG режим.

        taskMgr.add(self.move, "moveTask") # Добавляем задачу в наш движок

        self.capture_flag = Capture_flag(player=self.droid,
                                         base_1=self.environ,
                                         base_2=self.planet)

        taskMgr.add(self.capture_flag_update, "CaptureFlagUpdating")

        self.isMoving = False # Ставим значение isMoving на False(Вы можете менять это значение) чтобы игрок изначально стоял.
        # Делаем так, чтобы свет был изначально выключен.
        self.camera.setPos(self.droid.getX(), self.droid.getY() + 1, 3) # Ставим позицию камеры чуть больше позиции игрока

        if not self.EN : # если язык не английский
            self.state_info = MenuApi.text(self, text='корабль :' + str(float(self.state)), pos=(0.5, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля

        else : # если янглийский язык
            self.state_info = MenuApi.text(self, text='machine :' + str(float(self.state)), pos=(0.5, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля
            
                
        self.check_loss() # Проверяем поражение
        self.hide_weapon = False # Поставим, что оружие не убрано
        self.steam_pos = random.randrange(0, 5), random.randrange(0, 5) + self.speed, random.randrange(0, 5)
        self.fountain_pos = random.randrange(0, 5), random.randrange(0, 5), random.randrange(0, 1)

        self.motor_pos1 = 25.238849639892578, 8.962211608886719, 1.5 # позиция первого мотора
        self.motor_pos2 = -20.676218032836914, 10.55816650390625, 1.5 # позиция второго мотора

        self.motor1 = GameApi.loadParticleConfig(self, './special_effects/steam_critic+/fireish.ptf', self.motor_pos1, self.environ) # мотор 1
        self.motor2 = GameApi.loadParticleConfig(self, './special_effects/steam_critic+/fireish.ptf', self.motor_pos2, self.environ) # мотор 2

        self.state_info2 = MenuApi.text(self, text='', pos=(-0.8, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля
        self.state_droid_info = MenuApi.text(self, text=str(self.state_droid), pos=(-1.3, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии дроида

        self.force = False # Поставим, что не разгонялись

        self.light() # Свет

        # солнце(новая механика освещения)
        GameApi.light(self)

        # списки с обьектами
        self.objects = [self.environ, self.droid,
                        self.enemy, self.weapon,
                        self.bullet, self.flash,
                        self.cube, self.crosshair]
        
        # все графические обьекты
        self.gui_objects = [self.state_info]

        # если не включили одиночную игру, добавляем в список графических обьектов кнопку чата
        if not self.single:
            self.gui_objects.append(self.pg149)
        
        self.enemies = [self.enemy] # список врагов

        # Генерация врагов
        for e in range(0, 20):
            enemy = GameApi.object(self, './models/pod/pod.egg', 0.5, (-26 - e, e, 1.5))
            self.enemies.append(enemy)

        # если включена одиночная игра удаляем врагов
        for enemy in self.enemies:
            if self.single:
                enemy.hide()

        # список гранат
        self.grenades = [
            self.grenade]

        # список обьектов
        self.fragments = [
            self.fragment]

        # все обьекты, не поддающиюся эффектам
        self.all_objects = self.objects + self.fragments + self.grenades + [self.sky, self.fighter, self.planet]

        self.rust_texture = loader.loadTexture('./tex/rust.png') # загружаем текстуру ржавчины

        # Шейдеры
        GameApi.shaders(self, vert="./shaders/realistic/bloom.glsl", frag="./shaders/realistic/blur.glsl")
        GameApi.shaders(self, vert="./shaders/realistic/outline.glsl", frag="./shaders/realistic/repeat.glsl")
        GameApi.shaders(self, vert="./shaders/realistic/glow.glsl", frag="./shaders/realistic/grayscale.glsl")
        GameApi.shaders(self, vert="./shaders/realistic/shadow.frag", frag="./shaders/realistic/shadow.vert")
        
        # Если  игрок захотел поиграть в чёрнобелую игру, проверим это
        if self.GB :        
            GameApi.shaders(self, "./shaders/lighting.vert", "./shaders/lighting.frag") # теперь шейдеры работают!
            #render.set_shader(Shader.load(Shader.SL_GLSL, "./shaders/terrain.vert.glsl", "./shaders/terrain.frag.glsl"))

    def capture_flag_update(self, task):
        self.result = self.capture_flag.update() # updating  capture flag
        if self.result:
            print('You WIN!!!')
            self.exit()
    
    def _grenade_boom(self):
        # играем звуки гранаты
        self.grenade_launch.play()
        self.grenade_boun.play()
        self.grenade_boom.play()
    
        # Добавляем в список гранат гранату(ЛОГИКА:))
        self.grenades.append(self.grenade)
        # То же самое со списком фрагментов
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
        # Создаём обьект гранаты рядом с дроидом
        self.grenade = GameApi.object(self, 'models/grenade/Grenade.egg', 1, (self.droid.getX() - 5, self.droid.getY() - 3, 0))
        
        # эффект горения
        GameApi.loadParticleConfig(self, './special_effects/steam_critic+/fireish.ptf', self.grenade.getPos(), self.environ)
    

        # Создаём фрагмент железа
        self.fragment = GameApi.object(self, 'models/fragment/Fragment.egg', 1, (self.droid.getX(), self.droid.getY(), 0))
        self.fragment.hide() # не показываем фрагмент

        # Проверка условия : Если дроид рядом с гранатой, то вылетает железный фрагмент : якобы от дооида.
        if (self.droid.getX() - self.fragment.getX()) < 1 or (self.droid.getY() - self.fragment.getY()) < 1:
            self.fragment.show() # показываем фрагмент
        
        self._grenade_boom() # взрываем гранату

    def light_shader(self):
        '''Включение шейдера горения'''
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
        self.command_sound.play()
        if not self.pro_machine :
            self.force = True # Поставим, что мы уже разгонялись

            self.state -= 1 # сделаем меньше очков
            self.state_info.hide() # удалим текстовые очки

            for i in range(len(self.objects)):
                object = self.objects[i]
                object.setY(object.getY() - self.speed)
            
            if self.state != 10 and self.state > 10:
                self.state_info.hide() # убираем предедущее сообщение о жизнях корабля
                self.state_info = MenuApi.text(self, text='корабль :' + str(float(self.state)), pos=(0.5, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля
                self.check_loss() # проверяем поражение
                self.steam_pos = random.randrange(0, 5), random.randrange(0, 5) - (self.speed - 100), random.randrange(0, 1)
                GameApi.loadParticleConfig(self, 'special_effects/steam/steam.ptf', self.steam_pos, self.environ) 
                self.errorSound.play() # играем звук ошибки
                self.state_info2.hide() # убираем предедущее сообщение
                
                if not self.EN :
                    self.state_info2 = MenuApi.text(self, text='двигатель неисправен', pos=(-0.8, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля
                else :
                    self.state_info2 = MenuApi.text(self, text='motor error', pos=(-0.8, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля

                    
            else:
                self.state_info = MenuApi.text(self, text='корабль :' + str(float(self.state)), pos=(0.5, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля
                self.check_loss() # проверяем поражение
                self.steam_pos = random.randrange(0, 5), random.randrange(0, 5) - (self.speed - 100), random.randrange(0, 1)
                GameApi.loadParticleConfig(self, 'special_effects/steam_critic/steam.ptf', self.steam_pos, self.environ)
                self.errorSound.play() # играем звук ошибки
                self.state_info2.hide()  # убираем предедущее сообщение

                if not self.EN :
                    self.state_info2 = MenuApi.text(self, text='критическое состояние', pos=(-0.8, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля
                else :
                    self.state_info2 = MenuApi.text(self, text='critic state', pos=(-0.8, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля
        
            if self.state < 10:
                self.alarm_sound.play()
                self.state_info.hide()
                self.state_info = MenuApi.text(self, text='корабль :' + str(float(self.state)), pos=(0.5, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля
                self.check_loss() # проверяем поражение
                self.steam_pos = random.randrange(0, 5), random.randrange(0, 5) - (self.speed - 100), random.randrange(0, 5)
                                                                                   
                GameApi.loadParticleConfig(self, 'special_effects/steam_critic+/fireish.ptf', self.steam_pos, self.environ)
                self.errorSound.play() # играем звук ошибки
                self.state_info2.hide() # убираем предедущее сообщение

                if not self.EN :
                    self.state_info2 = MenuApi.text(self, text='падаем!', pos=(-0.8, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля
                else :
                    self.state_info2 = MenuApi.text(self, text='fall!', pos=(-0.8, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля

                # Вращаем обьекты в колрабле и сам корабль
                self.environ.hprInterval(50, (360, 360, 0)).loop()
                self.droid.hprInterval(50, (360, 360, 0)).loop()
                self.enemy.hprInterval(50, (360, 360, 0)).loop()

        else :
            if not self.EN :
                self.pro_info = MenuApi.text(self, text='ПРОФИ!', pos=(-0.8, 0.8), scale=0.1, font=self.font) # Напишем сообщение о том что вы профи :)
                
            else :
                self.pro_info = MenuApi.text(self, text='PRO!', pos=(-0.8, 0.8), scale=0.1, font=self.font) # Напишем сообщение о том что вы профи :)
                
            self.pro_machine_engine()

    def pro_machine_engine(self):
        '''Професиональная механика корабля'''
        # Тут нужен джойстик. Если его у вас нет, увы вы не сможете использовать этот режим.
        self.mgr = InputDeviceManager.get_global_ptr()
        for device in self.mgr.get_devices():
            self.gamepad = device

        MenuApi.text(self, text=str(self.gamepad), pos=(-1.6, -0.9), scale=0.05, font=self.font) # найденое устройство
        
        # Управление джойстиком
        taskMgr.add(self.moveTaskDjoystic, "moveTaskDjoystic")
        
    def reset(self):

        self.camera.setPosHpr(0, -200, 10, 0, 0, 0)
        self.environ.setPosHpr(0, -200, 9, 0, 0, 0)

    def moveTaskDjoystic(self, task):
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
        self.state_info2.hide() # убираем текст опасности
        if self.force:
            if self.state != 100:
                self.state += 1
                self.state_info.hide()
                self.state_info = MenuApi.text(self, text='корабль :' + str(float(self.state)), pos=(0.5, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля

            self.fountain_pos = random.randrange(0, 5), random.randrange(0, 5), random.randrange(0, 1)    
            GameApi.loadParticleConfig(self, 'special_effects/fountain/fountain.ptf', self.fountain_pos, self.environ)
            if self.fountain_pos == self.droid.getPos():
                if not self.EN:
                    self.state_info.setText('РЖАВЧИНА!')
                else:
                    self.state_info.setText('RUST!')

                self.state_droid -= 10
                self.state_droid_info.setText(str(self.state_droid)) # обновление состояния дроида

                self.droid.setTexture(self.rust_texture) # накладываем ржавчину на дроида
        self.weapon.setTexture(self.rust_texture) # накладываем ржавчмну на оружие

        else :
            if self.state != 100:
                self.state += 1
                self.state_info.hide()
                if not self.EN:
                    MenuApi.text(self, text='корабль :' + str(float(self.state)), pos=(0.5, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля
                else :
                    MenuApi.text(self, text='machine :' + str(float(self.state)), pos=(0.5, 0.8), scale=0.1, font=self.font) # Напишем сообщение о состоянии корабля ON ENGLISH
                #self.state_info = OnscreenText(text='корабль :' + str(self.state), pos=(0.5, 0.8), scale=0.1, fg=(1, 1, 1, 1), align=TextNode.ALeft, font=self.font) # Напишем сообщение о состоянии корабля

            self.fountain_pos = random.randrange(0, 5), random.randrange(0, 5), random.randrange(0, 1)    
            GameApi.loadParticleConfig(self, 'special_effects/fountain/fountain.ptf', self.fountain_pos, self.environ)
        
        
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
        dt = globalClock.getDt() + 0.5 # Cкорость движения
        if not self.hide_weapon : # если оружие убрано то мы не можем стрелять
            self.shotSound.play() # играем звук выстрела
            self.bullet.setPos(self.weapon_pos) # Пуля будет спавнится внутри пушки
            self.bullet.setY(self.bullet, 100 * dt) # Сдвигаем пулю на огромной скорости вперёд

            for object in self.objects:
                if object != self.droid and object != self.weapon and object != self.bullet:
                    if self.bullet.getY() == object.getY():
                        object.hide()
        else :
            self.kamikaze_sound.play()

    def check_loss(self):
        if self.state == 0: # если жизней у корабля не осталось
            self.weapon_hide() # уберём оружие
            if not self.EN :
                self.info = MenuApi.text(self, text='поражение', font=self.font,
                                pos=(-1.3, -0.5), scale=0.3) # напишем о поражении
            else :
                self.info = MenuApi.text(self, text='LOSS', font=self.font,
                                pos=(-1.3, -0.5), scale=0.3) # напишем о поражении
            self.crackSound.play() # играем звук взрыва

    def check_win(self):
        '''Проверка победы'''
        if (self.droid.getX(), self.droid.getY()) == (self.planet.getX(), self.planet.getY()):
            if not self.EN :
                self.info = MenuApi.text(self, text='победа', font=self.font,
                                pos=(-1.3, -0.5), scale=0.3)
            else :
                self.info = MenuApi.text(self, text='WIN', font=self.font,
                                pos=(-1.3, -0.5), scale=0.3)

    def cursor(self):
        # Рисуем прицел
        OnscreenText(text="||", style=1, fg=(1,1,1,1),pos=(0.0,0.03) , align=TextNode.ARight, scale = .07)
        OnscreenText(text="||", style=1, fg=(1,1,1,1),pos=(0.0,-0.05), align=TextNode.ARight, scale = .07)
        OnscreenText(text="==", style=1, fg=(1,1,1,1),pos=(-0.03,0.0), align=TextNode.ARight, scale = .07)
        OnscreenText(text="==", style=1, fg=(1,1,1,1),pos=(0.055,0.0), align=TextNode.ARight, scale = .07)

        # Перемещаем камеру рядом со снайпером
        self.camera.setPos(self.weapon.getX(), self.weapon.getY(), self.weapon.getZ())

    def easy_exit(self):
        # обычяеый выход(из меню)
        self.click_sound.play() # играем звук клика
        self.command_sound.play() # играем звук команды
        sys.exit() # просто системно выходим.
    
    def exit(self):
        # Выход из игры
        self.click_sound.play() # играем звук клика
        self.command_sound.play() # играем звук команды

        # проверим, включена ли одиночная игра
        if not self.single:
            self.networking.removeClient(self.username) # удаляем игрока с сервера

        self.exiting = True # поставим, что уже вышли из игры
        
        for o in self.all_objects: # удаляем все модели(абсолютно все)
            o.hide()
        for g in self.gui_objects: # удаляем все графтческие обьекты
            g.hide()
        self.menu(True) # выходим в меню

    def setKey(self, key, value):
        self.keyMap[key] = value # Делаем мехaнuзм нажатия клавиш.

    def move(self, task):

        ''' Делаем фуцнкцию движения игрока '''

        dt = globalClock.getDt() - .005 # Cкорость движения

        # Поворот камеры влево и вправо

        if self.keyMap["cam-left"]:
            self.camera.setX(self.camera, -10 * dt) # Меняем положеника камеры по икс. Таким образом получается илюзия поворота угла луча. Но на самом деле камера просто перемещается.
        if self.keyMap["cam-right"]:
            self.camera.setX(self.camera, + 10 * dt) # Тоже самое, что и наверху.

        startpos = self.droid.getPos() # Сделаем удобную переменную позиции игрока

        if self.keyMap["left"]:
            self.droid.setH(self.droid.getH() + 145 * dt)
            self.crosshair.setH(self.crosshair.getH() + 145 * dt)
            self.weapon.setH(self.weapon.getH() + 145 * dt)
            self.enemy.setY(self.enemy, 1 * dt )

            # движение врагов
            for e in self.enemies:
                bot(enemy=e, dt=dt)
            
        if self.keyMap["right"]:
            self.droid.setH(self.droid.getH() - 145 * dt)
            self.crosshair.setH(self.crosshair.getH() - 145 * dt)
            self.weapon.setH(self.weapon.getH() - 145 * dt)
            self.enemy.setY(self.enemy, -1 * dt)

            # движение врагов
            for e in self.enemies:
                bot(enemy=e, dt=dt)
            
        if self.keyMap["forward"]:
            if not DEVELOP_MODE:
                self.droid.setY(self.droid, -25 * dt) # перемещаем дроида
                self.crosshair.setY(self.crosshair, -25 * dt) # перемещаем круг над дроидом
                self.enemy.setX(self.enemy, 1 * dt) # перемещаем врага
                self.check_win() # Проверяем победу

            else :
                self.droid.setY(self.droid, -55 * dt)
                self.crosshair.setY(self.crosshair, -55 * dt)

            # движение врагов
            for e in self.enemies:
                bot(enemy=e, dt=dt)

            # Сделаем специальное условие проверки убрано оружие или нет
            if not self.hide_weapon:
                self.weapon_pos = self.droid.getX(), self.droid.getY() + 0.7, 3 # Позиция снайпера
                self.weapon.setPos(self.weapon_pos) # Обновляем позицию снайпера
            else:
                self.weapon_pos = self.droid.getX(), self.droid.getY() + 0.7, 3 # Снова вычесляем позицию снайпера
                self.flash.setPos(self.weapon_pos) # ставим фонарик на место снайпера

        if not self.another_camera:
            camvec = self.droid.getPos() - self.camera.getPos() # вектор камеры
            camvec.setZ(0) # 0 высота вектора
            camdist = camvec.length() # дистанция камеры от дроида
            camvec.normalize() # нормализируем вектор камеры
            if camdist > 10.0: # если дистанция камеры больше 10, то смещаем камеру за дрооидом
                self.camera.setPos(self.camera.getPos() + camvec * (camdist - 10))
                camdist = 10.0 # теперь дистанция будет снова 10
            if camdist < 5.0: # если дистагцтя камеры меньше 5, то...
                self.camera.setPos(self.camera.getPos() - camvec * (5 - camdist)) # сдвигаем камеру
                camdist = 5.0 # всё обновляем
                
            self.camera.lookAt(self.floater) # вот и пригодился наш floater


        return task.cont # возвращаем задачу



for addon_class in addon_classes:
    exec("addon_class().run()")

droid = DroidShooter() # Создадим экземпляр класса нашей игры
droid.run() # 3апустим игру


# разроботчики :
# Главный автор : ma3rx
# Помощник : panda3dmastercoder( присоеденился к проекту 31 января, 2021 года, 7:41)
# Рекламщик : rdb (написал первое сообщение на форуме 6 февраля 2021 года, 8:23)
