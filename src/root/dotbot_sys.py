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

<SysScreen>:

    BoxLayout:
        size_hint_x: 1
        orientation: 'vertical'
        spacing: 10

        Button:
            text: 'Console'
            on_release: root.quit_to_console()
        Button:
            text: 'Reboot'
            on_release: root.reboot()
        Button:
            text: 'Cancel'
            on_release: root.quit_to_home()
                
""")



class SysScreen(Screen):
    
    def __init__(self, **kwargs):
        super(SysScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
      

    def quit_to_console(self):
        print 'Bye!'
        sys.exit()
    
    
    def reboot(self):
        if sys.platform != "win32": 
            sudoPassword = 'posys'
            command = 'sudo reboot'
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
                
    def quit_to_home(self):
        self.sm.current = 'home'
