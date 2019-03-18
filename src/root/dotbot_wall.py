'''
Created on 28 Aug 2017
@author: Ed
'''


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

<WallSetScreen>:

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
                        text: root.profile_name
                        on_text: root.profile_name=self.text
           
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
                        text: 'Wall X:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24
                        input_filter: 'int'
                        multiline: False
                        text: str(root.wall_width_mm)
                        on_text: root.wall_width_mm=self.text
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
                        text: 'Wall Y:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24  
                        input_filter: 'int'
                        multiline: False
                        text: str(root.wall_height_mm)
                        on_text: root.wall_height_mm=self.text
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
                        text: 'Image lift:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24  
                        input_filter: 'int'
                        multiline: False
                        text: str(root.image_lift_mm)
                        on_text: root.image_lift_mm=self.text
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
                        text: 'Pixel diameter:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24
                        input_filter: 'float'
                        multiline: False
                        text: str(root.pixel_diameter)
                        on_text: root.pixel_diameter=self.text
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
                        text: 'Datum height:'
                    TextInput:
                        size_hint_x: 2
                        font_size:24
                        input_filter: 'float'
                        multiline: False
                        text: str(root.datum_height)
                        on_text: root.datum_height=self.text
                    Label:
                        size_hint_x: 1  
                        text: 'mm'
                                                                
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
                    filters: ['*.wall']
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

""")


lastSavedFilePath = 'settings/lastUsed/' + 'wall_lastUsed'
settingsDir = 'settings/'
        
class WallSetScreen(Screen):

    profile_name = StringProperty("Default")
    wall_width_mm = NumericProperty(10000)
    wall_height_mm = NumericProperty(10000)
    image_lift_mm = NumericProperty(1000)
    pixel_diameter = NumericProperty(85)
    datum_height = NumericProperty(1500)

    def __init__(self, **kwargs):
        super(WallSetScreen, self).__init__(**kwargs)
        if os.path.isfile(lastSavedFilePath): self.loadLastProfileSaved()
        
    def save(self):
        parametersList = [self.profile_name, self.wall_width_mm, self.wall_height_mm, 
                          self.image_lift_mm, self.pixel_diameter, self.datum_height]
        # save to settings folder       
        with open(settingsDir + self.profile_name + '.wall', 'wb') as output:
            pickle.dump(parametersList, output, pickle.HIGHEST_PROTOCOL)
        # save over last saved copy
        with open(lastSavedFilePath, 'wb') as output:
            pickle.dump(parametersList, output, pickle.HIGHEST_PROTOCOL)        
        self.refreshFilechooser()

    def load(self, filePath):
        if os.path.isfile(filePath):
            with open(filePath, 'rb') as input:
                p = pickle.load(input)
            self.profile_name = p[0]
            self.wall_width_mm = p[1]
            self.wall_height_mm = p[2]
            self.image_lift_mm = p[3]
            self.pixel_diameter = p[4]
            self.datum_height = p[5]

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


