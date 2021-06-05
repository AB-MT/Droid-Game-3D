#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectScrolledList import DirectScrolledList
from direct.gui.DirectScrolledList import DirectScrolledListItem
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectButton import DirectButton
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI_server:
    def __init__(self, rootParent=None):
        
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
            text='DOOMPY',
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
        self.pg2484.hide()
        self.pg2484.setTransparency(0)

        self.pg3545 = DirectButton(
            frameSize=(-2.3, 2.3, -0.213, 0.825),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(7.825, 0, -1.25),
            scale=LVecBase3f(1, 1, 1),
            text='D. connect',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg2484,
            command=self.load_game,
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
        #self.pg471.addItem(self.pg945)

    def show(self):
        self.pg471.show()

    def hide(self):
        self.pg471.hide()

    def destroy(self):
        self.pg471.destroy()
