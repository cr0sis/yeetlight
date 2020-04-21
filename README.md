# yeetlight
A python GUI script to control Yeelight (xiaomi) smartbulbs

This is a very early draft with just 4 options, which I use the most. Development ongoing.

## Setup

You will need to ensure you have tkinter (should be standard but I found I had to install it) and yeelight installed via:

`pip3 install tk`

`pip3 install yeelight`

You need to connect the light using the Yeelight app (or using any other appropriate way) to your network. Then enable `Developer Mode` (or `LAN Control Mode` in the current version of the app) for the light. This setting may need to be reset after a firmware update. You should also make sure that your DHCP server always assigns the same IP address to the light.
