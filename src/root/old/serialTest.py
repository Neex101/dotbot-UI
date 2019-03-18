'''
Created on 29 Oct 2017

@author: Ed
'''

import sys, os
if sys.platform != "win32": import serial  # @UnresolvedImport
from os import listdir
print "Hello"
import time

# serial link object to pass to bot. Must reside outside Bot() so bot instance can be pickled
if sys.platform != "win32": # if in linux only 
    filesForDevice = listdir('/dev/') # put all device files into list[]
    for line in filesForDevice: # run through all files
        if (line[:6] == 'ttyACM'): # look for prefix of known success
            devicePort = line # take whole line (includes suffix address e.g. ttyACM0
            serialLink = serial.Serial('/dev/' + str(devicePort), 9600) # assign
            print '>>>>>>>>>>>>>>>>>>>> Serial connection OK...'
            time.sleep(1000)
            serialLink.write("L1234R4576A180D2000B0X")
            print 'datasent'