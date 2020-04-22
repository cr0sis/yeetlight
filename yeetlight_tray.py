#!/usr/bin/env python3
import PySimpleGUIWx as sg
from yeelight import Bulb
from functools import partial
import json
import os
import threading
from yeetbulb import YeetBulb

current = 0

#load config
with open('config.json', 'r') as f:
    config = json.load(f)

bulbs = []
for bulb in config['bulbs']:
    bulbs.append(YeetBulb(bulb['name'], bulb['ip']))

#tray menu

tray_menu = config['tray_menu']
right_click_menu = []
right_click_menu.append('!' + bulbs[current]['name'])
right_click_menu.append('---')
if tray_menu['on']:
    right_click_menu.append('On')
if tray_menu['off']:
    right_click_menu.append('Off')
if tray_menu['on'] or tray_menu['off']:
    right_click_menu.append('---')
for menu_item in tray_menu['custom']:
    right_click_menu.append(menu_item['name'] + '::profile--' + menu_item['profile'])
if tray_menu['profiles']:
    right_click_menu.append('---')
    profiles_menu = []
    for file in os.listdir("./profiles"):
        if file.endswith(".json"):
            with open("./profiles/" + file, 'r') as f:
                profile = json.load(f)
                profiles_menu.append(profile['profile']['name'] + '::profile--' + file.rsplit( ".", 1 )[ 0 ])
    right_click_menu.append('Profiles')
    right_click_menu.append([profiles_menu])
right_click_menu.append('---')
if tray_menu['exit']:
    right_click_menu.append('Exit')


menu_def = ['Toggle', right_click_menu]

tray = sg.SystemTray(menu=menu_def, filename=r'bulb_on.ico')

def updateIcon():
    threading.Timer(1.0, updateIcon).start()
    properties = bulbs[current].bulb.get_properties()
    if properties['power'] == 'off':
        tray.update(None, None, filename=r'bulb_off.ico')
    else:
        tray.update(None, None, filename=r'bulb_on.ico')

updateIcon()

while True:  # The event loop
    menu_item = tray.read()
    print(menu_item)

    menu_item_key = menu_item.rsplit("::")

    if menu_item == '__ACTIVATED__':
        properties = bulbs[current].bulb.get_properties()
        if properties['power'] == 'off':
            tray.update(None, None, filename=r'bulb_on.ico')
            bulbs[current].bulb.turn_on()
        else:
            tray.update(None, None, filename=r'bulb_off.ico')
            bulbs[current].bulb.turn_off()
    if menu_item == 'On':
        tray.update(None, None, filename=r'bulb_on.ico')
        bulbs[current].bulb.turn_on()
    if menu_item == 'Off':
        tray.update(None, None, filename=r'bulb_off.ico')
        bulbs[current].bulb.turn_off()
    if len(menu_item_key) == 2:
        if menu_item_key[1].rsplit("--")[0] == 'profile':
            print(menu_item_key[1])
            bulbs[current].loadProfile(menu_item_key[1].rsplit("--")[1])
    elif menu_item == 'Exit':
        break