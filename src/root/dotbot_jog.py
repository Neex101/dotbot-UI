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
import dotbot_bot, dotbot_spray, dotbot_wall, dotbot_image, dotbot_rip # @UnresolvedImport
import math
import ntpath
from kivy.core.image import Image as CoreImage

if sys.platform != "win32": import serial  # @UnresolvedImport

Builder.load_string("""

<JogScreen>:

    datum_label:datum_label
    
    BoxLayout:
        orientation: 'horizontal'
    
        BoxLayout:
            size_hint_x: 1
            orientation: 'vertical'
            spacing: 10
            
            GridLayout:
                size_hint_y: 5
                cols: 3
                orientation: 'horizontal'
                padding: 5
                spacing: 5
                size_hint_y: None
                height: self.width
        
                Button:
                    disabled: True
                Button:
                    on_release: root.cancelXYJog()
                    on_press: root.buttonJogXY('Up')
                    BoxLayout:
                        padding: 10
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "up.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True                                    
                Button:
                    disabled: True
                Button:
                    on_release: root.cancelXYJog()
                    on_press: root.buttonJogXY('L')
                    BoxLayout:
                        padding: 10
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "left.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True                                    
                Label:
                    id:datum_label
                    text: ''
                Button:
                    on_release: root.cancelXYJog()
                    on_press: root.buttonJogXY('R')
                    BoxLayout:
                        padding: 10
                        size: self.parent.size
                        pos: self.parent.pos  
                        Image:
                            source: "right.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True                                    
                Button:
                    disabled: True
                Button:
                    on_release: root.cancelXYJog()
                    on_press: root.buttonJogXY('Dn')
                    BoxLayout:
                        padding: 10
                        size: self.parent.size
                        pos: self.parent.pos      
                        Image:
                            source: "down.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True                                    
                Button:
                    disabled: True
            
            BoxLayout:
                size_hint_y: 1
                orientation: 'horizontal'
                padding: 5
                spacing: 5 
                ToggleButton:
                    group: 'g1'
                    on_press: root.buttonJogSpeed('slow')
                    BoxLayout:
                        padding: 10
                        size: self.parent.size
                        pos: self.parent.pos      
                        Image:
                            source: "slow.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True                                      
                ToggleButton:
                    group: 'g1'
                    on_press: root.buttonJogSpeed('fast')
                    BoxLayout:
                        padding: 10
                        size: self.parent.size
                        pos: self.parent.pos      
                        Image:
                            source: "fast.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True   



        
        BoxLayout:
            size_hint_x: 1.2
            orientation: 'vertical'
            spacing: 10
            padding: 10
            BoxLayout:
                size_hint_y: 2
                padding: 5
                spacing: 5
                orientation: "horizontal"
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: 1  
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    Label:
                        size_hint_x: 3  
                        text: 'Slow speed:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24
                        input_filter: 'int'
                        multiline: False
                        text: str(root.slow_jog_speed)
                        on_text: root.slow_jog_speed=self.text
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: 1  
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    Label:
                        size_hint_x: 3  
                        text: 'Fast speed:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24
                        input_filter: 'int'
                        multiline: False
                        text: str(root.fast_jog_speed)
                        on_text: root.fast_jog_speed=self.text
            Label: 
                size_hint_y: 8
            Button:
                size_hint_y: 1
                text: 'Quit'
                on_release: root.quit()
                
""")


lastSavedFilePath = 'settings/lastUsed/' + 'jog_lastUsed'

class JogScreen(Screen):
    
    datum_height = NumericProperty(0)
    slow_jog_speed = NumericProperty(200)
    fast_jog_speed = NumericProperty(1000)
    
    JOG_MAX_MM = 2000 # target distance for job command, to be cancelled early by button release
    
    def __init__(self, **kwargs):
        super(JogScreen, self).__init__(**kwargs)
        if os.path.isfile(lastSavedFilePath): self.loadLastProfileSaved()

        self.bot=kwargs['bot']
        self.spray=kwargs['spray']
        self.wall=kwargs['wall']
        self.image=kwargs['image']
        self.sm=kwargs['screen_manager']
        self.s=kwargs['serial_link']
        
        self.datum_height = self.wall.datum_height

    def on_enter(self):
        self.datum_label.text = 'Datum height:\n' + str(self.datum_height) + 'mm'
        
    def loadLastProfileSaved(self):
        self.load(lastSavedFilePath)

    def load(self, filePath):
        if os.path.isfile(filePath):
            with open(filePath, 'rb') as input:
                p = pickle.load(input)
            self.slow_jog_speed = p[0]
            self.fast_jog_speed = p[1]

    def save(self):
        parametersList = [self.slow_jog_speed, self.fast_jog_speed]
        # save over last saved copy
        with open(lastSavedFilePath, 'wb') as output:
            pickle.dump(parametersList, output, pickle.HIGHEST_PROTOCOL)        
    
    def quit(self):
        self.save()
        self.sm.current = 'go'
        
    def buttonJogSpeed(self, speed):
        if speed == 'slow': 
            self.feedSpeedJogXY = self.slow_jog_speed
        if speed == 'fast': 
            self.feedSpeedJogXY = self.fast_jog_speed

    def buttonJogXY(self, case):
        if case == 'L': self.s.jog('L', self.JOG_MAX_MM)
        elif case == 'R': self.s.jog('R', self.JOG_MAX_MM) 
        elif case == 'Up': self.s.jog('Up', self.JOG_MAX_MM) 
        elif case == 'Dn': self.s.jog('Dn', self.JOG_MAX_MM) 

    def cancelXYJog(self):
        self.s.stop()
