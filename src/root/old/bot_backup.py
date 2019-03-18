'''
Created on 28 Aug 2017
Bot definition
@author: Ed
'''
# }}}}#[[[[[[[[[[[[ <---- addition from Poofy the cat


import sys, os
from os import listdir
if sys.platform != "win32": import serial  # @UnresolvedImport
import pickle
import math
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport

Builder.load_string("""

#:import os os

<BotSetScreen>:

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
                    canvas:
                        Color: 
                            rgba: 1,1,1,.2
                        Rectangle: 
                            size: self.size
                            pos: self.pos
                    TextInput:
                        id: fileNameTextInput
                        size_hint_y: 1
                        font_size:24
                        multiline: False
                        text: root.profileName
                        on_text: root.profileName=self.text
           
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
                        text: 'Motor wheel diameter:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24
                        id:motorWheelDiameterMM
                        input_filter: 'float'
                        multiline: False
                        text: str(root.motorWheelDiameterMM)
                        on_text: root.motorWheelDiameterMM=self.text
                    Label:
                        size_hint_x: 1  
                        text: 'mm'
                              
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
                        text: 'Motor steps per rev:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24  
                        id:motorStepsPerRev
                        input_filter: 'float'
                        multiline: False
                        text: str(root.motorStepsPerRev)
                        on_text: root.motorStepsPerRev=self.text
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
                    Label:
                        size_hint_x: 3  
                        text: 'Motor max speed:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24  
                        id:motorMaxSpeed
                        input_filter: 'int'
                        multiline: False
                        text: str(root.motorMaxSpeed)
                        on_text: root.motorMaxSpeed=self.text
                    Label:
                        size_hint_x: 1  
                        text: 'rpm?'
                              
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
                        text: 'Motor acceleration:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24
                        id:motorMaxAcceleration
                        input_filter: 'int'
                        multiline: False
                        text: str(root.motorAcceleration)
                        on_text: root.motorAcceleration=self.text
                    Label:
                        size_hint_x: 1  
                        text: 'rpmpm?'
                                
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
                    filters: ['*.bot']
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

""")

        
class BotSetScreen(Screen):

    profileName = StringProperty('Default')
    motorWheelDiameterMM = NumericProperty(26)
    motorStepsPerRev = NumericProperty(3200)
    motorMaxSpeed = NumericProperty(4000)
    motorAcceleration = NumericProperty(6000)
    p=[]

    def __init__(self, **kwargs):
        super(BotSetScreen, self).__init__(**kwargs)
        self.p.append(kwargs['profileObject'])
#         kwargs['profileObject'].testVariable1 = 1
#         print kwargs['profileObject'].testVariable1 
#         self.p[0].testVariable2 = 2
#         print self.p[0].testVariable2
        if os.path.isfile(lastSavedFilePath): self.loadLastProfileSaved()
        else: self.save()

    def on_motorWheelDiameterMM(self, *args): self.calculateStepsPerMM()
    def on_motorStepsPerRev(self, *args): self.calculateStepsPerMM()
    
    def calculateStepsPerMM(self):
        self.stepsPerMM = self.motorStepsPerRev/(math.pi * self.motorWheelDiameterMM)
    
    def save(self):
#         global self.p[0]
        self.p[0].profileName = self.profileName
        self.p[0].motorWheelDiameterMM = self.motorWheelDiameterMM
        self.p[0].motorStepsPerRev = self.motorStepsPerRev
        self.p[0].motorMaxSpeed = self.motorMaxSpeed
        self.p[0].motorAcceleration = self.motorAcceleration
        self.p[0].saveToUserLocation()
        self.p[0].saveToLastUsed()
        self.refreshFilechooser()

    def load(self, filePath):
#         global self.p[0]
        if os.path.isfile(filePath):
            with open(filePath, 'rb') as input:
                self.p[0] = pickle.load(input)
                
        print self.profileName
        print self.p[0].profileName
                
        self.profileName = self.p[0].profileName
        self.motorWheelDiameterMM = self.p[0].motorWheelDiameterMM 
        self.motorStepsPerRev = self.p[0].motorStepsPerRev
        self.motorMaxSpeed = self.p[0].motorMaxSpeed
        self.motorAcceleration = self.p[0].motorAcceleration

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
      
lastSavedFilePath = 'settings/lastUsed/' + 'bot_lastUsed'
     

# self.p[0] = BotProfile()
