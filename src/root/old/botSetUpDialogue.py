'''
Created on 19 Aug 2017

@author: Ed
'''
# config
from kivy.config import Config
import ImagePath
# from root.main_wallBot import serialLink
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

if sys.platform != "win32": import serial  # @UnresolvedImport

Builder.load_string("""
    
<BotSetScreen>:

    on_enter: 
        root.refreshSetupLabels()

    spray_indicator:spray_indicator
    sprayTimeInputLabel:sprayTimeInputLabel
    minSprayTimeLabel:minSprayTimeLabel
    maxSprayTimeLabel:maxSprayTimeLabel
    servoAngleInputLabel:servoAngleInputLabel
    sprayOnAngleLabel:sprayOnAngleLabel
    sprayOffAngleLabel:sprayOffAngleLabel
    canvasValue:canvasValue
    canvasXLabel:canvasXLabel
    canvasYLabel:canvasYLabel
    datumHeightLabel:datumHeightLabel
    imageLiftLabel:imageLiftLabel
    dotDiameterLabel:dotDiameterLabel
    machineValue:machineValue
    settingsNameLabel:settingsNameLabel
    accelerationLabel:accelerationLabel
    motorStepsPerRevLabel:motorStepsPerRevLabel
    motorWheelDiameterLabel:motorWheelDiameterLabel
    motorMaxSpeedLabel:motorMaxSpeedLabel
    
    
    Accordion:
        orientation: 'horizontal'

        AccordionItem:
            title: 'TRIGGER'

            GridLayout:
                cols: 1
                orientation: 'vertical'
                padding: 5
                spacing: 5
                
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: 1
            
                    Button:
                        text: 'Max angle'
                        on_press: root.maxServoAngleGo()
                    Label:
                        id: servoAngleInputLabel
                        text: '0'
                    Button:
                        text: '+'
                        on_press: root.plusServoAngleGo()
                    Button:
                        text: '+ +'
                        on_press: root.plusPlusServoAngleGo()

                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: 1

                    Button:
                        text: 'Min angle'
                        on_press: root.minServoAngleGo()
                    Label:
                        text: ''
                    Button:
                        text: '-'
                        on_press: root.minusServoAngleGo()
                    Button:
                        text: '- -'
                        on_press: root.minusMinusServoAngleGo()

                Label:
                    text: ''

                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: 1
            
                    Button:
                        text: 'Spray On'
                        on_press: root.sprayOnAngleGo()
                    Label:
                        id: sprayOnAngleLabel
                        text: '180'
                    Button:
                        text: 'Update'
                        on_press: root.updateSprayAngleOn()
                        
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: 1
            
                    Button:
                        text: 'Spray Off'
                        on_press: root.sprayOffAngleGo()
                    Label:
                        id: sprayOffAngleLabel
                        text: '0'
                    Button:
                        text: 'Update'
                        on_press: root.updateSprayAngleOff()
                        
                Button:
                    size_hint_y: 1
                    text: 'Hold to Spray'
                    on_press: root.sprayOnAngleGo()
                    on_release: root.sprayOffAngleGo()

                Button:
                    size_hint_y: 1
                    text: 'Spray profile'
                    on_press: 
                        root.manager.transition.direction = 'down'
                        root.manager.current = 'sprayProfile'
                
        AccordionItem:
            title: 'SATURATION'
            
            GridLayout:
    
                cols: 1
                orientation: 'vertical'
                padding: 5
                spacing: 5
                
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '100dp'
            
                    Button:
                        text: 'Hold to Spray'
                        on_press: root.sprayButtonPushed()
                        on_release: root.sprayButtonReleased()
                    Label:
                        id: sprayTimeInputLabel
                        text: '0.0'
                    Button:
                        text: '+'
                        on_press: root.addButtonPushed()

                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '100dp'

                    Button:
                        text: 'Test time'
                        on_press: root.testSprayButtonPushed()
                    Label:
                        id: spray_indicator
                        text: ''
                    Button:
                        text: '-'
                        on_press: root.minusButtonPushed()

                Label:
                    text: ''

                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '100dp'
            
                    Button:
                        text: 'Max Spray'
                        on_press: root.maxSprayButtonPushed()
                    Label:
                        id: maxSprayTimeLabel
                        text: '0.0'
                    Button:
                        text: 'Update'
                        on_press: root.updateMaxSprayTime()

                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '100dp'
            
                    Button:
                        text: 'Min Spray'
                        on_press: root.minSprayButtonPushed()
                    Label:
                        id: minSprayTimeLabel
                        text: '0.0'
                    Button:
                        text: 'Update'
                        on_press: root.updateMinSprayTime()

        AccordionItem:
            title: 'CANVAS'
 
            GridLayout:
                cols: 1
                orientation: 'vertical'
                padding: 5
                spacing: 5
 
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '60dp'
            
                    Label:
                        text: 'Value:'
                    TextInput:
                        id:canvasValue
                        size_hint_y: None
                        height: '50dp'
                        multiline: False
                        text: '0'
                        input_type: 'number'
                        input_filter: 'int'
                    Label:
                        text: 'mm'

                Label:
                    text: ''
            
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '80dp'
            
                    Label:
                        text: 'Canvas X'
                    Label:
                        id: canvasXLabel
                        text: '0'
                    Button:
                        text: 'Update'
                        on_press: root.updateCanvasXButtonPressed() 

                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '80dp'
            
                    Label:
                        text: 'Canvas Y'
                    Label:
                        id: canvasYLabel
                        text: '0'
                    Button:
                        text: 'Update'
                        on_press: root.updateCanvasYButtonPressed() 

                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '80dp'
            
                    Label:
                        text: 'Datum Height'
                    Label:
                        id: datumHeightLabel
                        text: '0'
                    Button:
                        text: 'Update'
                        on_press: root.updateDatumHeightButtonPressed() 

                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '80dp'
            
                    Label:
                        text: 'Image Lift'
                    Label:
                        id: imageLiftLabel
                        text: '0'
                    Button:
                        text: 'Update'
                        on_press: root.updateImageLiftButtonPressed() 

                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '80dp'
            
                    Label:
                        text: 'Dot diameter'
                    Label:
                        id: dotDiameterLabel
                        text: '0'
                    Button:
                        text: 'Update'
                        on_press: root.updateDotDiameterButtonPressed() 

        AccordionItem:
            title: 'MACHINE SETTINGS'
 
            GridLayout:
                cols: 1
                orientation: 'vertical'
                padding: 5
                spacing: 5
 
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '60dp'
            
                    Label:
                        text: 'Value:'
                    TextInput:
                        id:machineValue
                        size_hint_y: None
                        height: '50dp'
                        multiline: False
                        text: ''
                    Label:
                        text: '<<< input'

                Label:
                    text: ''
            
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '80dp'
            
                    Label:
                        text: 'Motor wheel diameter (mm)'
                    Label:
                        id: motorWheelDiameterLabel
                        text: '0'
                    Button:
                        text: 'Update'
                        on_press: root.updateMotorWheelDiameterButtonPressed()      
                               
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '80dp'
            
                    Label:
                        text: 'Motor steps per rev'
                    Label:
                        id: motorStepsPerRevLabel
                        text: '0'
                    Button:
                        text: 'Update'
                        on_press: root.updateMotorStepsPerRevButtonPressed()

                              
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '80dp'
            
                    Label:
                        text: 'Max speed'
                    Label:
                        id: motorMaxSpeedLabel
                        text: '0'
                    Button:
                        text: 'Update'
                        on_press: root.updateMaxSpeedButtonPressed()    
                        
                BoxLayout:
                    padding: 5
                    spacing: 5
                    orientation: "horizontal"
                    size_hint_y: None
                    height: '80dp'
            
                    Label:
                        text: 'Acceleration'
                    Label:
                        id: accelerationLabel
                        text: '0'
                    Button:
                        text: 'Update'
                        on_press: root.updateAccelerationButtonPressed() 
                        
        AccordionItem:
            title: 'LOAD OUT'


            GridLayout:
                cols: 1
                orientation: 'vertical'
                padding: 10
                spacing: 10
            
                Label:
                    id: settingsNameLabel
                    text: ''
                    
                Button:
                    text: 'Load'
                    on_press: 
                        root.manager.transition.direction = 'left'
                        root.manager.current = 'settingsSave'
                Button:
                    text: 'Save As'
                    on_press: 
                        root.manager.transition.direction = 'left'
                        root.manager.current = 'settingsSave'
                Button:
                    text: 'Save'
                    on_press: 
                        root.save()
                Button:
                    text: 'Quit without save'
                    on_press: 
                        root.manager.transition.direction = 'left'
                        root.manager.current = 'home'

            
""")

