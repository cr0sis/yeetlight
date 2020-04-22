#!/usr/bin/env python3
from tkinter import *
from yeelight import Bulb

class YeetBulb:
    def __init__(self, ip):
        self.ip = ip
        self.bulb = Bulb(self.ip, effect="smooth", duration=750, auto_on=True)

    def turnoff(self):
        self.bulb.turn_off()

    def turnon(self):
        self.bulb.turn_on()

    def day(self):
        self.bulb.set_brightness(100)
        self.bulb.set_color_temp(4700)
        self.bulb.set_default()

    def night(self):
        self.bulb.set_brightness(5)
        self.bulb.set_color_temp(2700)
        self.bulb.set_default()
#   def pink(self):
#       self.bulb.set_rgb(255,192,203)



bulb = YeetBulb('YOUR.IP.HERE') # See Readme on how to find IP
bulb.turnon() # Turn on to last known default when we start the script

yeetlight = Tk()
yeetlight.title('Yeetlight v0.1')

topFrame = Frame(yeetlight)
topFrame.pack()
buttonOff = Button(topFrame, text="Off", bg="black", fg="red", command=bulb.turnoff)
buttonOn = Button(topFrame, text="On", bg="black", fg="green", command=bulb.turnon)
buttonNightmode = Button(topFrame, text="Night mode", bg="black", fg="blue", command=bulb.night)
buttonDaylight = Button(topFrame, text="Daylight bright", bg="black", fg="gold", command=bulb.day)
buttonOn.pack(side=LEFT)
buttonOff.pack(side=LEFT)
buttonDaylight.pack(side=LEFT)
buttonNightmode.pack(side=LEFT)

yeetlight.call('wm', 'attributes', '.', '-topmost', '1') # Force on top of other windows, delete if you wish

yeetlight.mainloop()

