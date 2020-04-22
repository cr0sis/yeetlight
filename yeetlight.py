#!/usr/bin/env python3
from tkinter import *
from yeelight import Bulb
from functools import partial
import json
import os
from yeetbulb import YeetBulb

current = 0

def turnon():
    bulbs[current].turnon()
def turnoff():
    bulbs[current].turnoff()
def loadProfile(profile):
    bulbs[current].loadProfile(profile)

#load config
with open('config.json', 'r') as f:
    config = json.load(f)

bulbs = []
for bulb in config['bulbs']:
    bulbs.append(YeetBulb(bulb['name'], bulb['ip']))

buttons = config['buttons']

#create window
yeetlight = Tk()
yeetlight.title('Yeetlight')
topFrame = Frame(yeetlight)
topFrame.pack()

#create buttons
if buttons['on']:
    Button(topFrame, text="On", bg="black", fg="green", command=turnon).pack(side=LEFT)
if buttons['off']:
    Button(topFrame, text="Off", bg="black", fg="red", command=turnoff).pack(side=LEFT)
for button in buttons['custom']:
    tbtn = Button(topFrame, text=button['name'], bg=button['bg'], fg=button['fg'], command=partial(loadProfile, button['profile']))
    tbtn.pack(side=LEFT)

#create profile dropdown
profileSelect = StringVar(yeetlight)
profiles = []

for file in os.listdir("./profiles"):
    if file.endswith(".json"):
        profiles.append(file.rsplit( ".", 1 )[ 0 ])

OptionMenu(topFrame, profileSelect, *profiles).pack()
profileSelect.set('Profile')

def set_profile(*args):
    loadProfile(profileSelect.get())

profileSelect.trace('w', set_profile)

#create light dropdown
tkvar = StringVar(yeetlight)
choices = [x["name"] for x in bulbs]
choices = dict(zip(choices, range(len(choices))))
OptionMenu(topFrame, tkvar, *choices.keys()).pack()
tkvar.set('Bulb')

def change_dropdown(*args):
    global current
    current = choices[tkvar.get()]

tkvar.trace('w', change_dropdown)

yeetlight.call('wm', 'attributes', '.', '-topmost', '1') # Force on top of other windows, delete if you wish
yeetlight.mainloop()