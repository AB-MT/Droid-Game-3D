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

class GUI:
    def __init__(self, USERNAME, rootParent=None):
        
        self.pg149 = DirectLabel(
            frameSize=(-1.149999976158142, 1.25, -0.11250001192092896, 0.7250000238418579),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0.525),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='Top',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=rootParent,
        )
        self.pg149.setTransparency(0)

        self.pg1336 = DirectScrolledList(
            forceHeight=0.1,
            frameSize=(-0.5, 0.5, -0.01, 0.75),
            hpr=LVecBase3f(0, 0, 0),
            numItemsVisible=5,
            pos=LPoint3f(0.025, 0, -0.25),
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
            parent=rootParent,
        )
        self.pg1336.setTransparency(0)

        self.pg1693 = DirectScrolledListItem(
            frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 0),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            state='disabled',
            text='Admin',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg1336,
            command=base.messenger.send,
            extraArgs=['select_list_item_changed'],
        )
        self.pg1693.setTransparency(0)

        self.pg1715 = DirectScrolledListItem(
            frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.1),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='NFSMW',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg1336,
            command=base.messenger.send,
            extraArgs=['select_list_item_changed'],
        )
        self.pg1715.setTransparency(0)

        self.pg1740 = DirectScrolledListItem(
            frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.2),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='|X_X|',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg1336,
            command=base.messenger.send,
            extraArgs=['select_list_item_changed'],
        )
        self.pg1740.setTransparency(0)

        self.pg1768 = DirectScrolledListItem(
            frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.3),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text=USERNAME,
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg1336,
            command=base.messenger.send,
            extraArgs=['select_list_item_changed'],
        )
        self.pg1768.setTransparency(0)

        self.pg1799 = DirectScrolledListItem(
            frameSize=(-3.831250286102295, 3.9062500953674317, -0.21250001192092896, 0.85),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -0.4),
            scale=LVecBase3f(0.1, 0.1, 0.1),
            text='.___.',
            text_align=TextNode.A_center,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            text_wordwrap=None,
            parent=self.pg1336,
            command=base.messenger.send,
            extraArgs=['select_list_item_changed'],
        )
        self.pg1799.setTransparency(0)

        self.pg1336.addItem(self.pg1693)
        self.pg1336.addItem(self.pg1715)
        self.pg1336.addItem(self.pg1740)
        self.pg1336.addItem(self.pg1768)
        self.pg1336.addItem(self.pg1799)

    def show(self):
        self.pg149.show()
        self.pg1336.show()

    def hide(self):
        self.pg149.hide()
        self.pg1336.hide()

    def destroy(self):
        self.pg149.destroy()
        self.pg1336.destroy()
