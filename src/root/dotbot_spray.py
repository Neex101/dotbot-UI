'''
Created on 19 Aug 2017

@author: Ed
'''
# config
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
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
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport

if sys.platform != "win32": import serial  # @UnresolvedImport

Builder.load_string("""

<SpraySetScreen>:

    fileSelectedLabel:fileSelectedLabel
    fileNameTextInput:fileNameTextInput
    filechooser:filechooser
    deleteButton:deleteButton
    loadButton:loadButton
    
    standby_abs_label:standby_abs_label
    dump_abs_label:dump_abs_label
    crack_abs_label:crack_abs_label

    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 5
    
        BoxLayout:
            size_hint_y: 9
            orientation: 'horizontal'
            padding: 0
            spacing: 5
    
            BoxLayout:
                size_hint_x: 1
                orientation: 'vertical'
                padding: 0
                spacing: 5

                BoxLayout:
                    padding: 10
                    spacing: 10
                    size_hint_y: 1
                    orientation: 'horizontal'
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    TextInput:
                        size_hint_x: 3
                        id: fileNameTextInput
                        font_size:24
                        multiline: False
                        text: root.profileName
                        on_text: root.profileName=self.text
                    Button:
                        size_hint_x: 1  
                        text: 'Profile'
                        on_release: 
                            root.manager.transition.direction = 'down'
                            root.manager.current = 'sprayChannels'  

                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: 4  

                    BoxLayout:
                        padding: 5
                        spacing: 5
                        orientation: "vertical"
                        size_hint_x: 1.5  
                        canvas:
                            Color: 
                                rgba: 1,1,1,.2
                            Rectangle: 
                                size: self.size
                                pos: self.pos
                        
                        TextInput:
                            size_hint_x: 1
                            font_size:24
                            multiline: False
                            text: str(root.goSteps)
                            on_text: root.goSteps=int(self.text)
                        Button:
                            size_hint_y: 1  
                            text: 'UP'
                            on_release: root.goUp()
                        Label:
                            size_hint_y: 1  
                            text: str(root.position_rel_to_crack) + " (" + str(root.position_abs) + ")"
                            font_size: 24
                        Button:
                            size_hint_y: 1  
                            text: 'DOWN'
                            on_release: root.goDown()
                        

                    BoxLayout:
                        padding: 0
                        spacing: 0
                        orientation: "vertical"
                        size_hint_x: 3  
                                                     
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
                            Button:
                                size_hint_x: 1  
                                text: 'Standby'
                                on_release: root.goToStandby()
                            TextInput:
                                size_hint_x: 1
                                font_size:24
                                multiline: False
                                text: str(root.standby_rel_to_crack)
                                on_text: 
                                    root.standby_rel_to_crack=int(self.text)
                                    standby_abs_label.text='(' + str(root.crack_position_abs + root.standby_rel_to_crack) + ')'
                            Label:
                                id: standby_abs_label
                                font_size: 24
                                size_hint_x: 1  
                                text: '(' + str(root.crack_position_abs + root.standby_rel_to_crack) + ')'
                                      
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
                            Button:
                                size_hint_x: 1  
                                text: 'Crack'
                                on_release: root.goToCrack()
                            Button:
                                size_hint_x: 1
                                text: 'Set'
                                on_release: root.setCrack()
                            Label:
                                id: crack_abs_label
                                size_hint_x: 1 
                                font_size: 24
                                text: '(' + str(root.crack_position_abs) + ')'
                                      
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
                            Button:
                                size_hint_x: 1  
                                text: 'Dump'
                                on_release: root.goToDump()
                            TextInput:
                                size_hint_x: 1
                                font_size:24
                                multiline: False
                                text: str(root.dump_rel_to_crack)
                                on_text: 
                                    root.dump_rel_to_crack=int(self.text)
                                    dump_abs_label.text = '(' + str(root.crack_position_abs + root.dump_rel_to_crack) + ')'                        
                            Label:
                                id: dump_abs_label
                                size_hint_x: 1  
                                font_size: 24
                                text: '(' + str(root.crack_position_abs + root.dump_rel_to_crack) + ')'                        
                        
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
                                size_hint_x: 1  
                                text: 'Max dot'
                                font_size:24
                            TextInput:
                                size_hint_x: 1
                                font_size:24
                                multiline: False
                                text: str(root.max_dot_dia_mm)
                                on_text: root.max_dot_dia_mm=int(self.text)
                            Label:
                                size_hint_x: 1  
                                text: 'mm'
                                font_size:24

                                
            BoxLayout:
                size_hint_x:1
                orientation: 'vertical'
                padding: 0
                spacing: 5
                canvas:
                    Color: 
                        rgba: 1,1,1,.2
                    Rectangle: 
                        size: self.size
                        pos: self.pos            
                FileChooserListView:
                    id: filechooser
                    size_hint_y: 7
                    filter_dirs: True
                    filters: ['*.spray']
                    rootpath: 'settings/'
                    on_selection: root.refreshFilechooser()
                Label:
                    id: fileSelectedLabel
                    size_hint_y: 1
                    font_size:24
        BoxLayout:
            size_hint_y:2
            orientation: 'horizontal'
            padding: 5
            spacing: 5
            Button:
                text: 'Cancel'
                on_release:
                    root.loadLastProfileSaved(0)
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'home'                          
            Button:
                text: 'Save'
                on_release: 
                    root.save()
#                     root.manager.transition.direction = 'right'
#                     root.manager.current = 'home'                          
            Button:
                id:loadButton
                text: 'Load'
                disabled: True
                on_release: 
                    root.load(filechooser.selection[0])
            Button:
                id: deleteButton
                text: 'Delete'
                disabled: True
                on_release:
                    root.deleteSelected(filechooser.selection[0])
    
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
    test_forever_button:test_forever_button
     
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
                on_release: 
                    root.manager.transition.direction = 'up'
                    root.manager.current = 'spraySet'                          
            Button:
                size_hint_y: 1
                text: 'z ^' 
                on_release: root.zUp()
            Button:
                size_hint_y: 1
                text: 'z V' 
                on_release: root.zDown()
            Button:
                size_hint_y: 1
                text: '< Copy' 
                on_release: root.copyPrevious()
            Button:
                size_hint_y: 1
                text: 'Copy >' 
                on_release: root.copyNext()
            Button:
                size_hint_y: 1
                text: 't ^' 
                on_release: root.tUp()
            Button:
                size_hint_y: 1
                text: 't V' 
                on_release: root.tDown()
            Button:
                size_hint_y: 1
                text: 'TEST x1' 
                on_release: root.test()              
            Button:
                size_hint_y: 1
                text: 'TEST xN' 
                on_release: root.test_forever()   
                id: test_forever_button 
            
""")


