'''
Created on 19 Aug 2017

@author: Ed
'''
# config
from kivy.config import Config
import ImagePath
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
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    TextInput:
                        id: fileNameTextInput
                        font_size:24
                        multiline: False
                        text: root.profileName
                        on_text: root.profileName=self.text

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
                        Button:
                            size_hint_y: 1  
                            text: 'UP'
                            on_release: root.goUp()
                        Label:
                            size_hint_y: .5  
                            text: str(root.position)
                        Button:
                            size_hint_y: 1  
                            text: 'Down'
                            on_release: root.goDown()
                        Button:
                            size_hint_y: 1  
                            text: 'Profile'
                            on_release: 
                                root.manager.transition.direction = 'down'
                                root.manager.current = 'sprayChannels'                          

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
                                text: 'Unload'
                                on_release: root.goToUnload()
                            TextInput:
                                size_hint_x: 1
                                font_size:24
                                input_filter: 'int'
                                multiline: False
                                text: str(root.unload_StepsRelToCrack)
                                on_text: root.unload_StepsRelToCrack=self.text
                            Label:
                                size_hint_x: 1  
                                text: 'steps'
                                      
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
                                input_filter: 'int'
                                multiline: False
                                text: str(root.standby_StepsRelToCrack)
                                on_text: root.standby_StepsRelToCrack=self.text
                            Label:
                                size_hint_x: 1  
                                text: 'steps'
                                      
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
                                size_hint_x: 2
                                text: 'Set'
                                on_release: 
                                      
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
                                input_filter: 'int'
                                multiline: False
                                text: str(root.dump_StepsRelToCrack)
                                on_text: root.dump_StepsRelToCrack=self.text
                            Label:
                                size_hint_x: 1  
                                text: 'steps'
                                
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
                    root.loadLastProfileSaved()
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'home'                          
            Button:
                text: 'Save'
                on_release: 
                    root.save()
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'home'                          
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
                on_press: 
                    root.manager.transition.direction = 'up'
                    root.manager.current = 'spraySet'                          
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


lastSavedFilePath = 'settings/lastUsed/' + 'spray_lastUsed'
settingsDir = 'settings/'

class SpraySetScreen(Screen):
    
    profileName = StringProperty('Default')
    unload_StepsRelToCrack = NumericProperty(-80)
    standby_StepsRelToCrack = NumericProperty(-20)
    dump_StepsRelToCrack = NumericProperty(30)
    position = NumericProperty(0)
    
    ### Channel class variables
    numberOfChannels = 10
    zFactorProfile = []
    tFactorProfile = []
    channelsUsed = numberOfChannels


    def __init__(self, **kwargs):
        super(SpraySetScreen, self).__init__(**kwargs)
     
        for x in xrange(self.numberOfChannels):
            self.zFactorProfile.append(0)
            self.tFactorProfile.append(0)
        if os.path.isfile(lastSavedFilePath): self.loadLastProfileSaved()
        self.sprayChannelScreen = SprayChannelScreen(name='sprayChannels', 
                                                zFactorProfile=self.zFactorProfile,
                                                tFactorProfile=self.tFactorProfile, 
                                                numberOfChannels=self.numberOfChannels,
                                                channelsUsed=self.channelsUsed)
        kwargs['screen_manager'].add_widget(self.sprayChannelScreen)

    def save(self):
        # note order is important here: must match loading order. TODO: switch to dict?
        parametersList = [self.profileName, self.unload_StepsRelToCrack, self.standby_StepsRelToCrack, self.dump_StepsRelToCrack, self.position,
                          self.numberOfChannels, self.zFactorProfile, self.tFactorProfile, self.channelsUsed]
        
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
            self.unload_StepsRelToCrack = p[1]
            self.standby_StepsRelToCrack = p[2]
            self.dump_StepsRelToCrack = p[3]
            self.position = p[4]
            self.numberOfChannels = p[5]
            self.zFactorProfile = p[6]
            self.tFactorProfile = p[7]
            self.channelsUsed = p[8]
    
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
        
    def loadLastProfileSaved(self):
        self.load(lastSavedFilePath)


class SprayChannel(Widget):

    zFactor = NumericProperty(0)
    tFactor = NumericProperty(0)

    def __init__(self, **kwargs):
        super(SprayChannel, self).__init__(**kwargs)
        
        print 'z: ' + str(kwargs['zFactorValue'])
        print 't: ' + str(kwargs['tFactorValue'])
        
#         self.zFactor = NumericProperty(int(kwargs['zFactorValue']))
#         self.tFactor = NumericProperty(int(kwargs['tFactorValue']))
        self.zFactor = kwargs['zFactorValue']
        self.tFactor = kwargs['tFactorValue']
        
    def maxButtonPressed(self, channelID):
        self.parent.parent.parent.maxButtonPressed(channelID)

class SprayChannelScreen(Screen):
    
    channelReferences = []
    
    def __init__(self, **kwargs):
        super(SprayChannelScreen, self).__init__(**kwargs)
        self.zFactorProfile=kwargs['zFactorProfile']
        self.tFactorProfile=kwargs['tFactorProfile']
        self.numberOfChannels=kwargs['numberOfChannels']
        self.channelsUsed = kwargs['channelsUsed']
        Clock.schedule_once(self.addChannels)
        
    def addChannels(self, dt):
        for i in xrange(self.numberOfChannels):
            print i
            ch = SprayChannel(id='ch_'+str(i), 
                              zFactorValue=self.zFactorProfile[i], 
                              tFactorValue=self.tFactorProfile[i])
            self.channelBoxLayout.add_widget(ch)
            self.channelReferences.append(ch)
        self.channelReferences[self.numberOfChannels-1].maxButton.state = 'down'
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
            else:
                self.channelReferences[i].zSlider.disabled = True
                self.channelReferences[i].tSlider.disabled = True
                self.channelReferences[i].selectButton.disabled = True
                self.channelReferences[i].maxButton.text = 'Max'
        channelsUsed = id + 1
        
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

    def save(self):
        
        
        #### UNTESTED
        
        
        p.channelsUsed = self.channelsUsed
        p.zFactors = []
        p.tFactors = []
        for i in xrange(self.numberOfChannels):
            p.zFactors.append(self.channelReferences[i].zFactor)
            p.tFactors.append(self.channelReferences[i].tFactor)
        p.saveToUserLocation()
        p.saveToLastUsed()
        
    def load(self):
        
        #### UNTESTED
        
        self.channelsUsed = p.channelsUsed
        for i in xrange(self.numberOfChannels):
            self.channelReferences[i].zFactor = p.zFactors[i]
            self.channelReferences[i].tFactor = p.tFactors[i]
        self.maxButtonPressed('ch_'+str(self.channelsUsed-1))

                
