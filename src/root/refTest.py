'''
Created on 19 Aug 2017

@author: Ed
'''
# config
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '440')

import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.popup import Popup

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
import time

import os, sys
import subprocess
import ntpath
from shutil import copyfile, rmtree
from kivy.lib.osc.OSC import null
import zipfile
from kivy.uix.video import Video
from os import listdir
from os.path import isfile, join
import pickle
import shutil

import math
import ntpath
from kivy.core.image import Image as CoreImage

if sys.platform != "win32": import serial  # @UnresolvedImport

Builder.load_string("""

<SprayChannel>

    zSlider:zSlider
    tSlider:tSlider
    selectButton:selectButton
    maxButton:maxButton

    BoxLayout:
        orientation: 'vertical'
        size: self.parent.size
        pos: self.parent.pos
        
        canvas:
            Color:
                rgba: 1,0,1,0.25
            Rectangle:
                size: self.parent.size
                pos: self.parent.pos           
        ToggleButton:
            id: maxButton
            size_hint_y: 1
            text: str(root.sizePercentage) + '%'
            group: 'maxToggleGroup'                       
            on_press: root.maxButtonPressed(root.id)
        Slider:
            id: zSlider
            size_hint_y: 4
            min:0
            max:1
            step:0.01
            value: root.zFactor
            orientation: 'vertical'
            sensitivity: 'handle'
            on_value: root.zFactor = self.value
        Slider:
            sensitivity: 'handle'
            id: tSlider
            value: root.tFactor
            size_hint_y: 4
            min:0
            max:1
            step:0.01
            orientation: 'vertical'
            on_value: root.tFactor = self.value
        ToggleButton:
            size_hint_y: 1
            id: selectButton
            group: 'selectToggleGroup'
            text: 'Select'    
    
<SprayChannelScreen>

    channelBoxLayout:channelBoxLayout
     
    BoxLayout:
        orientation: 'horizontal'
        padding: 5
        spacing: 5

        BoxLayout:
            orientation: 'vertical'
            padding: 5
            spacing: 5
            size_hint_x: 0.25
            Label: 
                text: 'Z'
            Label:
                text: 'T'
        
        BoxLayout:
            id: channelBoxLayout
            orientation: 'horizontal'
            padding: 5
            spacing: 5
            size_hint_x: 9
            
        BoxLayout:
            size_hint_x: 1
            orientation:'vertical'
            Button:
                size_hint_y: 1
                text: 'Quit' 
                on_press: root.quit()
            Button:
                size_hint_y: 1
                text: 'z ^' 
                on_press: root.zUp()
            Button:
                size_hint_y: 1
                text: 'z V' 
                on_press: root.zDown()
            Button:
                size_hint_y: 1
                text: '< Copy' 
                on_press: root.copyPrevious()
            Button:
                size_hint_y: 1
                text: 'Copy >' 
                on_press: root.copyNext()
            Button:
                size_hint_y: 1
                text: 't ^' 
                on_press: root.tUp()
            Button:
                size_hint_y: 1
                text: 't V' 
                on_press: root.tDown()
            Button:
                size_hint_y: 1
                text: 'TEST' 
                on_press: root.test()
            
""")

class SprayChannel(Widget):

    zFactor = NumericProperty(0.0)
    tFactor = NumericProperty(0.0)
    sizePercentage = NumericProperty(0)

    def maxButtonPressed(self, channelID):
        sprayChannelScreen.maxButtonPressed(channelID)
    
class SprayChannelScreen(Screen):
    
    numberOfChannels = 10
    channelReferences = []
    channelsUsed = numberOfChannels
    
    def __init__(self, **kwargs):
        super(SprayChannelScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.addChannels)

    def addChannels(self, dt):
        for i in xrange(self.numberOfChannels):
            ch = SprayChannel(id='ch_'+str(i))
            self.channelBoxLayout.add_widget(ch)
            self.channelReferences.append(ch)
        self.channelReferences[self.numberOfChannels-1].maxButton.state = 'down'
        self.maxButtonPressed('ch_'+str(self.numberOfChannels-1))
        self.channelReferences[0].selectButton.state = 'down'
    
    def maxButtonPressed(self, channelID):
        id = int(channelID.split('_')[1])
        for i in xrange(self.numberOfChannels):
            if i <= id:
                self.channelReferences[i].zSlider.disabled = False
                self.channelReferences[i].tSlider.disabled = False
                self.channelReferences[i].selectButton.disabled = False
                percentage = str(int(((i+1.0)/(id+1.0))*100.0))+'%'
                self.channelReferences[i].maxButton.text = percentage
            else:
                self.channelReferences[i].zSlider.disabled = True
                self.channelReferences[i].tSlider.disabled = True
                self.channelReferences[i].selectButton.disabled = True
                self.channelReferences[i].maxButton.text = 'Max'
 
    def detectSelection(self):
        result = None
        for i in xrange(self.numberOfChannels):
            if self.channelReferences[i].selectButton.state == 'down':
                result = i
        return result

    def zUp(self):
        ch = self.detectSelection()
        if ch != None: 
            if self.channelReferences[ch].zFactor < 1: self.channelReferences[ch].zFactor += .01
            
    def zDown(self):
        ch = self.detectSelection()
        if ch != None: 
            if self.channelReferences[ch].zFactor > 0: self.channelReferences[ch].zFactor -= .01
    
    def copyPrevious(self):
        ch = self.detectSelection()
        if ch != None and ch > 0: 
            self.channelReferences[ch].zFactor = self.channelReferences[ch-1].zFactor
            self.channelReferences[ch].tFactor = self.channelReferences[ch-1].tFactor
    
    def copyNext(self):
        ch = self.detectSelection()
        if ch != None and ch < self.numberOfChannels: 
            self.channelReferences[ch].zFactor = self.channelReferences[ch+1].zFactor
            self.channelReferences[ch].tFactor = self.channelReferences[ch+1].tFactor
    
    def tUp(self):
        ch = self.detectSelection()
        if ch != None: 
            if self.channelReferences[ch].tFactor < 1: self.channelReferences[ch].tFactor += .01

    def tDown(self):
        ch = self.detectSelection()
        if ch != None: 
            if self.channelReferences[ch].tFactor > 0: self.channelReferences[ch].tFactor -= .01

    def test(self):
        pass
    
    def quit(self):
        pass
   
sm = ScreenManager()

sprayChannelScreen = SprayChannelScreen(name='sprayChannel')

sm.add_widget(sprayChannelScreen)


class Wank():
    pass

class TestApp(App):

    def build(self):
        a = Wank()
        b = a
        b.whatever = 'yo'
        print a.whatever

if __name__ == '__main__':
    TestApp().run()