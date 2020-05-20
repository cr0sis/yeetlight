from yeelight import Bulb
import json
import sys
import os

basedir = os.path.dirname(sys.argv[0])

class YeetBulb:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.bulb = Bulb(self.ip, effect="smooth", duration=750, auto_on=True)
        self.properties = self.bulb.get_properties()

    def __getitem__(self, key):
        return getattr(self, key)

    def turnoff(self):
        self.bulb.turn_off()

    def turnon(self):
        self.bulb.turn_on()

    def toggle(self):
        self.bulb.toggle()

    def loadPreset(self, preset):
        if os.path.isfile(preset):
            with open(preset, 'r') as f:
                config = json.load(f)

            if 'preset' in config:
                preset = config['preset']
                if ('rgb' in preset):
                    try:
                        self.bulb.set_rgb(preset['rgb'][0], preset['rgb'][1], preset['rgb'][2])
                    except:
                        print('not supported by bulb')
                if('hsv' in preset):
                    try:
                        self.bulb.set_hsv(preset['hsv'][0], preset['hsv'][1], preset['hsv'][2])
                    except:
                        print('not supported by bulb')
                if ('color_temp' in preset):
                    try:
                        self.bulb.set_color_temp(preset['color_temp'])
                    except:
                        print('not supported by bulb')
                if ('brightness' in preset):
                    try:
                        self.bulb.set_brightness(preset['brightness'])
                    except:
                        print('not supported by bulb')
                if ('color_temp' in preset):
                    try:
                        self.bulb.set_color_temp(preset['color_temp'])
                    except:
                        print('not supported by bulb')
        else:
            print('File not found: ' + preset)
    
    def updateProperties(self):
        self.properties = self.bulb.get_properties()
