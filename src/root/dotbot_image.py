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
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Line)
from kivy.graphics.context_instructions import Color  # @UnresolvedImport
# import kivy.graphics.Scale
from kivy.graphics.opengl import *
from kivy.graphics import *

Builder.load_string("""

#:import os os

<ImageSetScreen>:

    fileSelectedLabel:fileSelectedLabel
    filechooser:filechooser
    deleteButton:deleteButton
    loadButton:loadButton
    importButton:importButton
    saveButton:saveButton
    imageDescriptionLabel:imageDescriptionLabel

    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0

        BoxLayout:
            size_hint_y:9
            padding: 5
            spacing: 5
            orientation: 'horizontal'

            BoxLayout:
                size_hint_x: 1
                padding: 5
                spacing: 5
                orientation: 'vertical'
    
                Image:
                    size_hint_y:8
                    source: root.source_image_path
                    allow_stretch: True
                    keep_ratio: True
                    size: self.parent.size
                    pos: self.parent.pos
                Label:
                    size_hint_y:1
                    id: imageDescriptionLabel
                
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
                    filters: ['*.jpg','*.jpeg','*.JPG','*.JPEG','*.png','*.PNG']
                    rootpath: 'sourceImages/'
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
                text: 'Quit'
                on_release:
#                     root.loadLastProfileSaved()
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'home'                          
            Button:
                text: 'Save'
                id: saveButton
                disabled: True
                on_release: 
                    root.save_imgset_for_lastUsed()
#                     root.manager.transition.direction = 'right'
#                     root.manager.current = 'home'                          
            Button:
                id:importButton
                text: 'Import'
                disabled: True
                on_release: 
            Button:
                id:loadButton
                text: 'Load'
                disabled: True
                on_release: 
                    root.loadFromImageNameSelection(filechooser.selection[0])
            Button:
                id: deleteButton
                text: 'Delete'
                disabled: True
                on_release:
                    root.deleteSelected(filechooser.selection[0])


""")


lastSavedFilePath = 'sourceImages/lastUsed/' + 'image_lastUsed'
settingsDir = 'sourceImages/'
logoPath = 'dotbot_logo.png'
        
class ImageSetScreen(Screen):

    profile_name = StringProperty('No image loaded')
    source_image_path = StringProperty(logoPath)
    imageXPixels = 50
    imageYPixels = 50
    
    def on_enter(self):
        self.refreshFilechooser()

    def on_source_image_path(self, *args):
        if self.source_image_path != logoPath: 
            self.saveButton.disabled = False
            
    def refresh_image_description_label(self):
        self.imageDescriptionLabel.text = self.profile_name + ' (X:' + str(self.imageXPixels) + ' Y:' + str(self.imageYPixels) + ')'

    
    def __init__(self, **kwargs):
        super(ImageSetScreen, self).__init__(**kwargs)
        if os.path.isfile(lastSavedFilePath): self.loadLastProfileSaved()
        
    def loadFromImageNameSelection(self, image_filePath):
        if os.path.isfile(image_filePath):
            self.profile_name = os.path.basename(image_filePath).split('.')[0]
            self.source_image_path = image_filePath
            image = CoreImage(image_filePath, keep_data = True)
            self.imageXPixels = image.width
            self.imageYPixels = image.height
            
            parametersList = [self.profile_name, self.source_image_path, 
                              self.imageXPixels, self.imageYPixels]        # save to settings folder       
            with open(settingsDir + self.profile_name + '.imgset', 'wb') as output:
                pickle.dump(parametersList, output, pickle.HIGHEST_PROTOCOL)
            self.refresh_image_description_label()
        
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
        
    def save_imgset_for_lastUsed(self):
        parametersList = [self.profile_name, self.source_image_path, 
                          self.imageXPixels, self.imageYPixels]        
        # save over last saved copy
        with open(lastSavedFilePath, 'wb') as output:
            pickle.dump(parametersList, output, pickle.HIGHEST_PROTOCOL)        
        self.refreshFilechooser()

    def loadLastProfileSaved(self):
        if os.path.isfile(lastSavedFilePath):
            with open(lastSavedFilePath, 'rb') as input:
                p = pickle.load(input)
            imageLocation = p[1]
            if os.path.isfile(imageLocation):
                self.profile_name = p[0]
                self.source_image_path = p[1]
                self.imageXPixels = p[2]
                self.imageYPixels = p[3]
                self.refresh_image_description_label()

                

