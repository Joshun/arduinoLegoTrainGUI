# -*- coding: utf-8 -*-

from gi.repository import Gtk
import time

class widgetSet:

    def __init__(self, builder):
        self.builder = builder
        self.widgets = {}

    def addWidget(self, wname):
        self.widgets[wname] = Gtk.Builder.get_object(self.builder, wname)

    def getWidget(self, wname):
        return self.widgets[wname]

class timeStructure:

    def __init__(self, etime, ttime, command):
        self.etime = etime
        self.ttime = ttime
        self.command = command

class timeSet:

    def __init__(self):
       self.times = []

    def addElement(self, timeTuple, command): # Must pass a tuple
        print('Added:', timeTuple)
        print('Time:', time.asctime(timeTuple))
        etime = time.mktime(timeTuple)
        self.times.append(timeStructure(etime, timeTuple, command))
    def printTimes(self):
        for element in self.times:
            print('Tuple:', element.ttime, 'Epoch:', element.etime, 'Command:', element.command)
    def sortTimes(self):
        sorted(self.times, key=lambda element: element.etime)
    def waitTimes(self):
        previousItem = self.times[0]
        num = 0
        for item in self.times:
            if num == 0:
                print('Need to sleep for:', item.etime)
            else:
                print('Need to sleep for:', item.etime - previousItem.etime)
            num += 1
            previousItem = item

class scheduler:

    def __init__(self):
        self.builder = Gtk.Builder.new_from_file("scheduler.glade")
        self.builder.connect_signals(self)
        self.widgets = widgetSet(self.builder)
        self.widgets.addWidget('mainWindow')
        self.widgets.addWidget('invalidDateDialog')
        self.widgets.addWidget('dateEntry')
        self.widgets.addWidget('commandEntry')
        self.widgets.addWidget('hourAdjustment')
        self.widgets.addWidget('minuteAdjustment')
        self.widgets.addWidget('secondAdjustment')

        currentTime = time.localtime(time.time())
        dateEntry = self.widgets.getWidget('dateEntry')
        hourEntry = self.widgets.getWidget('hourAdjustment')
        minuteEntry = self.widgets.getWidget('minuteAdjustment')
        secondEntry = self.widgets.getWidget('secondAdjustment')
        commandEntry = self.widgets.getWidget('commandEntry')
        Gtk.Calendar.select_month(dateEntry, (currentTime[1] - 1), currentTime[0])
        Gtk.Calendar.select_day(dateEntry, currentTime[2])
        Gtk.Adjustment.set_value(hourEntry, currentTime[3])
        Gtk.Adjustment.set_value(minuteEntry, currentTime[4])
        Gtk.Adjustment.set_value(secondEntry, currentTime[5])
        Gtk.Entry.set_text(commandEntry, 'T1:0,0|T2:0,0')

        Gtk.SpinButton

        self.schedule = timeSet()

    def onWindowClosed(self, *args):
        print('\"delete\" event received')
        Gtk.main_quit(*args)
    def onHourChanged(self, button):
        pass
    def onMinuteChanged(self, button):
        pass
    def onSecondChanged(self, button):
        pass
    def onCalendarChanged(self, button):
        print('Day selected')
        calendar = self.widgets.getWidget('dateEntry')
        year, month, day = Gtk.Calendar.get_date(calendar)
        print('Date: {}/{}/{}'.format(day, month, year))
        pass
    def onAddtaskClicked(self, button):
        print('\"Add Task\" clicked')
        hourAdjustment = self.widgets.getWidget('hourAdjustment')
        minuteAdjustment = self.widgets.getWidget('minuteAdjustment')
        secondAdjustment = self.widgets.getWidget('secondAdjustment')
        calendar = self.widgets.getWidget('dateEntry')
        commandEntry = self.widgets.getWidget('commandEntry')

        hour = int(Gtk.Adjustment.get_value(hourAdjustment))
        minute = int(Gtk.Adjustment.get_value(minuteAdjustment))
        second = int(Gtk.Adjustment.get_value(secondAdjustment))
        year, month, day = Gtk.Calendar.get_date(calendar)
        command = Gtk.Entry.get_text(commandEntry)

        month += 1 # Stupid GTK Calendar does months differently
        dateStr = "{}/{}/{}".format(day, month, year)
       # print('Date entered:', dateStr)
        struct_time = time.strptime(dateStr, "%d/%m/%Y")
        #print('Format:', struct_time)
        editable_struct_time = list(struct_time)
        editable_struct_time[3] = hour
        editable_struct_time[4] = minute
        editable_struct_time[5] = second
        finalised_struct_time = tuple(editable_struct_time)
        #print('Future time:', hour, minute, second)
        self.schedule.addElement(finalised_struct_time, command)
        self.checkTime(finalised_struct_time)
        self.schedule.sortTimes()
        self.schedule.printTimes()
        self.schedule.waitTimes()

    def checkTime(self, struct_time):
        currentTime = time.time()
        futureTime = time.mktime(struct_time)
        if futureTime - currentTime < 0:
            Gtk.Window.show_all(self.widgets.getWidget('invalidDateDialog'))
    def hideInvalidDateWindow(self, button):
        Gtk.Window.hide(self.widgets.getWidget('invalidDateDialog'))

def main():
    schedule = scheduler()
    mainWindow = schedule.widgets.getWidget('mainWindow')
    Gtk.Window.show_all(mainWindow)
    Gtk.main()

if __name__ == '__main__': main()
