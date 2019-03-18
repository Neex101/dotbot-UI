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
import bot, triggerProfile, botSetUpDialogue
import math
import ntpath
from kivy.core.image import Image as CoreImage

if sys.platform != "win32": import serial  # @UnresolvedImport

Builder.load_string("""

#:import Clock kivy.clock.Clock
        
# blank screen hides garish white video startup
<BlankScreen>:
#     on_enter: Clock.schedule_once(self.startSplash, 3)
    on_enter: Clock.schedule_once(self.startSplash, 0)
    canvas.before:
        Color:
            rgba: 0,0,0,0

<SplashScreen>:
#     on_enter: Clock.schedule_once(self.goToMainScreen, 4)
    on_enter: Clock.schedule_once(self.goToMainScreen, 0)
    Video:
        source: "splash.mp4"
        state: "play"

<HomeScreen>:
    imagePreview:imagePreview
    imageData:imageData
    magicGoButton:magicGoButton
    botStatsText:botStatsText
    
#     on_enter: Clock.schedule_once(self.checkQ, 0)
    on_enter: root.checkQ()
   
    
    GridLayout:
        cols: 4
        orientation: 'horizontal'
        padding: 20
        spacing: 10
        
        Image:
            source: 'logo.png'
        Button:
            text: 'Load file'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'local_file_load'
        Button:
            text: 'Bot setup'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'botsetup'
        Button:
            text: 'Set Datum'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'datum'
        Label:
            id: botStatsText
            text: 'No Serial!'
        Image:
            id: imagePreview
            source: 'defaults/noimageloaded.png'
        Label:
            id: imageData
            text: '<Job stats here>'
        Button:
            text: 'Go'
            background_color: 0, 1, 0, 1
            id: magicGoButton
            on_press: root.goPrint() 
                


<SettingsSaveScreen> 
    on_enter: 
        root.refreshFilechooser()
        fileNameTextEntry.text=''
        
    fileNameTextEntry:fileNameTextEntry
    filechooser:filechooser

    BoxLayout:
        padding: 20
        spacing: 10
        size: root.size
        pos: root.pos
        orientation: "vertical"
        
        Label:
            halign: 'left'
            text: 'Save As...'
            size_hint_y: None
            height: '30dp'
        BoxLayout:
            size_hint_y: None
            height: 50

            TextInput:
                id:fileNameTextEntry
                size_hint_y: None
                height: '50dp'
                size_hint_x: None
                width: '640dp'
                multiline: False
                text: ''
            Button:
                text: "Save"
                on_release: 
                    root.saveAs() 
        
        Label:
            halign: 'left'
            text: 'Or load...'
            size_hint_y: None
            height: '30dp'

        
        FileChooserListView:
            id: filechooser
            path: ''
        
        BoxLayout:
            size_hint_y: None
            height: 50

            Button:
                text: "Delete selected"
                on_release: 
                    root.deleteSelected(filechooser.selection)
            Button:
                text: "Delete all"
                on_release: 
                    root.deleteAll()
            Button:
                text: "Cancel"
                on_release: 
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'botsetup'
            Button:
                text: "Load"
                on_release: 
                    root.open(filechooser.selection) 
 
<DatumScreen>:

    datumHeightTargetLabel:datumHeightTargetLabel
    
    GridLayout:
        cols: 1
        orientation: 'vertical'
        padding: 20
        spacing: 10

        BoxLayout:
            size_hint_y: None
            height: 50
            Label:
                text: 'Left'
            Label:
                text: 'Right'
        BoxLayout:
            size_hint_y: None
            height: 320
            GridLayout:
                cols: 2
                orientation: 'vertical'
                padding: 10
                spacing: 20
            
                Button:
                    id: leftCCW
                    text: 'leftCCW' 
                    on_press: 
                        root.leftCCW() 
                Button:
                    id: leftCW
                    text: 'leftCW' 
                    on_press: 
                        root.leftCW()
                Button:
                    id: leftCCWplus
                    text: 'leftCCW+' 
                    on_press: 
                        root.leftCCWplus() 
                Button:
                    id: leftCWplus
                    text: 'leftCW+' 
                    on_press: 
                        root.leftCWplus()                                    
            GridLayout:
                cols: 2
                orientation: 'vertical'
                padding: 10
                spacing: 20
                
                Button:
                    id: rightCCW
                    text: 'rightCCW' 
                    on_press: 
                        root.rightCCW() 
                Button:
                    id: rightCW
                    text: 'rightCW' 
                    on_press: 
                        root.rightCW()
                Button:
                    id: rightCCWplus
                    text: 'rightCCW+' 
                    on_press: 
                        root.rightCCWplus() 
                Button:
                    id: rightCWplus
                    text: 'rightCW+' 
                    on_press: 
                        root.rightCWplus()  
            
        BoxLayout:
            size_hint_y: None
            height: 70
            padding: 10
            spacing: 20

            Label:
                id: datumHeightTargetLabel
                text: 'Datum height: '                     
            Button:
                text: "Quit"
                on_release: 
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'home'


            
<PrintSetScreen>:

    stats_button:stats_button

    GridLayout:
        cols: 3
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Button:
            text: 'Load file'
            on_press:
                root.manager.transition.direction = 'down'
                root.manager.current = 'local_file_load'
        Image:
            source: 'ball.png'
        Button:
            id: stats_button
            text: 'Statistics: awaiting file...'

        Button:
            text: 'Quit'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'home'
        Button:
            text: 'Move'    
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'move'
        Button:
            text: 'Cut'
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'print_check'
            



<ModelPreview>:

    GridLayout:
        cols: 1
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Label:
            text: "Test"
        Button:
            text: "Cancel"
            on_release: 
                root.cancel() 


<PrintCheckScreen>:

    GridLayout:
        cols: 1
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Button:
            text: 'Have you cleaned the tray?'
        Button:
            text: 'Have you calibrated the platform?'
        Button:
            text: 'Cancel'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'print_set'
        Button:
            text: ''    
            disabled: True
        Button:
            text: 'Print'
            background_color: 0, 1, 0, 1
            on_press:
                root.projector_go()
                root.manager.transition.direction = 'left'
                root.manager.current = 'print_status'
                
<LocalFileLoadScreen>:
    filechooser:filechooser
    fileNameTextEntry:fileNameTextEntry
    usbButton:usbButton

    BoxLayout:
        padding: 20
        spacing: 10
        size: root.size
        pos: root.pos
        orientation: "vertical"

        BoxLayout:
            size_hint_y: None
            height: '48dp'

            Button:
                id: usbButton
                text: 'Import from USB'
                on_release: root.checkUSB()
            Button:
                text: 'Refresh'
                on_release:
                    root.refreshFilechooser()
                    
        FileChooserIconView:
            id: filechooser
            path: 'C:\'
            
        TextInput:
            id:fileNameTextEntry
            size_hint_y: None
            height: '50dp'
            multiline: False
            text: ''

        BoxLayout:
            size_hint_y: None
            height: 50

            Button:
                text: "Delete selected"
                on_release: 
                    root.deleteSelected(filechooser.selection)
                    root.refreshFilechooser()
            Button:
                text: "Delete all"
                on_release: 
                    root.deleteAll()
                    root.refreshFilechooser()
            Button:
                text: "Cancel"
                on_release: 
                    root.quit()
            Button:
                text: "Select"
                on_release: 
                    root.load(filechooser.path, filechooser.selection)
    
<USBFileLoadScreen>:
    filechooser:filechooser
    
    BoxLayout:
        padding: 20
        spacing: 10
        size: root.size
        pos: root.pos
        orientation: "vertical"

        BoxLayout:
            size_hint_y: None
            height: '48dp'
    
            Button:
                text: 'Refresh USB'
                on_release:
                    root.manager.current = 'usb_file_load'

        FileChooserIconView:
            id: filechooser
            path: 'C:\'

        BoxLayout:
            size_hint_y: None
            height: 30
                    
            Button:
                text: "Cancel"
                on_release: 
                    root.quit()
            Button:
                text: "Import"
                on_release: 
                    root.importFile(filechooser.path, filechooser.selection)




            
<PrintStatusScreen>:
    GridLayout:
        cols: 1
        orientation: 'vertical'
        padding: 20
        spacing: 10
        
        Label:
            text: ''
        Label:
            font_size: '100sp'
            text: '00:00:00'
        Label:
            text: ''
        Button:
            text: 'Pause'
        Button:
            text: 'Quit Job'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'home'
            
""")


