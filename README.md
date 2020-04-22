# yeetlight
A python GUI script to control Yeelight (xiaomi) smartbulbs

This is a very early draft with just 4 options, which I use the most. See todo.txt for more information.

## Setup

You will need to ensure you have tkinter (should be standard but I found I had to install it) and yeelight installed via pip

`pip install tk` or `pip3 install tk`

`pip install yeelight` or `pip3 install yeelight`

You need to connect the light using the Yeelight app (or using any other appropriate way) to your network. Then enable `Developer Mode` (or `LAN Control Mode` in the current version of the app) for the light. This setting may need to be reset after a firmware update. You should also make sure that your DHCP server always assigns the same IP address to the light.

### Finding your lightbulb IP's with nmap

`sudo apt install nmap`

`nmap -sn 192.168.1.* > nmapresult.txt` Your 1 might be different so change it based on your router, use `ifconfig` to find your ip range.

`nano nmapresult.txt`

#### To-do

Main: 

        -Convert project gui from tkinter to pysimplegui
        
        -Optional default when changing mode, instead of forced per mode switch. Currently any mode change sets itself as    default, meaning if you flip the main switch off and on it automatically remembers last config. 
        
        -systray
        
        -hotkey menu
        
        -brightness
        
        -warmth(K)
        
        -colourpicker
        
        -multi bulb support
        
        -sliders!!
Light modes:

        -Sunset
        
        -Sunrise
        
        -Home
        
        -Romance
        
        -Date Night
        
        -Movie Night
        
        -rainbow mode



Fluff:
        -irc highlights
        -bin day notification
