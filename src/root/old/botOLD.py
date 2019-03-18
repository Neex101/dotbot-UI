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

class BotProfile(object):
    
    profileName = StringProperty('Default')
    motorWheelDiameterMM = NumericProperty(26)
    motorStepsPerRev = NumericProperty(3200)
    motorMaxSpeed = NumericProperty(4000)
    motorAcceleration = NumericProperty(6000)
    
    def saveToUserLocation(self):
        filePath = 'settings/' + self.profileName + '.bot'
        with open(filePath, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
    
    def saveToLastUsed(self):
        filePath = 'settings/lastUsed/' + 'bot_lastUsed'
        with open(filePath, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)        

        
b = BotProfile()


class BotSetScreen(Screen):

    profileName = StringProperty('Default')
    motorWheelDiameterMM = NumericProperty(26)
    motorStepsPerRev = NumericProperty(3200)
    motorMaxSpeed = NumericProperty(4000)
    motorAcceleration = NumericProperty(6000)

    def on_motorWheelDiameterMM(self, *args): self.calculateStepsPerMM()
    def on_motorStepsPerRev(self, *args): self.calculateStepsPerMM()
    
    def calculateStepsPerMM(self):
        self.stepsPerMM = self.motorStepsPerRev/(math.pi * self.motorWheelDiameterMM)
        print self.stepsPerMM 
    
    def save(self):
        b.profileName = self.profileName 
        b.motorWheelDiameterMM = self.motorWheelDiameterMM
        b.motorStepsPerRev = self.motorStepsPerRev
        b.motorMaxSpeed = self.motorMaxSpeed
        b.motorAcceleration = self.motorAcceleration
        b.saveToUserLocation()
        b.saveToLastUsed()
        self.refreshFilechooser()

    def load(self, filePath):
        global b
        if os.path.isfile(filePath):
            with open(filePath, 'rb') as input:
                b = pickle.load(input)
        self.profileName = b.profileName
        self.motorWheelDiameterMM = b.motorWheelDiameterMM 
        self.motorStepsPerRev = b.motorStepsPerRev
        self.motorMaxSpeed = b.motorMaxSpeed
        self.motorAcceleration = b.motorAcceleration
    
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
        
    def init(self):
        self.loadLastProfileSaved()
        
    def loadLastProfileSaved(self):
        filePath = 'settings/lastUsed/' + 'bot_lastUsed'
        self.load(filePath)

    
    
class WhateverProfile(object):

############### SetUp: Spray profile and Canvas

#     sprayServoAngleOn = 180
#     sprayServoAngleOff = 0
#     maxSprayTime = 0.0
#     minSprayTime = 0.0
#     canvasXmm = 0
#     canvasYmm = 0
#     datumHeightmm = 1000
#     imageLiftmm = 2000
#     dotDiametermm = 50

    
    
    
    def calculateImpliedParameters(self):
#         self.calculateStepsPerStringMM()
#         self.setDatumCoordsMM()
        pass
     
    def calculateStepsPerStringMM(self):
        self.stepsPermm = self.motorStepsPerRev/(math.pi * self.motorWheelDiameterMM)
    
############# Spray

    def sprayOn(self, serialLink):
        self.setSprayServoToAngle(serialLink, self.sprayServoAngleOn)

    def sprayOff(self, serialLink):
        self.setSprayServoToAngle(serialLink, self.sprayServoAngleOff)
           
    def getDurationForPixelGreyscaleValue(self, sprayDurationFraction):
        seconds = sprayDurationFraction  * (self.maxSprayTime - self.minSprayTime) + self.minSprayTime
        millis = int(seconds * 1000)
        return millis
        
    
############# Image processing
        
    imagePixels = ""
    imageXPixels = 0
    imageYPixels = 0
    imageWidthMM = 0
    imageHeightMM = 0
    imageHeightWithLiftMM = 0
    
    def defineImage(self, imagePath):
        image = CoreImage(imagePath, keep_data = True)
        self.imagePixels = image.size
        self.imageXPixels = image.width
        self.imageYPixels = image.height
        self.imageWidthMM = image.width * self.dotDiametermm
        self.imageHeightMM = image.height * self.dotDiametermm
        self.imageHeightWithLiftMM = self.imageHeightMM + self.imageLiftmm
        
    def getPixelCoordsInMM(self, xy_pixels):    #See docs for definition of datum (bottom left)
        x_pixel = xy_pixels[0]
        y_pixel = xy_pixels[1] 
        x_coordMM = (self.canvasXmm / 2) - (self.imageWidthMM / 2) + (x_pixel - 1) * self.dotDiametermm
        y_coordMM = self.imageLiftmm + self.imageHeightMM - (y_pixel - 1) * self.dotDiametermm
        return [x_coordMM, y_coordMM]
        
    def getPixelGreyValue(self, xy_pixels, imagePath):
        image = CoreImage(imagePath, keep_data = True)
        rgb = image.read_pixel(xy_pixels[0], xy_pixels[1])
        return (rgb[0]+rgb[1]+rgb[2])/3 #averaging method (see for more options: https://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/)
    
############ XY positioning calculations

    datumCoordsMM = [0,0] # x,y coords for datum position
    
    def getStringStepsForCoordsMM(self, coordsMM):

        x_coordMM = coordsMM[0]
        y_coordMM = coordsMM[1]
        leftStringMM = math.sqrt(
            x_coordMM**2 + 
            (self.canvasYmm - y_coordMM)**2 
        )
        rightStringMM = math.sqrt(
            (self.canvasXmm - x_coordMM)**2 + 
            (self.canvasYmm - y_coordMM)**2 
        )
        leftStringSteps = int(leftStringMM * self.stepsPermm)
        rightStringSteps = int(rightStringMM * self.stepsPermm)
        return [leftStringSteps, rightStringSteps]

    def setDatumCoordsMM(self):
        self.datumCoordsMM = [self.canvasXmm/2, self.datumHeightmm]
        
############# Printing functions

    def setBotCoordsToDatum(self):
        self.coordsMM = self.datumCoordsMM

    def printNewDot(self, xy_pixels, imagePath, serialLink):

        #goto pixel location
        self.goToCoordsMM(self.getPixelCoordsInMM(xy_pixels), serialLink)
        #block until motors complete (awaiting serial message '#')
        if sys.platform != "win32": 
            response = "" 
            while True:
                response = serialLink.readline()
                if response != "": 
                    print response
                    break
        
        #spray according to pixel definition
        greyscalevalue = self.getPixelGreyValue(xy_pixels, imagePath)
        print greyscalevalue
        duration = self.getDurationForPixelGreyscaleValue(greyscalevalue)
        print duration
        self.sprayServoForDuration(serialLink, self.sprayServoAngleOn, duration, self.sprayServoAngleOff)
        #block until motors complete (awaiting serial message '#')
        if sys.platform != "win32": 
            response = "" 
            while True:
                response = serialLink.readline()
                if response != "": 
                    print response
                    break
        
############## Serial commands
    
    def moveLeftMotorMM(self, increment, serialLink):
        if sys.platform != "win32": 
            serialLink.write("LM " + str(increment*self.stepsPermm) + "\n")
    
    def moveRightMotorMM(self, increment, serialLink):
        if sys.platform != "win32": 
            serialLink.write("RM " + str(increment*self.stepsPermm) + "\n")

    def setMotorStepsToDatumPos(self, serialLink):
        if sys.platform != "win32": 
            steps = self.getStringStepsForCoordsMM(self.datumCoordsMM)
            serialLink.write("SD " + str(steps[0]) + "\n")
    
    def goToCoordsMM(self, coordsMM, serialLink):
        if sys.platform != "win32":
            steps = self.getStringStepsForCoordsMM(coordsMM)
            serialLink.write("BM L" + str(steps[0]) + " R" + str(steps[1]) + "\n")        
        
    def goToDatum(self, serialLink):
        if sys.platform != "win32":
            steps = self.getStringStepsForCoordsMM(self.datumCoordsMM)
            serialLink.write("BM L" + str(steps[0]) + " R" + str(steps[1]) + "\n")
        
    def setSprayServoToAngle(self, serialLink, degrees):
        if sys.platform != "win32": 
            serialLink.write("SS " + str(degrees) + "\n")         
    
    def sprayServoForDuration(self, serialLink, setDegrees, duration, rtnDegrees):
        if sys.platform != "win32": 
            serialLink.write("BS A" + str(setDegrees) + " D" + str(duration) + " B" + str(rtnDegrees) + "\n") 