class BlankScreen(Screen):
    def startSplash(self, dt):
        sm.current = 'splash'

class SplashScreen(Screen):
    def goToMainScreen(self, dt):
        sm.current = 'home'


class HomeScreen(Screen):
    
    global fileToPrintPath
    
    def checkQ(self):
        self.magicGoButton.disabled = True
        for fname in os.listdir(printQueueFolder):
            if fname.endswith(('.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG')):

                self.fileToPrintPath = printQueueFolder + str(fname)
                self.imagePreview.source = self.fileToPrintPath
                b.defineImage(self.fileToPrintPath)
                
                self.imageData.text = "Datum height: " + str(b.datumHeightmm/1000.00) + "m" +\
                    "\n\nCanvas Width: " + str(b.canvasXmm/1000.0) + "m" +\
                    "\nCanvas Height: " + str(b.canvasYmm/1000.00) + "m" +\
                    "\n\nImg pixels: " + str(b.imagePixels) +\
                    "\nImg Width: " + str(b.imageWidthMM/1000.00) + "m" +\
                    "\nImg Height: " + str(b.imageHeightMM/1000.00) + "m" +\
                    "\nLift from floor: " + str(b.imageLiftmm/1000.00) + "m" +\
                    "\nHeight inc lift: " + str(b.imageHeightWithLiftMM/1000.00) + "m"
                    
                self.magicGoButton.disabled = False

    def goPrint(self):

        b.calculateImpliedParameters()
        
        # Assume bot is postitioned at Datum
        b.setBotCoordsToDatum()
        b.setMotorStepsToDatumPos(serialLink)
        
        # Start painting
        for y in range (b.imageYPixels):
            for x in range (b.imageXPixels):
                print str(x) + ", " + str(y) + ": " + str(b.getPixelCoordsInMM([x, y])) + " " + str(b.getPixelGreyValue([x, y], self.fileToPrintPath))
                b.printNewDot([x,y], self.fileToPrintPath, serialLink)
        
        # Return home to datum for collection
        b.goToDatum(serialLink)
                  

        
