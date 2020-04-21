#!/usr/bin/env python3
from tkinter import *
from yeelight import Bulb
bulb = Bulb("YOUR.IP.HERE", effect="smooth", duration=750, auto_on=True) # Set IP, find in router or phone app. Keep the quotes!
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
yeetlight = Tk()
yeetlight.title('Yeetlight v0.1')
topFrame = Frame(yeetlight)
topFrame.pack()
buttonOff = Button(topFrame, text="Off", bg="black", fg="red", command=turnoff)
buttonOn = Button(topFrame, text="On", bg="black", fg="green", command=turnon)
buttonNightmode = Button(topFrame, text="Night mode", bg="black", fg="blue", command=night)
buttonDaylight = Button(topFrame, text="Daylight bright", bg="black", fg="gold", command=day)
buttonOn.pack(side=LEFT)
buttonOff.pack(side=LEFT)
buttonDaylight.pack(side=LEFT)
buttonNightmode.pack(side=LEFT)
yeetlight.call('wm', 'attributes', '.', '-topmost', '1') # Force on top of other windows, delete if you wish
yeetlight.mainloop()

