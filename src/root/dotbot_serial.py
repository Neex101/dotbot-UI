'''
Created on 13 Jan 2018

@author: Ed
'''
import serial, sys, time, string
from os import listdir
from kivy.clock import Clock

ENABLE_STATUS_REPORTS = True
STATUS_INTERVAL = 1 # seconds
DEBUG_SND = False
DEBUG_REC = False
BAUD_RATE = 9600
SQRL_SCANNER_MIN_DELAY = 0.05 # Delay between checking for response from sqrl. Needs to be hi-freq for quick streaming, e.g. 0.01


class DotBotSerial(object):

    s = None # serial object - can't be pickled.
    serial_address = ''

        
    def initialise_objects(self, botSetScreen, spraySetScreen, wallSetScreen, imageSetScreen):
        self.bot = botSetScreen
        self.spray = spraySetScreen
        self.wall = wallSetScreen
        self.image = imageSetScreen
    
    def connect(self, win_port):

        # Parameter 'win'port' only used for windows dev e.g. "COM4"
        if sys.platform == "win32": 
            try:
                self.s = serial.Serial(win_port, BAUD_RATE) 
                self.initialise_arduino()
                return True  
            except:
                return False
        else:
            try: 
                filesForDevice = listdir('/dev/') # put all device files into list[]
                for line in filesForDevice: # run through all files
                    if (line[:6] == 'ttyUSB' or line[:6] == 'ttyACM'): # look for prefix of known success (covers both Mega and Uno)
                        devicePort = line # take whole line (includes suffix address e.g. ttyACM0
                        self.s = serial.Serial('/dev/' + str(devicePort), BAUD_RATE) # assign
                        self.initialise_arduino()
                        return True
            except:
                return False

   
    def is_connected(self):
        
        if self.s: return True 
        else: return False
    
    def initialise_arduino(self):
        if self.is_connected():
            self.write_command("\r\n\r\n", show_in_sys=False, show_in_console=False)    # Wakes sqrl
            Clock.schedule_once(self.start_services, 2) # Delay for sqrl to initialize 
        
    def start_services(self, dt):

        self.s.flushInput()  # Flush startup text in serial input
        Clock.schedule_once(self.sqrl_scanner, 0)   # Listen for messages from sqrl
        self.set_servo_angle(150) # Make sure the can isn't being sprayed on all the time!
        if ENABLE_STATUS_REPORTS:
            Clock.schedule_interval(self.poll_status, STATUS_INTERVAL)      # Poll for status


    def poll_status(self, dt):
        
        self.write_command('?', show_in_sys=False, show_in_console=False)

######## READ

    VERBOSE_ALL_PUSH_MESSAGES = False         # Push is for messages (e.g. status)
    VERBOSE_ALL_RESPONSE = False     # Response is for stream counting (sending g-code file)
    VERBOSE_STATUS = False

    def sqrl_scanner(self, dt):


        # If there's a message received, deal with depending on type
        if self.s.inWaiting():

            rec_temp = self.s.readline().strip() # Usually blocking, hence need for .inWaiting()
            
            # Update the gcode monitor (may not be initialised) and console
            try:
                self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('rec', rec_temp)
            except:
                pass
            if self.VERBOSE_ALL_RESPONSE: print rec_temp
            
            # If RESPONSE message (used in streaming, counting processed gcode lines)
            if rec_temp.startswith(('#', 'error')):                
                self.process_sqrl_response(rec_temp)
            
            # If PUSH message
            else:   
                self.process_sqrl_push(rec_temp)
            
                
        Clock.schedule_once(self.sqrl_scanner, SQRL_SCANNER_MIN_DELAY)   # Loop this method



    def process_sqrl_response(self, message):
        
        # This is a special condition, used only at startup to set EEPROM settings
        pass
 
    def process_sqrl_push(self, message):
        
        if self.VERBOSE_ALL_PUSH_MESSAGES: print message
        
        # If it's a status message, e.g. <Idle|MPos:-1218.001,-2438.002,-2.000|Bf:35,255|FS:0,0>
        if message.startswith('<'): 
            status_parts = message.translate(string.maketrans("", "", ), '<>').split('|') # fastest strip method
            
            # Get machine's status
            self.m_state = status_parts[0]
            for part in status_parts:
                
                # Get machine's position (may not be displayed, depending on mask)
                if part.startswith('MPos:'): 
                    pos = part[5:].split(',')
                    self.m_x = pos[0]
                    self.m_y = pos[1]
                


######## WRITE  
    
    def write_command(self, serialCommand, show_in_sys=False, show_in_console=False):  
        
        # INLCUDES end of line command (which returns an 'ok' from grbl - used in algorithms)
        if self.s: 
            try:
                self.s.write(serialCommand + '\n')
            except:
                print "Failed to write_command: " + serialCommand
            
            try:
                if show_in_sys:
                    print serialCommand          
                if show_in_console:                
                    self.sm.get_screen('home').gcode_monitor_widget.update_monitor_text_buffer('snd', serialCommand)
            except:
                print "Written to serial, but failed to display: " + serialCommand            
    


############# Commands

    def jog(self, dir, mm):
        steps = str(mm * 3600)
        if dir == 'L': self.write_command('BM L' + steps + ' R' + steps)
        elif dir == 'R': self.write_command('BM L-' + steps + ' R-' + steps)
        elif dir == 'Up': self.write_command('BM L' + steps + ' R-' + steps)
        elif dir == 'Dn': self.write_commande('BM L-' + steps + ' R' + steps)
        
    def stop(self):
        # Sets a new target position that causes the stepper to stop as quickly as possible, using the current speed and acceleration parameters.
        self.write_command('STOPXY')
    
    servo_pos = 0
    
#     def increment_servo(self, angle):
#         self.servo_pos += angle
#         if self.servo_pos < 0: self.servo_pos = 0
#         self.write_command('SS ' + str(self.servo_pos), show_in_sys=True)

    def set_servo_angle(self, angle):
        if self.servo_pos < 0: self.servo_pos = 0
        self.write_command('SS ' + str(angle), show_in_sys=True, show_in_console=False)
    
    def bounce_servo(self, start_angle, total_millis, end_angle):
#     BS A150 D500 R30
        if start_angle > 0 and total_millis > 0 and end_angle > 0:
            self.write_command('BS A' + str(start_angle) + ' D' + str(total_millis) + ' B' + str(end_angle), show_in_sys=True)