lastSavedFilePath = 'settings/lastUsed/' + 'spray_lastUsed'
settingsDir = 'settings/'

class SpraySetScreen(Screen):
    
    profileName = StringProperty('Default')
    standby_rel_to_crack = NumericProperty(-20)
    dump_rel_to_crack = NumericProperty(30)
    max_dot_dia_mm = NumericProperty(80)
    position_abs = NumericProperty(30)
    position_rel_to_crack = NumericProperty(0)
    goSteps = NumericProperty(2)
    crack_position_abs = NumericProperty(50)

    def __init__(self, **kwargs):
        super(SpraySetScreen, self).__init__(**kwargs)
        self.s = kwargs['serial_link']
        self.sm = kwargs['screen_manager']
        self.sprayChannelScreen = SprayChannelScreen(name='sprayChannels', screen_manager=self.sm, serial_link=self.s)
        self.sm.add_widget(self.sprayChannelScreen)
        if os.path.isfile(lastSavedFilePath): Clock.schedule_once(self.loadLastProfileSaved, 1)

    def save(self):
        # note order is important here: must match loading order. TODO: switch to dict?
        parametersList = [self.profileName, self.crack_position_abs, self.standby_rel_to_crack, 
                          self.dump_rel_to_crack, self.max_dot_dia_mm, 
                          self.sprayChannelScreen.get_z_and_t_FactorsForProfile(), 
                          self.sprayChannelScreen.channelsUsed]
                
        # save to file in settings folder       
        with open(settingsDir + self.profileName + '.spray', 'wb') as output:
            pickle.dump(parametersList, output, pickle.HIGHEST_PROTOCOL)
        # save over 'last saved' copy
        with open(lastSavedFilePath, 'wb') as output:
            pickle.dump(parametersList, output, pickle.HIGHEST_PROTOCOL)        
        self.refreshFilechooser()
        
    def load(self, filePath):
        global p
        if os.path.isfile(filePath):
            with open(filePath, 'rb') as input:
                p = pickle.load(input)
            self.profileName = p[0]
            self.crack_position_abs = p[1]
            self.standby_rel_to_crack = p[2]
            self.dump_rel_to_crack = p[3]
            self.max_dot_dia_mm = p[4]
            print 'Loading...'
            self.sprayChannelScreen.load(p[5])
            self.sprayChannelScreen.channelsUsed = p[6]
            self.sprayChannelScreen.maxButtonPressed('ch_' + str(self.sprayChannelScreen.channelsUsed - 1))
    
    def deleteSelected(self, filePath):
        self.fileSelectedLabel.text = ''
        os.remove(filePath)
        self.filechooser.selection = self.filechooser.selection[0] 
        self.refreshFilechooser()

    def refreshFilechooser(self):
        try:
            if self.filechooser.selection[0] != 'C':
                self.deleteButton.disabled = False
                self.loadButton.disabled = False
                self.fileSelectedLabel.text = os.path.basename(self.filechooser.selection[0])
            else:
                self.deleteButton.disabled = True
                self.loadButton.disabled = True
                self.fileSelectedLabel.text = ''
        except:
            self.deleteButton.disabled = True
            self.loadButton.disabled = True
            self.fileSelectedLabel.text = ''
        self.filechooser._update_files()
        
    def loadLastProfileSaved(self, dt):
        self.load(lastSavedFilePath)

    def goUp(self):
        self.position_abs -= self.goSteps
        if self.position_abs < 0: self.position_abs = 0
        self.position_rel_to_crack = self.position_abs - self.crack_position_abs
        self.s.set_servo_angle(self.position_abs)
        
    def goDown(self):
        self.position_abs += self.goSteps
        if self.position_abs < 0: self.position_abs = 0
        self.position_rel_to_crack = self.position_abs - self.crack_position_abs
        self.s.set_servo_angle(self.position_abs)

    def goToStandby(self):
        angle = self.crack_position_abs + self.standby_rel_to_crack
        if angle < 0: angle = 0
        self.s.set_servo_angle(angle)
        self.position_abs = angle
        self.position_rel_to_crack = self.position_abs - self.crack_position_abs

    def goToCrack(self):
        angle = self.crack_position_abs
        if angle < 0: angle = 0
        self.s.set_servo_angle(angle)
        self.position_abs = angle
        self.position_rel_to_crack = self.position_abs - self.crack_position_abs

    def goToDump(self):
        angle = self.crack_position_abs + self.dump_rel_to_crack
        if angle < 0: angle = 0
        self.s.set_servo_angle(angle)
        self.position_abs = angle
        self.position_rel_to_crack = self.position_abs - self.crack_position_abs

    def setCrack(self):
        self.crack_position_abs = self.position_abs
        self.position_rel_to_crack = self.position_abs - self.crack_position_abs



