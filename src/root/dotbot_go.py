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
import dotbot_jog # @UnresolvedImport
import math
import ntpath
from kivy.core.image import Image as CoreImage

if sys.platform != "win32": import serial  # @UnresolvedImport

Builder.load_string("""

<GoScreen>:

    BoxLayout:
        orientation: 'horizontal'
        
        BoxLayout:
            size_hint_x: 1
            orientation: 'vertical'
            spacing: 10
            Button:
                text: 'Move'
                on_release: 
                    root.manager.transition.direction = 'down'
                    root.manager.current = 'jog'
            Button:
                text: 'Scan'
                on_release: root.scan()
            Button:
                text: 'Go'
                on_release: root.go()
            Button:
                text: 'Quit'
                on_release: root.quit()

        BoxLayout:
            size_hint_x: 1
                
""")



class GoScreen(Screen):
    
    def __init__(self, **kwargs):
        super(GoScreen, self).__init__(**kwargs)
        
        self.bot=kwargs['bot']
        self.spray=kwargs['spray']
        self.wall=kwargs['wall']
        self.image=kwargs['image']
        self.sm=kwargs['screen_manager']
        self.s=kwargs['serial_link']
        
        self.jogScreen = dotbot_jog.JogScreen(name='jog', bot=self.bot, spray=self.spray, 
                                                 wall=self.wall, image=self.image, screen_manager=self.sm, 
                                                 serial_link=self.s)

        self.sm.add_widget(self.jogScreen)

    def scan(self):
        pass

    def go(self):
        pass
        
    def quit(self):
        self.sm.current = 'home'
