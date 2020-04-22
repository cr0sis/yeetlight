# yeetlight
A python GUI script to control Yeelight (xiaomi) smartbulbs

This is a very early draft with just 4 options, which I use the most. See todo.txt for more information.

## Setup

You will need to ensure you have tkinter (should be standard but I found I had to install it) and yeelight installed via pip

`pip install tk`

`pip install yeelight`

You need to connect the light using the Yeelight app (or using any other appropriate way) to your network. Then enable `Developer Mode` (or `LAN Control Mode` in the current version of the app) for the light. This setting may need to be reset after a firmware update. You should also make sure that your DHCP server always assigns the same IP address to the light.

### Finding your llightbulb IP's with nmap

`sudo apt install nmap`

`nmap -sn 192.168.1.* > nmapresult.txt`

`nano nmapresult.txt`
