# -*- coding: utf-8 -*-
import serial

class arduinoControl:

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
    def connect(self):
        self.serialInterface = serial.Serial(self.port, self.baudrate)
    def sendCommand(self, command):
        self.command = command.encode("ascii", "replace") # Remove unicode characters
        try:
            self.serialInterface.write(self.command)
        except AttributeError:
            print('Error: connection has not been initialised.')
    def getResponse(self):
        try:
            return self.serialInterface.readline()
        except AttributeError:
            print('Error: connection has not been initialised.')

def test_func():
    control1 = arduinoControl("/dev/ttyACM0", 9600)
    control1.connect()
    control1.sendCommand('Buddy')

if __name__ == '__main__': test_func()