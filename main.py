from psuedoSensor import PseudoSensor
from week1python import Ui_MainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from time import sleep
import datetime
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

#Main.py Project 2 file for temp and humidity sensors w/ HTML UI
#by Abdul Rahman Alsherazi Alsabbagh, CU Boulder MSEE

# handler for the websocket
class WSHandler(tornado.websocket.WebSocketHandler):
    #prints text when a connection is made
    def open(self):
        print("Websocket Open")

    # this function handles received messages
    # if a 'Read1Value" message is received from the client, it will read data from the sensor, store it in the list, and send it
    # if a 'Read10Values' message is received, it will read 10 values, store them in the list, and send the latest reading
    # if a 'Calculate' message is received, it will calculate min, max and averages for both temperature and humidity and send these stats to the client
    # if a 'TAlarm' message is received, it will compare it against the maximum temp value and tell the client whether there is an alarm
    # if a 'HAlarm" message is received, it will do same as above but for humidity
    # if a different message is received, it will tell the client that the message is not recognized
    def on_message(self, message):
        print ('message received')
        print (message)
        if message == 'Read1Value':
            print ('Read 1 value message received')
            Read1Value()
            self.write_message('Last Temperature Reading: ' + str(TData[-1]))
            self.write_message('Last Humidity Reading: ' + str(HData[-1]))
            print ('1 value read and sent')
        
        elif message == 'Read10Values':
            print ('Read 10 values message received')
            Read10Values()
            self.write_message('Last Temperature Reading: ' + str(TData[-1]))
            self.write_message('Last Humidity Reading: ' + str(HData[-1]))
            print ('10 values read, last value sent')
        
        elif message == 'Calculate':
            print ('Calculate min, max and average message received')
            self.write_message('Min Temperautre: ' + str(min(TData[-10:-1])))
            self.write_message('Max Temperature: ' + str(max(TData[-10:-1])))
            self.write_message('Average Tempreature: ' + str(sum(TData[-10:-1])/len(TData[-10:-1])))
            self.write_message('Min Humidity: ' + str(min(HData[-10:-1])))
            self.write_message('Max Humidity: ' + str(max(HData[-10:-1])))
            self.write_message('Average Humidity: ' + str(sum(HData[-10:-1])/len(HData[-10:-1])))
            print ('min, max, and averages of 10 last values sent')
            
        elif message[0:6] == 'TAlarm':
            if float(message[6:]) < max(TData):
                self.write_message('TEMPERATURE ALARM!')
            else:
                 self.write_message('No Temperature Alarm')
                 
        elif message[0:6] == 'HAlarm':
            if float(message[6:]) < max(HData):
                self.write_message('HUMIDITY ALARM!')
            else: 
                self.write_message('No Humidity Alarm')
        
        else: 
            self.write_message('Request not recognized')
            
    # the program quits once a connection is closed    
    def on_close(self):
        print 'connection closed'
        quit()
    
    def check_origin(self,origin):
        return True
        
#Read 1 button and reads 1 set of humidity and temperature values
#Reads data from sensor and then appends values to TData (Temp) and HData (Humidity) lists
def Read1Value():
    h,t = ps.generate_values()
    TData.append(t)
    HData.append(h)
    TimeDateData.append(datetime.datetime.now())
  


#reads 10 sets of temperature and humidity values with 1 second delay between every reading
#Calls Read1Value 10 times
def Read10Values():
    i=0
    while i<10:
        Read1Value()
        sleep(1)
        i=i+1
    
    
#setup of sensor data using PseudoSensor class
ps = PseudoSensor()

#Lists where data read from sensors will be stored
TData = []
HData = []

#where time stamps are stored with every reading
TimeDateData = []
 
#initilization of the websocket server
application = tornado.web.Application([(r'/ws', WSHandler),])
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(8888)
myIP = socket.gethostbyname(socket.gethostname())
print '*** Websocket Server Started at %s***' % myIP
tornado.ioloop.IOLoop.instance().start()    

sys.exit(app.exec_())


