#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectLabel import DirectLabel
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)
# We need showbase to make this script directly runnable
from direct.showbase.ShowBase import ShowBase

class GUI:
    def __init__(self, rootParent=None):
        self.inst_font = loader.loadFont('./fonts/iAWriterDuoS-Bold.ttf')
        self.victorinst_font = loader.loadFont('./fonts/VictorMono-BoldItalic.ttf')
        
        
        self.pg10024 = DirectLabel(
            frameSize=(-3.15, 3.25, -0.112, 0.725),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.025, 0, 0.45),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Привелегии',
            text0_align=TextNode.A_center,
            text0_scale=(1, 1),
            text0_pos=(0, 0),
            text0_fg=LVecBase4f(0, 0, 0, 1),
            text0_bg=LVecBase4f(0, 0, 0, 0),
            text0_wordwrap=None,
            parent=rootParent,
            text_font=self.inst_font,
        )
        self.pg10024.setTransparency(0)

        self.pg5201 = DirectLabel(
            frameSize=(-3.66, 3.66, -0.113, 0.725),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.175),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='В разработке...',
            text0_align=TextNode.A_center,
            text0_scale=(1, 1),
            text0_pos=(0, 0),
            text0_fg=LVecBase4f(0, 0, 0, 1),
            text0_bg=LVecBase4f(0, 0, 0, 0),
            text0_wordwrap=None,
            parent=rootParent,
            text_font=self.victorinst_font,
        )
        self.pg5201.setTransparency(0)


    def show(self):
        self.pg10024.show()
        self.pg5201.show()

    def hide(self):
        self.pg10024.hide()
        self.pg5201.hide()

    def destroy(self):
        self.pg10024.destroy()
        self.pg5201.destroy()

