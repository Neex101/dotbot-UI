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
from kivy.graphics.context_instructions import Color  # @UnresolvedImport
from kivy.graphics.opengl import *
from kivy.graphics import *


Builder.load_string("""

#:import os os

<RipSetScreen>:

    fileSelectedLabel:fileSelectedLabel
    fileNameTextInput:fileNameTextInput
    filechooser:filechooser
    deleteButton:deleteButton
    loadButton:loadButton
    simulateButton:simulateButton
    gCodePreview:gCodePreview
    optimisationLabel:optimisationLabel

    Accordion:
        orientation: 'horizontal'

        AccordionItem:
            title: 'Profile: ' + root.profile_name
            collapse: False

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
                            size_hint_y: 2  
        
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
                            size_hint_y: 8  
                                        
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
                            filters: ['*.rip']
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

        AccordionItem:
            title: 'Generate'
            collapse: False
            
            BoxLayout:
                padding: 5
                spacing: 5
                orientation: "horizontal"

                BoxLayout:
                    size_hint_x:2
                    padding: 5
                    spacing: 5
                    orientation: "vertical"
                    Button:
                        size_hint_y: 2
                        text: 'Process array'
                        on_release: root.createRipArray()
                    Button:
                        id: simulateButton
                        size_hint_y: 2
                        text: 'Simulate'
                        disabled: True
                        on_release: root.simulateDots()
                    Slider:
                        id: zSlider
                        size_hint_y: 8
                        min:0
                        max:1
                        step:0.01
                        value: root.minGreyValue
                        orientation: 'vertical'
                        sensitivity: 'handle'
                        on_value: root.minGreyValue = self.value
                    Label:
                        size_hint_y: 1
                        id: optimisationLabel
                        text: 'Optimisation'
                    
                
                Scatter:
                    index: 9999
                    auto_bring_to_front: False
                    size_hint_x:8
                    size: self.parent.size
#                     canvas.after:
#                         Color:
#                             rgba: 1,0,0,.5
#                         Rectangle:
#                             size:self.size
#                             pos:self.pos
                    do_rotation: False
                    do_scale: True
                    Label:
#                         canvas.before:
#                             PushMatrix
#                             Rotate:
#                                 angle: 180
#                                 origin: self.parent.size[0]/2, self.parent.size[1]/2
#                         canvas.after:
#                             PopMatrix
                        size: self.parent.size
                        id: gCodePreview


""")


lastSavedFilePath = 'settings/lastUsed/' + 'rip_lastUsed'
settingsDir = 'settings/'
        
class RipSetScreen(Screen):

    profile_name = StringProperty("Default")
    minGreyValue = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super(RipSetScreen, self).__init__(**kwargs)
        if os.path.isfile(lastSavedFilePath): self.loadLastProfileSaved()
        
        self.bot=kwargs['bot']
        self.spray=kwargs['spray']
        self.wall=kwargs['wall']
        self.image=kwargs['image']
        
    def save(self):
        parametersList = [self.profile_name, self.minGreyValue]
        # save to settings folder       
        with open(settingsDir + self.profile_name + '.rip', 'wb') as output:
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
            self.minGreyValue = p[1]

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
        
    def createRipArray(self):
        
        self.ripArray = [] # x_pos_mm, y_pos_mm, greyValue, zValue, tValue
        self.ripBounds = [] # rip_x_min_mm, rip_y_min_mm, rip_x_max_mm, rip_y_max_mm

        img_width_pixels = self.image.imageXPixels
        img_height_pixels = self.image.imageYPixels
        img_width_mm = img_width_pixels * self.wall.pixel_diameter
        img_height_mm = img_height_pixels * self.wall.pixel_diameter
        wall_width_mm = self.wall.wall_width_mm
        img_lift_mm = self.wall.image_lift_mm
        
        # imgBounds
        x_min_mm = wall_width_mm/2 - img_width_mm/2
        y_min_mm = self.wall.image_lift_mm
        x_max_mm = x_min_mm + img_width_mm
        y_max_mm = y_min_mm + img_height_mm
        
        x_values = []
        y_values = []
        
        # ripArray
        for y in range (img_height_pixels):
            for x in range (img_width_pixels):
                x_pos_mm = x_min_mm + self.getPixelCoordsInMM([x, img_height_pixels-y-1])[0] 
                y_pos_mm = y_min_mm + self.getPixelCoordsInMM([x, img_height_pixels-y-1])[1]
                greyValue = self.getPixelGreyValue([x, y])
                zValue = None
                tValue = None
                if greyValue >= self.minGreyValue:
                    self.ripArray.append([x_pos_mm, y_pos_mm, greyValue, zValue, tValue])
                    x_values.append(x_pos_mm)
                    y_values.append(y_pos_mm)
        
        # ripBounds            
        self.ripBounds = [min(x_values), min(y_values), max(x_values), max(y_values)]
         
        # res info                    
        max_res = img_width_pixels * img_height_pixels
        optimised_res = len(self.ripArray)
        self.optimisationLabel.text = str(optimised_res) + ' / ' + str(max_res)
        self.simulateButton.disabled = False
        
        


    def simulateDots(self):
                
        self.gCodePreview.canvas.clear()
         
        scale_x = self.gCodePreview.size[0]/(self.wall.wall_width_mm * 1.0)
        scale_y = self.gCodePreview.size[1]/(self.wall.wall_height_mm * 1.0)
        scale = min(scale_x,scale_y)

        with self.gCodePreview.canvas:

            Scale(scale,scale,1)

            # wall
            Color(1,1,1,.1)
            Rectangle(pos=(0, 0), size=(self.wall.wall_width_mm, 
                                          self.wall.wall_height_mm))

            # dots
            Color(0,1,0,1)
            max_dot_rad = self.spray.max_dot_dia_mm / 2
            max_dot_area = math.pi * (max_dot_rad ** 2)
            
            for n in range (len(self.ripArray)):
                x_center = self.ripArray[n][0]
                y_center = self.ripArray[n][1]
                dia = math.sqrt((self.ripArray[n][2] * max_dot_area)/math.pi) * 2
                Ellipse(pos=(x_center-dia/2,y_center-dia/2), size = (dia,dia))

            # bounds
            Color(0,0,1,1)
            Line(points=[self.ripBounds[0], self.ripBounds[1],
                         self.ripBounds[0], self.ripBounds[3],
                         self.ripBounds[2], self.ripBounds[3],
                         self.ripBounds[2], self.ripBounds[1]], width=2, close=True)

        
    def getPixelCoordsInMM(self, xy_pixels):    #See docs for definition of datum (bottom left)
        x_pixel = xy_pixels[0]
        y_pixel = xy_pixels[1] 
        x_coordMM = self.wall.pixel_diameter/2 + x_pixel*self.wall.pixel_diameter
        y_coordMM = self.wall.pixel_diameter/2 + y_pixel*self.wall.pixel_diameter
        return [x_coordMM, y_coordMM]
        
    def getPixelGreyValue(self, xy_pixels):
        image = CoreImage(self.image.source_image_path, keep_data = True)
        rgb = image.read_pixel(xy_pixels[0], xy_pixels[1])
        return (rgb[0]+rgb[1]+rgb[2])/3 #averaging method (see for more options: https://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/)

        

