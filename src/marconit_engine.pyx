# Самописное API к direct и panda3d

import pyximport # импоритурем Cython
pyximport.install() # инициализируем его
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectSlider import DirectSlider
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import *

from array import array
import random


class MenuApi(DirectObject):
    def slider(self, pos, scale, value, command):
        return DirectSlider(pos=pos, scale=scale, value=value,
                                    command=command)
    
    def button(self, pos, text, scale, pad, command):
        return DirectButton(pos=pos, text=text,
                                   scale=scale, pad=pad,
                                   command=command)

    def addInstruction(self, pos, msg, font):
        return OnscreenText(text=msg, style=1, fg=(1,1,1,1), font=font, pos=(-1.6, pos), align=TextNode.ALeft, scale = .04, shadow=(0,0,0,1))
        

    def addTitle(self, msg, font):
        return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=0.2,
                            parent=base.a2dBottomRight, align=TextNode.ARight,
                            pos=(-0.1, 0.09), shadow=(0, 0, 0, 1), font=font)

    def text(self, pos, text, font, scale):
        return OnscreenText(text=text, pos=pos, scale=scale, fg=(1, 1, 1, 1), align=TextNode.ALeft, font=font)

class GameApi(DirectObject):
    def light(self):
        sun = DirectionalLight("sun")
        sun.set_color_temperature(6000)
        sun.color = sun.color * 4
        sun_path = render.attach_new_node(sun)
        sun_path.set_pos(10, -10, -10)
        sun_path.look_at(0, 0, 0)
        sun_path.hprInterval(self.sun_interval, (sun_path.get_h(), sun_path.get_p() - 360, sun_path.get_r()), bakeInStart=True).loop()
        render.set_light(sun_path)

    def object(self, path, scale, pos):
        self.object = loader.loadModel(path)
        self.object.reparentTo(render)
        self.object.setScale(scale)
        self.object.setPos(pos)

        return self.object

    def sound(self, path, volume):
        self.sound = loader.loadMusic(path)
        self.sound.setVolume(volume)

        return self.sound

    def shaders(self, vert, frag):
        render.set_shader(Shader.load(Shader.SL_GLSL, vert, frag))

    def loadParticleConfig(self, filename, pos, object):
        self.p.cleanup()
        self.p = ParticleEffect()
        self.p.loadConfig(Filename(filename))

        self.p.start(object)
        self.p.setPos(pos)

    def make_shader(self, object, pos):
        '''Про шейдер'''
        object.set_shader(self.light_shader())
        object.set_shader_input('pos_light', pos)
