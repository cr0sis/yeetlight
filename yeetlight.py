#!/usr/bin/env python3
from tkinter import *
from yeelight import Bulb
from yeetbulb import YeetBulb
import json

current = 0

def turnon():
    bulbs[current].turnon()
def turnoff():
    bulbs[current].turnoff()
def day():
    bulbs[current].day()
def night():
    bulbs[current].night()

#load config
with open('config.json', 'r') as f:
    config = json.load(f)

bulbs = []
for bulb in config['bulbs']:
    bulbs.append(YeetBulb(bulb['name'], bulb['ip']))

#create window
yeetlight = Tk()
yeetlight.title('Yeetlight')
topFrame = Frame(yeetlight)
topFrame.pack()

#create buttons
buttonOn = Button(topFrame, text="On", bg="black", fg="green", command=turnon)
buttonOn.pack(side=LEFT)
buttonOff = Button(topFrame, text="Off", bg="black", fg="red", command=turnoff)
buttonOff.pack(side=LEFT)
buttonDaylight = Button(topFrame, text="Daylight bright", bg="black", fg="gold", command=day)
buttonDaylight.pack(side=LEFT)
buttonNightmode = Button(topFrame, text="Night mode", bg="black", fg="blue", command=night)
buttonNightmode.pack(side=LEFT)

#create light dropdown
tkvar = StringVar(yeetlight)
choices = [x["name"] for x in bulbs]
choices = dict(zip(choices,range(len(choices))))
OptionMenu(topFrame, tkvar, *choices.keys()).pack()
tkvar.set('Select')

# on change dropdown value
def change_dropdown(*args):
    global current
    current = choices[tkvar.get()]

# link function to change dropdown
tkvar.trace('w', change_dropdown)

yeetlight.call('wm', 'attributes', '.', '-topmost', '1') # Force on top of other windows, delete if you wish
yeetlight.mainloop()