b = None
serialLink = None

def init(botObject, serialObject):
    global b, serialLink
    b = botObject
    serial = serialObject

# SETUP    
class BotSetScreen(Screen):
        
    #Screen Inputs
    servoAngleInput = 0
    sprayTimeInput = 0.0
    maxServoAngle = 180
    minServoAngle = 0
    angleIncrementSmall = 1
    angleIncrementBig = 5
    saturationIncrement = 0.05
    sprayStartTime = 0.0
    sprayEndTime = 0.0

    def refreshSetupLabels(self):
                
        # Inputs
        self.sprayTimeInputLabel.text = str(format(self.sprayTimeInput, '.2f'))
        self.servoAngleInputLabel.text = str(self.servoAngleInput)
        
        # bot properties
        self.settingsNameLabel.text = str(b.settingsName)
        self.sprayOnAngleLabel.text = str(b.sprayServoAngleOn)
        self.sprayOffAngleLabel.text = str(b.sprayServoAngleOff)
        self.minSprayTimeLabel.text = str(format(b.minSprayTime, '.2f'))
        self.maxSprayTimeLabel.text = str(format(b.maxSprayTime, '.2f'))
        self.canvasXLabel.text = str(b.canvasXmm)
        self.canvasYLabel.text = str(b.canvasYmm)
        self.datumHeightLabel.text = str(b.datumHeightmm)
        self.imageLiftLabel.text = str(b.imageLiftmm)
        self.dotDiameterLabel.text = str(b.dotDiametermm)
        self.motorWheelDiameterLabel.text = str(b.motorWheelDiameterMM)
        self.motorStepsPerRevLabel.text= str(b.motorStepsPerRev) 
        self.accelerationLabel.text= str(b.motorAcceleration) 
        self.motorMaxSpeedLabel.text= str(b.motorMaxSpeed)