class SprayChannel(Widget):

    zFactor = NumericProperty(0)
    tFactor = NumericProperty(0)

    def __init__(self, **kwargs):
        super(SprayChannel, self).__init__(**kwargs)
        pass
    
    def maxButtonPressed(self, channelID):
        self.parent.parent.parent.maxButtonPressed(channelID)

class SprayChannelScreen(Screen):
    
    numberOfChannels = 12
    channelsUsed = numberOfChannels
    max_press_time_in_millis = 3000
    
    channelReferences = []
    
    def __init__(self, **kwargs):
        super(SprayChannelScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.s = kwargs['serial_link']

        Clock.schedule_once(self.addChannels)

        
    def load(self, z_and_t_FactorsForProfile):
        for i in xrange(self.numberOfChannels):
            self.channelReferences[i].zFactor
            z_and_t_FactorsForProfile[i][0]
            self.channelReferences[i].zFactor = z_and_t_FactorsForProfile[i][0]
            self.channelReferences[i].tFactor = z_and_t_FactorsForProfile[i][1]

    def get_z_and_t_FactorsForProfile(self):
        z_and_t_FactorsForProfile = []
        for i in xrange(self.numberOfChannels):
            z_and_t_FactorsForProfile.append( [float(self.channelReferences[i].zFactor), 
                                                   float(self.channelReferences[i].tFactor)] ) 
        return z_and_t_FactorsForProfile
        
    def addChannels(self, dt):
        for i in xrange(self.numberOfChannels):
            ch = SprayChannel(id='ch_'+str(i))
            self.channelBoxLayout.add_widget(ch)
            self.channelReferences.append(ch)
        self.maxButtonPressed('ch_'+str(self.channelsUsed-1))
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
                self.channelReferences[i].maxButton.state = 'normal'
            else:
                self.channelReferences[i].zSlider.disabled = True
                self.channelReferences[i].tSlider.disabled = True
                self.channelReferences[i].selectButton.disabled = True
                self.channelReferences[i].maxButton.text = 'Max'
                self.channelReferences[i].maxButton.state = 'normal'
        self.channelReferences[id].maxButton.state = 'down'
        self.channelsUsed = id + 1
        
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
        ch = self.detectSelection()
        if ch != None: 
            
            crack_angle = self.sm.get_screen('spraySet').crack_position_abs
            end_angle = int(crack_angle + self.sm.get_screen('spraySet').standby_rel_to_crack)
            
            press_time = int(self.max_press_time_in_millis * self.channelReferences[ch].tFactor)
            
            dump_angle = crack_angle + self.sm.get_screen('spraySet').dump_rel_to_crack
            angle_range = dump_angle - crack_angle
            start_angle = int(crack_angle + (angle_range * self.channelReferences[ch].zFactor))
            
            print (start_angle, press_time, end_angle)

            self.s.bounce_servo(start_angle, press_time, end_angle)
            
           

    is_test_forever_in_progress = False
    test_forever_count = 0
    test_forever_event = None

    def test_forever(self):

        if self.is_test_forever_in_progress == False: # start the repetition
            
            ch = self.detectSelection()
            if ch != None: 
                self.test_forever_count = 0
                press_time = int(self.max_press_time_in_millis * self.channelReferences[ch].tFactor)/1000.0
                print press_time
                self.test_forever_event = Clock.schedule_interval(self.fire_the_test, press_time+1)
                self.is_test_forever_in_progress = True

        else: # stop the repetition
            if self.test_forever_event != None:
                self.test_forever_event.cancel()
                self.test_forever_button.text = "TEST xN"
                self.is_test_forever_in_progress = False

    
    def fire_the_test(self, dt):
        print 'fired'
        self.test_forever_count +=1
        self.test_forever_button.text = str(self.test_forever_count)
        self.test()            
        

            
                
