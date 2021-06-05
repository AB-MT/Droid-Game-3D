#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

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

class GUI_3:
    def __init__(self, rootParent=None):
        
        self.pg149 = DirectLabel(
            frameSize=(-3.15, 3.25, -0.113, 0.725),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.525),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Moderators',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=rootParent,
        )
        self.pg149.setTransparency(0)

        self.pg422 = DirectScrolledList(
            forceHeight=0.1,
            scale=LVecBase3f(10, 10, 10),
            frameSize=(-0.5, 0.5, -0.01, 0.75),
            hpr=LVecBase3f(0, 0, 0),
            numItemsVisible=5,
            pos=LPoint3f(0, 0, -7.9),
            state='normal',
            text='',
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
            parent=self.pg149,
        )
        self.pg422.setTransparency(0)

        self.pg1117 = DirectScrolledListItem(
            frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            state='disabled',
            text='Marcic_Admin',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg422,
            command=base.messenger.send,
            extraArgs=['select_list_item_changed'],
        )
        self.pg1118 = DirectScrolledListItem(
            frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            state='disabled',
            text='panda3dmastercoder',
            text_align=TextNode.A_center,
            text_scale=(0.8, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg422,
            command=base.messenger.send,
            extraArgs=['select_list_item_changed'],
        )
        self.pg1117.setTransparency(0)

        self.pg422.addItem(self.pg1117)
        self.pg422.addItem(self.pg1118)

    def show(self):
        self.pg149.show()

    def hide(self):
        self.pg149.hide()

    def destroy(self):
        self.pg149.destroy()