class SettingsSaveScreen(Screen):
        
    def setFilechooserPath(self, fileChooserPath):
        self.filechooser.path=str(fileChooserPath)
        
    def deleteAll(self):
        rmtree(settingsDir)
        os.makedirs(settingsDir)
        self.refreshFilechooser()

    def deleteSelected(self, filename):
        os.remove(filename[0])
        self.refreshFilechooser()
        
    def saveAs(self):
        fileName = str(self.fileNameTextEntry.text)
        b.settingsName = fileName
        filePath = settingsDir + fileName
        with open(filePath, 'wb') as output:
            pickle.dump(b, output)
        self.manager.current = 'botsetup'

    def open(self, filePath):
        global b
        with open(filePath[0], 'rb') as input:
            b = pickle.load(input)
        self.manager.current = 'botsetup'
        botSetScreen.refreshSetupLabels()

    def refreshFilechooser(self):
        self.filechooser._update_files()
        
            
class SettingsLoadScreen(Screen):
    pass

class LocalFileLoadScreen(Screen):
    
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    
    def setForSettingsSave(self):
        self.setFilechooserPath(settingsDir)
        self.usbButton.disabled = 'True'
    
    def load(self, path, filename):

        global fileToPrintPath
        fileToPrintPath = str(filename[0])
 
        # clear jobQ in Windows
        if sys.platform == "win32":
            for the_file in os.listdir(printQueueFolder):
                file_path = os.path.join(printQueueFolder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
        # clear jobQ in Linux
        if sys.platform != "win32":
            rmtree(printQueueFolder)
            os.makedirs(printQueueFolder)
            
        # move selected file to Q
        head, tail = ntpath.split(fileToPrintPath)
        shutil.copyfile(fileToPrintPath, printQueueFolder + tail)
     
        homeScreen.checkQ()
        self.quit()
        
    def quit(self):
        self.manager.current = 'home'
        self.manager.transition.direction = 'up'
        
    def deleteAll(self):
        global localFilePath
        print localFilePath
        rmtree(localFilePath)
        os.makedirs(localFilePath)

    def deleteSelected(self, filename):
        os.remove(filename[0])
        
    def refreshFilechooser(self):
        self.filechooser._update_files()
        
    def setFilechooserPath(self, fileChooserPath):
        self.filechooser.path=str(fileChooserPath)
        
    def checkUSB(self):
        
        if sys.platform != "win32":
            # is USB flash drive present?
            partitionsFile = open("/proc/partitions")
            lines = partitionsFile.readlines()[2:]#Skips the header lines
            for line in lines:
                words = [x.strip() for x in line.split()]
                minorNumber = int(words[1])
                deviceName = words[3]
                if minorNumber % 16 == 0:
                    path = "/sys/class/block/" + deviceName
                    if os.path.islink(path):
                        if os.path.realpath(path).find("/usb") > 0:
                            usbDataFile = "/dev/" + deviceName + "1" # the +1 forces sda1 instead of just 'sda', which works. HACK! Needs looking into why.
                            if os.path.isdir(usbPath) == False: 
                                os.system("echo posys | sudo -S mkdir " + usbPath) #TODO: VERY Insecure - requires script reference
                                os.system("echo posys | sudo -S chown -R sysop:sysop " + usbPath) #TODO: VERY Insecure - requires script reference
                            mountCommand = "echo posys | sudo -S mount " + usbDataFile + " " + usbPath + " -o uid=sysop,gid=sysop" #TODO: VERY Insecure - requires script reference
                            print mountCommand
                            os.system(mountCommand)
                            usbFileScreen.setFilechooserPath(usbPath)
                            self.manager.current = 'usb_file_load'
                            self.manager.transition.direction = 'down'
        else:
            usbFileScreen.setFilechooserPath(usbPath)
            self.manager.current = 'usb_file_load'
            self.manager.transition.direction = 'down'
       
class USBFileLoadScreen(Screen):

    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def importFile(self, filepath, filename):
        
        global localFilePath, localFileScreen
        dst = localFilePath + str(ntpath.basename(filename[0]))
        src = filename[0]
        copyfile(src, dst) # copy file is a method form shutil import
        localFileScreen.refreshFilechooser()
        self.quit()
        
    def quit(self):
        self.manager.current = 'local_file_load'
        self.manager.transition.direction = 'up'
        
    def setFilechooserPath(self, fileChooserPath):
        self.filechooser.path=str(fileChooserPath)

class DatumScreen(Screen):
    
    rotateSmallMM = 10
    rotateBigMM = 50
    
    def leftCCW(self): self.moveLeftMotor(-self.rotateSmallMM)
    def leftCW(self): self.moveLeftMotor(self.rotateSmallMM)
    def leftCCWplus(self): self.moveLeftMotor(-self.rotateBigMM)
    def leftCWplus(self): self.moveLeftMotor(self.rotateBigMM)
    def rightCCW(self): self.moveRightMotor(-self.rotateSmallMM)
    def rightCW(self): self.moveRightMotor(self.rotateSmallMM)
    def rightCCWplus(self): self.moveRightMotor(-self.rotateBigMM)
    def rightCWplus(self): self.moveRightMotor(self.rotateBigMM)

    def moveLeftMotor(self, increment):
        if sys.platform != "win32":
            b.moveLeftMotorMM(increment, serialLink)

    def moveRightMotor(self, increment):
        if sys.platform != "win32":
            b.moveRightMotorMM(increment, serialLink)

# Rubbish
class PrintCheckScreen(Screen):
    pass
class PrintSetScreen(Screen):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    dismiss_popup = ObjectProperty(None)
        
    def setFileStats(self):
        printFileFolderName = os.listdir(printQueueFolder)
        if not printFileFolderName:
            self.stats_button.text = "Queue empty"
        else:
            self.stats_button.text = printFileFolderName[0]
class PrintStatusScreen(Screen):
    pass
class GoScreen(Screen):
    pass    

########## Serial connection

serialLink = None
# serial link object to pass to bot. Must reside outside Bot() so bot instance can be pickled
if sys.platform != "win32": # if in linux only 
    filesForDevice = listdir('/dev/') # put all device files into list[]
    for line in filesForDevice: # run through all files
        if (line[:6] == 'ttyACM'): # look for prefix of known success
            devicePort = line # take whole line (includes suffix address e.g. ttyACM0
            serialLink = serial.Serial('/dev/' + str(devicePort), 9600) # assign
            print '>>>>>>>>>>>>>>>>>>>> Serial connection OK...'

# initialise objects
b = bot.Bot()

# initialise modules
botSetUpDialogue.init(b, serialLink)

# Create the screen manager
# sm = ScreenManager(transition=NoTransition())
sm = ScreenManager()

homeScreen = HomeScreen(name='home')
usbFileScreen = USBFileLoadScreen(name='usb_file_load')
localFileScreen = LocalFileLoadScreen(name='local_file_load')
printSetScreen = PrintSetScreen(name='print_set')
settingsLoadScreen = SettingsLoadScreen(name='settingsLoad')
settingsSaveScreen = SettingsSaveScreen(name='settingsSave')
botSetScreen = botSetUpDialogue.BotSetScreen(name='botsetup')

datumScreen = DatumScreen(name='datum')
sprayProfile = triggerProfile.SprayProfileScreen(name='sprayProfile')

sm.add_widget(BlankScreen(name='blank'))
sm.add_widget(SplashScreen(name='splash'))
sm.add_widget(homeScreen)
sm.add_widget(printSetScreen)
sm.add_widget(localFileScreen)
sm.add_widget(usbFileScreen)
sm.add_widget(PrintCheckScreen(name='print_check'))
sm.add_widget(PrintStatusScreen(name='print_status'))
sm.add_widget(datumScreen)
sm.add_widget(GoScreen(name='go'))
sm.add_widget(botSetScreen)
sm.add_widget(settingsLoadScreen)
sm.add_widget(settingsSaveScreen)
sm.add_widget(sprayProfile)

if serialLink:
    homeScreen.botStatsText = "Serial OK"

# file location settings
if sys.platform == "win32":
    localFilePath = 'C:/Users/Ed/Google Drive/My projects/DotBot/src/jobCache/' # Local place where print files are kept
    fileToPrintPath = '' # File to be printed
    printQueueFolder = 'C:/Users/Ed/Google Drive/My projects/DotBot/src/jobQ/'
    usbPath = 'D:/'
    settingsDir = 'C:/Users/Ed/Google Drive/My projects/DotBot/src/settings/'
else:
    localFilePath = '/home/sysop/dotbot/src/jobCache/' # Local place where print files are kept
    fileToPrintPath = '' # File to be printed
    printQueueFolder = '/home/sysop/dotbot/src/jobQ/'
    usbPath = '/media/usb/'
    settingsDir = '/home/sysop/dotbot/src/settings/'


defaultSettingsLocation = [1] 
defaultSettingsLocation[0] = str(settingsDir + "Default")
settingsSaveScreen.open(defaultSettingsLocation)
homeScreen.checkQ()

class TestApp(App):

    def build(self):

        printSetScreen.setFileStats()
        localFileScreen.setFilechooserPath(localFilePath)
        settingsSaveScreen.setFilechooserPath(settingsDir)
        
        b.calculateImpliedParameters()

        return sm

if __name__ == '__main__':
    TestApp().run()