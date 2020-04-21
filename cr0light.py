#!/usr/bin/env python3
from tkinter import *
from yeelight import Bulb
bulb = Bulb("192.168.1.87", effect="smooth", duration=750, auto_on=True)
bulb.turn_on()
def turnoff():
    bulb.turn_off()
def turnon():
    bulb.turn_on()
def day():
    bulb.set_brightness(100)
    bulb.set_color_temp(4700)
    bulb.set_default()
def night():
    bulb.set_brightness(5)
    bulb.set_color_temp(2700)
    bulb.set_default()
yeelight = Tk()
yeelight.title('cr0light 0.01')
topFrame = Frame(yeelight)
topFrame.pack()
buttonOff = Button(topFrame, text="Off", bg="black", fg="red", command=turnoff)
buttonOn = Button(topFrame, text="On", bg="black", fg="green", command=turnon)
buttonNightmode = Button(topFrame, text="Night mode", bg="black", fg="blue", command=night)
buttonDaylight = Button(topFrame, text="Daylight bright", bg="black", fg="gold", command=day)
buttonOn.pack(side=LEFT)
buttonOff.pack(side=LEFT)
buttonDaylight.pack(side=LEFT)
buttonNightmode.pack(side=LEFT)
yeelight.call('wm', 'attributes', '.', '-topmost', '1')
yeelight.mainloop()

