# yeetlight
A python GUI script with multi bulb profile support, to control Yeelight (xiaomi) smartbulbs.

## Setup

You will need to ensure you have PyQT5 and yeelight installed via pip

`sudo apt-install python3-pyqt5`

and

`pip install yeelight` or `pip3 install yeelight`

You need to connect the light using the Yeelight app (or using any other appropriate way) to your network. Then enable `Developer Mode` (or `LAN Control Mode` in the current version of the app) for the light. This setting may need to be reset after a firmware update. You should also make sure that your DHCP server always assigns the same IP address to the light.

# Finding your lightbulb IP's with nmap

`sudo apt install nmap`

`nmap -sn 192.168.1.* > nmapresult.txt` Your 1 might be different so change it based on your router, use `ifconfig` to find your ip range.

`nano nmapresult.txt`

Edit your config.json file with the IP(s) of you bulb(s).

## To-do

Convert project gui from tkinter to pysimplegui
        
Optional default when changing mode, instead of forced per mode switch. 
         
systray
        
hotkey menu
        
brightness
        
warmth(K) 
        
colourpicker
        
<s>multi bulb support</s>
        
sliders

Sunset
        
Sunrise
        
Home
        
Romance
        
Date Night
        
Movie Night
        
rainbow mode

irc highlights

bin day notification
