#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from control import *

class mainControlHandler:
    def __init__(self, builder, controller):
        self.builder = builder
        self.controller = controller
        self.adjustment1 = Gtk.Builder.get_object(self.builder, "adjustment1")
        self.adjustment2 = Gtk.Builder.get_object(self.builder, "adjustment2")
        self.switch1 = Gtk.Builder.get_object(self.builder, "switch1")
        self.switch2 = Gtk.Builder.get_object(self.builder, "switch2")
        self.spinbutton1 = Gtk.Builder.get_object(self.builder, "spinbutton1")
        self.spinbutton2 = Gtk.Builder.get_object(self.builder, "spinbutton2")
        Gtk.Adjustment.set_value(self.adjustment1, 0)
        Gtk.Adjustment.set_value(self.adjustment2, 0)
        self.trainSpeed = [ 0, 0]
        self.trainReverse = [ False, False]

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onSpinButtonChanged(self, button):
        spinnerID = Gtk.Buildable.get_name(button)
        spinnerValue = Gtk.SpinButton.get_value_as_int(button)
        print('Spinner with ID', spinnerID, 'has value', spinnerValue)
        self.makeTrainCommand()

    def onSwitchButtonChanged(self, button, gparam):
        switchID = Gtk.Buildable.get_name(button)
        switchState = Gtk.Switch.get_active(button)
        if switchState is True:
            print('Switch with ID', switchID, 'is enabled')
        else:
            print('Switch with ID', switchID, 'is disabled')
        self.makeTrainCommand()

    def onStopButtonPressed(self, button):
        buttonID = Gtk.Buildable.get_name(button)
        print('Button with ID', buttonID, 'pressed')
        if buttonID == "button1":
            adjustmentObject = self.adjustment1
        elif buttonID == "button2":
            adjustmentObject = self.adjustment2
        else:
            return
        Gtk.Adjustment.set_value(adjustmentObject, 0)
        self.makeTrainCommand()

    def makeTrainCommand(self, *args):
        self.trainSpeed[0] = Gtk.SpinButton.get_value(self.spinbutton1)
        self.trainSpeed[1] = Gtk.SpinButton.get_value(self.spinbutton2)
        self.trainReverse[0] = Gtk.Switch.get_active(self.switch1)
        self.trainReverse[1] = Gtk.Switch.get_active(self.switch2)
        command = 'T1:%d,%d|T2:%d,%d\n' % (self.trainSpeed[0], int(self.trainReverse[0]), self.trainSpeed[1], int(self.trainReverse[1]))
        print('Commmand:', command)
        self.controller.sendCommand(command)
        print('Reponse:', self.controller.getResponse())
        return command

def main():
    controller = arduinoControl("/dev/ttyACM0", 9600)
    controller.connect()
    builder = Gtk.Builder()
    builder.add_from_file("spin_buttons.glade")
    signalHandler = mainControlHandler(builder, controller)
    builder.connect_signals(signalHandler)

    window = builder.get_object("window1")
    window.show_all()

    Gtk.main()

if __name__ == '__main__': main()
