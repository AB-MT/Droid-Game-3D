
#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer
import pyximport # импоритурем Cython
pyximport.install() # инициализируем его
from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectScrolledList import DirectScrolledList
from direct.gui.DirectScrolledList import DirectScrolledListItem
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)
# We need showbase to make this script directly runnable
from direct.showbase.ShowBase import ShowBase

class GUI:
    def __init__(self, moders_list, rootParent=None):
        self.inst_font = loader.loadFont('./fonts/iAWriterDuoS-Bold.ttf')
        self.victorinst_font = loader.loadFont('./fonts/VictorMono-BoldItalic.ttf')
        
        self.pg10215 = DirectLabel(
            frameSize=(-3.15, 3.25, -0.113, 0.725),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-0.05, 0, 0.65),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Модераторы',
            text0_align=TextNode.A_center,
            text0_scale=(1, 1),
            text0_pos=(0, 0),
            text0_fg=LVecBase4f(0, 0, 0, 1),
            text0_bg=LVecBase4f(0, 0, 0, 0),
            text0_wordwrap=None,
            parent=rootParent,
            text_font=self.inst_font,
        )
        self.pg10215.setTransparency(0)

        self.pg11109 = DirectScrolledList(
            forceHeight=0.1,
            frameSize=(-0.5, 0.5, -0.01, 0.75),
            hpr=LVecBase3f(0, 0, 0),
            numItemsVisible=5,
            pos=LPoint3f(0.025, 0, -0.2),
            state='normal',
            text='Модерация',
            decButton_borderWidth=(0.005, 0.005),
            decButton_hpr=LVecBase3f(0, 0, 0),
            decButton_pos=LPoint3f(-0.45, 0, 0.03),
            decButton_state='disabled',
            decButton_text='Prev',
            decButton_text0_align=TextNode.A_left,
            decButton_text0_scale=(0.05, 0.05),
            decButton_text0_pos=(0, 0),
            decButton_text0_fg=LVecBase4f(0, 0, 0, 1),
            decButton_text0_bg=LVecBase4f(0, 0, 0, 0),
            decButton_text0_wordwrap=None,
            decButton_text1_align=TextNode.A_left,
            decButton_text1_scale=(0.05, 0.05),
            decButton_text1_pos=(0, 0),
            decButton_text1_fg=LVecBase4f(0, 0, 0, 1),
            decButton_text1_bg=LVecBase4f(0, 0, 0, 0),
            decButton_text1_wordwrap=None,
            decButton_text2_align=TextNode.A_left,
            decButton_text2_scale=(0.05, 0.05),
            decButton_text2_pos=(0, 0),
            decButton_text2_fg=LVecBase4f(0, 0, 0, 1),
            decButton_text2_bg=LVecBase4f(0, 0, 0, 0),
            decButton_text2_wordwrap=None,
            decButton_text3_align=TextNode.A_left,
            decButton_text3_scale=(0.05, 0.05),
            decButton_text3_pos=(0, 0),
            decButton_text3_fg=LVecBase4f(0, 0, 0, 1),
            decButton_text3_bg=LVecBase4f(0, 0, 0, 0),
            decButton_text3_wordwrap=None,
            incButton_borderWidth=(0.005, 0.005),
            incButton_hpr=LVecBase3f(0, 0, 0),
            incButton_pos=LPoint3f(0.45, 0, 0.03),
            incButton_state='disabled',
            incButton_text='Next',
            incButton_text0_align=TextNode.A_right,
            incButton_text0_scale=(0.05, 0.05),
            incButton_text0_pos=(0, 0),
            incButton_text0_fg=LVecBase4f(0, 0, 0, 1),
            incButton_text0_bg=LVecBase4f(0, 0, 0, 0),
            incButton_text0_wordwrap=None,
            incButton_text1_align=TextNode.A_right,
            incButton_text1_scale=(0.05, 0.05),
            incButton_text1_pos=(0, 0),
            incButton_text1_fg=LVecBase4f(0, 0, 0, 1),
            incButton_text1_bg=LVecBase4f(0, 0, 0, 0),
            incButton_text1_wordwrap=None,
            incButton_text2_align=TextNode.A_right,
            incButton_text2_scale=(0.05, 0.05),
            incButton_text2_pos=(0, 0),
            incButton_text2_fg=LVecBase4f(0, 0, 0, 1),
            incButton_text2_bg=LVecBase4f(0, 0, 0, 0),
            incButton_text2_wordwrap=None,
            incButton_text3_align=TextNode.A_right,
            incButton_text3_scale=(0.05, 0.05),
            incButton_text3_pos=(0, 0),
            incButton_text3_fg=LVecBase4f(0, 0, 0, 1),
            incButton_text3_bg=LVecBase4f(0, 0, 0, 0),
            incButton_text3_wordwrap=None,
            itemFrame_frameColor=(1, 1, 1, 1),
            itemFrame_frameSize=(-0.47, 0.47, -0.5, 0.1),
            itemFrame_hpr=LVecBase3f(0, 0, 0),
            itemFrame_pos=LPoint3f(0, 0, 0.6),
            text0_align=TextNode.A_center,
            text0_scale=(0.1, 0.1),
            text0_pos=(0, 0.015),
            text0_fg=LVecBase4f(0, 0, 0, 1),
            text0_bg=LVecBase4f(0, 0, 0, 0),
            text0_wordwrap=None,
            parent=rootParent,
            text_font=self.victorinst_font
        )
        self.pg11109.setTransparency(0)

        for mod in moders_list:
            self.pg11109.addItem(DirectScrolledListItem(
            frameSize=LVecBase4f(-3.83125, 3.90625, -0.2125, 0.85),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            state='disabled',
            text=str(mod),
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
            parent=self.pg11109,
            command=base.messenger.send,
            extraArgs=['select_list_item_changed'],
            text_font=self.inst_font,
        ))

    def show(self):
        self.pg10215.show()
        self.pg11109.show()

    def hide(self):
        self.pg10215.hide()
        self.pg11109.hide()

    def destroy(self):
        self.pg10215.destroy()
        self.pg11109.destroy()

# Create a ShowBase instance to make this gui directly runnable