#         datumScreen.datumHeightTargetLabel.text = str("Datum height: " + str(b.datumHeightmm))
        
        b.calculateImpliedParameters()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# TRIGGER SET
# Setting up the servo to be at a position to start/stop spraying
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def setSprayServoToAngle(self, degrees):
        self.servoAngleInput = degrees
        self.refreshSetupLabels()
        if sys.platform != "win32":
            b.setSprayServoToAngle(serialLink, self.servoAngleInput)
        
    def maxServoAngleGo(self):
        self.setSprayServoToAngle(self.maxServoAngle)
        
    def minServoAngleGo(self):
        self.setSprayServoToAngle(self.minServoAngle)
    
    def plusServoAngleGo(self):
        self.servoAngleInput = self.servoAngleInput + self.angleIncrementSmall
        self.setSprayServoToAngle(self.servoAngleInput)
    
    def plusPlusServoAngleGo(self):
        self.servoAngleInput = self.servoAngleInput + self.angleIncrementBig
        self.setSprayServoToAngle(self.servoAngleInput)
        
    def minusServoAngleGo(self):
        self.servoAngleInput = self.servoAngleInput - self.angleIncrementSmall
        self.setSprayServoToAngle(self.servoAngleInput)
    
    def minusMinusServoAngleGo(self):
        self.servoAngleInput = self.servoAngleInput - self.angleIncrementBig
        self.setSprayServoToAngle(self.servoAngleInput)
        
    def sprayOnAngleGo(self):
        self.setSprayServoToAngle(b.sprayServoAngleOn)
 
    def sprayOffAngleGo(self):
        self.setSprayServoToAngle(b.sprayServoAngleOff)
        
    def updateSprayAngleOn(self):
        b.sprayServoAngleOn = self.servoAngleInput
        self.refreshSetupLabels()
        
    def updateSprayAngleOff(self):
        b.sprayServoAngleOff = self.servoAngleInput
        self.refreshSetupLabels()
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# SATURATION
# Setting the duration of sprayForDuration to achive max/min sprayForDuration saturation (gradient)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    def sprayForDuration(self, secondsToSpray):
        self.sprayOn()
        Clock.schedule_once(lambda dt: self.sprayOff(), secondsToSpray)
    
    def sprayOn(self):
        self.spray_indicator.text="SPRAY!"
        if sys.platform != "win32":
            b.sprayOn(serialLink)
     
    def sprayOff(self):
        self.spray_indicator.text=""
        if sys.platform != "win32":
            b.sprayOff(serialLink)
  
    def sprayButtonPushed(self):
        self.sprayOn()
        self.sprayStartTime = time.time()
        
    def sprayButtonReleased(self):
        self.sprayOff()
        self.sprayEndTime = time.time()
        self.sprayTimeInput = self.sprayEndTime - self.sprayStartTime
        self.refreshSetupLabels()

    def minusButtonPushed(self):
        self.sprayTimeInput = self.sprayTimeInput - self.saturationIncrement
        self.refreshSetupLabels()

    def addButtonPushed(self):
        self.sprayTimeInput = self.sprayTimeInput + self.saturationIncrement
        self.refreshSetupLabels()
    
    def testSprayButtonPushed(self):
        self.sprayForDuration(self.sprayTimeInput)

    def maxSprayButtonPushed(self):
        self.sprayForDuration(b.maxSprayTime)
            
    def minSprayButtonPushed(self):
        self.sprayForDuration(b.minSprayTime)    

    def updateMaxSprayTime(self):
        b.maxSprayTime = self.sprayTimeInput
        self.refreshSetupLabels()
        
    def updateMinSprayTime(self):
        b.minSprayTime = self.sprayTimeInput
        self.refreshSetupLabels()
        
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# CANVAS
# Setting the duration of sprayForDuration to achive max/min sprayForDuration saturation (gradient)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>       

    def updateCanvasXButtonPressed(self):
        b.canvasXmm = int(self.canvasValue.text)
        self.refreshSetupLabels()
        
    def updateCanvasYButtonPressed(self): 
        b.canvasYmm = int(self.canvasValue.text)
        self.refreshSetupLabels()
    
    def updateDatumHeightButtonPressed(self):
        b.datumHeightmm = int(self.canvasValue.text)
        self.refreshSetupLabels()
        
    def updateImageLiftButtonPressed(self):
        b.imageLiftmm = int(self.canvasValue.text)
        self.refreshSetupLabels()
    
    def updateDotDiameterButtonPressed(self):
        b.dotDiametermm = int(self.canvasValue.text)
        self.refreshSetupLabels()
        
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# MACHINE
# Setting general machine parameters
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>          
    
    def updateMotorWheelDiameterButtonPressed(self):
        b.motorWheelDiameterMM = self.machineValue.text
        self.refreshSetupLabels() 
           
    def updateMotorStepsPerRevButtonPressed(self):
        b.motorStepsPerRev = self.machineValue.text
        self.refreshSetupLabels() 
           
    def updateMaxSpeedButtonPressed(self):
        b.motorMaxSpeed = self.machineValue.text
        self.refreshSetupLabels()
        
    def updateAccelerationButtonPressed(self):
        b.motorAcceleration = self.machineValue.text
        self.refreshSetupLabels()
        
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# LOAD OUT
# Load settings or saveAs new settings, before quitting
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>     
            
    def printBotSettings(self):
        b.printSettingsList()
    
#     def save(self):
#         homeScreen.checkQ()
#         fileName = b.settingsName
#         filePath = settingsDir + fileName
#         with open(filePath, 'wb') as output:
#             pickle.dump(b, output)
