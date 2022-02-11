#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectRadioButton import DirectRadioButton
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

        self.pg20901 = DirectLabel(
            frameSize=(-3.15, 3.25, -0.113, 0.725),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.675),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Настройки',
            text0_align=TextNode.A_center,
            text0_scale=(1, 1),
            text0_pos=(0, 0),
            text0_fg=LVecBase4f(0, 0, 0, 1),
            text0_bg=LVecBase4f(0, 0, 0, 0),
            text0_wordwrap=None,
            parent=rootParent,
            text_font=self.inst_font,
        )
        self.pg20901.setTransparency(0)

        self.pg23091 = DirectRadioButton(
            frameSize=(-3.644, 8.919, -0.294, 0.931),
            hpr=LVecBase3f(0, 0, 0),
            indicatorValue=1,
            pos=LPoint3f(-0.65, 0, 0.35),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Одиночная игра',
            indicator_hpr=LVecBase3f(0, 0, 0),
            indicator_pos=LPoint3f(-3.269, 0, 0.0185),
            indicator_relief=3,
            indicator_text0_align=TextNode.A_center,
            indicator_text0_scale=(1, 1),
            indicator_text0_pos=(0, -0.25),
            indicator_text0_fg=LVecBase4f(0, 0, 0, 1),
            indicator_text0_bg=LVecBase4f(0, 0, 0, 0),
            indicator_text0_wordwrap=None,
            indicator_text1_align=TextNode.A_center,
            indicator_text1_scale=(1, 1),
            indicator_text1_pos=(0, -0.25),
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
            command=onet,
            variable=[],
            value=[],
            text_font=self.victorinst_font,
        )
        self.pg23091.setTransparency(0)

        self.pg26503 = DirectRadioButton(
            frameSize=(-3.644, 8.919, -0.294, 0.931),
            hpr=LVecBase3f(0, 0, 0),
            indicatorValue=1,
            pos=LPoint3f(-0.65, 0, 0.175),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Черно-белый режим',
            indicator_hpr=LVecBase3f(0, 0, 0),
            indicator_pos=LPoint3f(-3.269, 0, 0.0185),
            indicator_relief=3,
            indicator_text0_align=TextNode.A_center,
            indicator_text0_scale=(1, 1),
            indicator_text0_pos=(0, -0.25),
            indicator_text0_fg=LVecBase4f(0, 0, 0, 1),
            indicator_text0_bg=LVecBase4f(0, 0, 0, 0),
            indicator_text0_wordwrap=None,
            indicator_text1_align=TextNode.A_center,
            indicator_text1_scale=(1, 1),
            indicator_text1_pos=(0, -0.25),
            indicator_text1_fg=LVecBase4f(0, 0, 0, 1),
            indicator_text1_bg=LVecBase4f(0, 0, 0, 0),
            indicator_text1_wordwrap=None,
            text0_align=TextNode.A_left,
            text0_scale=(1, 1),
            text0_pos=(-0.6, 0.0),
            text0_fg=LVecBase4f(0, 0, 0, 1),
            text0_bg=LVecBase4f(0, 0, 0, 0),
            text0_wordwrap=None,
            text1_align=TextNode.A_left,
            text1_scale=(1, 1),
            text1_pos=(-0.6, 0.0),
            text1_fg=LVecBase4f(0, 0, 0, 1),
            text1_bg=LVecBase4f(0, 0, 0, 0),
            text1_wordwrap=None,
            text2_align=TextNode.A_left,
            text2_scale=(1, 1),
            text2_pos=(-0.6, 0.0),
            text2_fg=LVecBase4f(0, 0, 0, 1),
            text2_bg=LVecBase4f(0, 0, 0, 0),
            text2_wordwrap=None,
            text3_align=TextNode.A_left,
            text3_scale=(1, 1),
            text3_pos=(-0.6, 0.0),
            text3_fg=LVecBase4f(0, 0, 0, 1),
            text3_bg=LVecBase4f(0, 0, 0, 0),
            text3_wordwrap=None,
            parent=rootParent,
            variable=[],
            value=[],
            text_font=self.victorinst_font,
        )
        self.pg26503.setTransparency(0)

        self.pg23091.setOthers([])
        self.pg26503.setOthers([])

    def show(self):
        self.pg20901.show()
        self.pg23091.show()
        self.pg26503.show()

    def hide(self):
        self.pg20901.hide()
        self.pg23091.hide()
        self.pg26503.hide()

    def destroy(self):
        self.pg20901.destroy()
        self.pg23091.destroy()
        self.pg26503.destroy()
