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
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty  # @UnresolvedImport
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
import dotbot_bot, dotbot_spray, dotbot_wall, dotbot_image, dotbot_rip, dotbot_go, dotbot_serial, dotbot_sys  # @UnresolvedImport
import math
import ntpath
from kivy.core.image import Image as CoreImage
import socket


if sys.platform != "win32": import serial  # @UnresolvedImport

Builder.load_string("""

<HomeScreen>:

    botProfileLabel:botProfileLabel
    sprayProfileLabel:sprayProfileLabel
    wallProfileLabel:wallProfileLabel
    fileProfileLabel:fileProfileLabel
    ripProfileLabel:ripProfileLabel
    printPreview:printPreview

    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 5
        
        BoxLayout:
            size_hint_y: 0.9
            orientation: 'horizontal'
            padding: 0
            spacing: 5
            
            BoxLayout:
                size_hint_x:.5
                Scatter:
                    center: self.parent.center
                    size: self.parent.size
                    do_rotation: False
                    do_translation: True
                    do_scale: True
                    FloatLayout:
    #                     index: 99
                        size: self.parent.size
                        pos:self.pos
                        PrintPreview:
                            index:99
                            auto_bring_to_front: False
                            id:  printPreview
                            size:self.parent.size
                            pos:self.parent.pos

            BoxLayout:
                size_hint_x: 0.5
                orientation: 'vertical'
                padding: 0
                spacing: 5
                
                BoxLayout:
                    size_hint_y: 1
                    orientation: 'horizontal'
                    padding: 5
                    spacing: 5
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    Button:
                        text: 'Bot'
                        on_release: 
                            root.manager.transition.direction = 'left'
                            root.manager.current = 'botSet'
                    Label:
                        id: botProfileLabel
                        text: '<update me>'
                BoxLayout:
                    size_hint_y: 1
                    orientation: 'horizontal'
                    padding: 5
                    spacing: 5
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    Button:
                        text: 'Spray profile'
                        on_release: 
                            root.manager.transition.direction = 'left'
                            root.manager.current = 'spraySet'
                    Label:
                        id: sprayProfileLabel
                        text: '<update me>'
                BoxLayout:
                    size_hint_y: 1
                    orientation: 'horizontal'
                    padding: 5
                    spacing: 5
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    Button:
                        text: 'Wall'
                        on_release: 
                            root.manager.transition.direction = 'left'
                            root.manager.current = 'wallSet'
                    Label:
                        id: wallProfileLabel
                        text: '<update me>'
                BoxLayout:
                    size_hint_y: 1
                    orientation: 'horizontal'
                    padding: 5
                    spacing: 5
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    Button:
                        text: 'Image'
                        on_release: 
                            root.manager.transition.direction = 'left'
                            root.manager.current = 'imageSet'
                    Label:
                        id: fileProfileLabel
                        text: '<update me>'
                BoxLayout:
                    size_hint_y: 1
                    orientation: 'horizontal'
                    padding: 5
                    spacing: 5
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    Button:
                        text: 'Process'
                        on_release: 
                            root.manager.transition.direction = 'left'
                            root.manager.current = 'ripSet'
                    Label:
                        id: ripProfileLabel
                        text: '<update me>'

                BoxLayout:
                    size_hint_y: 1
                    orientation: 'horizontal'
                    padding: 5
                    spacing: 5
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    Button:
                        text: 'Go'
                        on_release: 
                            root.manager.transition.direction = 'left'
                            root.manager.current = 'go'
        
        BoxLayout:
            size_hint_y: 0.1
            padding: 5
            spacing: 5
            canvas:
                Color: 
                    rgba: 1,1,1,.2
                Rectangle: 
                    size: self.size
                    pos: self.pos

            Button:
                size_hint_x: 1
                text: "Sys"
                on_release: 
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'sys'
            Label:
                size_hint_x: 4
                text: root.ip_status_label            
            Label:
                size_hint_x: 4
                text: root.connection_status_label
            
                
<PrintPreview>
    
    canvasPreview:canvasPreview
    imagePreview:imagePreview
    
    on_size: root.reposition_assets()
    on_pos: root.reposition_assets()

    Image:
    
        id: canvasPreview
        source: 'wall_preview.png'
        allow_stretch: True
        keep_ratio: False
    Image:
        index: 100
        auto_bring_to_front: False

        id:imagePreview
        source: 'dotbot_logo.png'
        allow_stretch: True
        keep_ratio: True

        
            
""")

class PrintPreview(Widget):
    
    def reposition_assets(self):
        
        self.imagePreview.source = imageSetScreen.source_image_path
        
        widget_x = self.parent.width
        widget_y = self.parent.height
        
        wall_x = wallSetScreen.wall_width_mm
        wall_y = wallSetScreen.wall_height_mm
        
        image_x = imageSetScreen.imageXPixels * wallSetScreen.pixel_diameter
        image_y = imageSetScreen.imageYPixels * wallSetScreen.pixel_diameter
       
        image_lift = wallSetScreen.image_lift_mm
        
        scale_x = widget_x / (wall_x * 1.0)
        scale_y = widget_y / (wall_y * 1.0)
        scale = min(scale_x, scale_y)
        
        self.canvasPreview.size = (wall_x * scale, wall_y * scale)
        self.canvasPreview.pos = (self.parent.center_x - (wall_x * scale) / 2, 0)
        self.imagePreview.size = (image_x * scale, image_y * scale)
        self.imagePreview.pos = (self.parent.center_x - (image_x * scale) / 2, image_lift * scale)


class HomeScreen(Screen):
    
    connection_status_label = StringProperty('Connection status')
    ip_status_label = StringProperty('Connection status')
    
    def on_enter(self):
        self.refreshLabels()
        self.printPreview.reposition_assets()
    
    def refreshLabels(self):
        self.botProfileLabel.text = botSetScreen.profileName
        self.sprayProfileLabel.text = spraySetScreen.profileName
        self.wallProfileLabel.text = wallSetScreen.profile_name
        self.fileProfileLabel.text = imageSetScreen.profile_name
        self.ripProfileLabel.text = ripSetScreen.profile_name

        # Sqrl connection status label
        if serial_link.is_connected(): self.connection_status_label = serial_link.serial_address + 'Sqrl OK'
        else: self.connection_status_label = serial_link.serial_address + 'No Sqrl'
        
        # Wifi/IP status label
        if sys.platform == "win32": 
            try:
                hostname=socket.gethostname()   
                IPAddr=socket.gethostbyname(hostname)
                ip_address = str(IPAddr)
            except:
                ip_address = 'No wifi'
        else: 
            try:
                f = os.popen('hostname -I')
                first_info = f.read().strip().split(' ')[0]
                if len(first_info.split('.')) == 4:
                    ip_address = first_info
                else:
                    ip_address = 'No Wifi'
            except:
                ip_address = 'No Wifi'
        
        self.ip_status_label = ip_address
        
        


# initialisation - don't reorder

serial_link = dotbot_serial.DotBotSerial()
serial_link.connect("COM6")

sm = ScreenManager()

homeScreen = HomeScreen(name='home')
botSetScreen = dotbot_bot.BotSetScreen(name='botSet')
spraySetScreen = dotbot_spray.SpraySetScreen(name='spraySet', screen_manager=sm, serial_link=serial_link)
wallSetScreen = dotbot_wall.WallSetScreen(name='wallSet')
imageSetScreen = dotbot_image.ImageSetScreen(name='imageSet')
ripSetScreen = dotbot_rip.RipSetScreen(name='ripSet', bot=botSetScreen, spray=spraySetScreen,
                                       wall=wallSetScreen, image=imageSetScreen)
goScreen = dotbot_go.GoScreen(name='go', bot=botSetScreen, spray=spraySetScreen,
                              wall=wallSetScreen, image=imageSetScreen, screen_manager=sm, serial_link=serial_link)
sysScreen = dotbot_sys.SysScreen(name='sys', screen_manager=sm)

sm.add_widget(homeScreen)
sm.add_widget(botSetScreen)
sm.add_widget(spraySetScreen)
sm.add_widget(wallSetScreen)
sm.add_widget(imageSetScreen)
sm.add_widget(ripSetScreen)
sm.add_widget(goScreen)
sm.add_widget(sysScreen)

sm.current = 'home'

serial_link.initialise_objects(botSetScreen, spraySetScreen, wallSetScreen, imageSetScreen)


class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
