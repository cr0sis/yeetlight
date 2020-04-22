from yeelight import Bulb
import json

class YeetBulb:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.bulb = Bulb(self.ip, effect="smooth", duration=750, auto_on=True)
        
    def __getitem__(self, key):
        return getattr(self, key)

    def turnoff(self):
        self.bulb.turn_off()

    def turnon(self):
        self.bulb.turn_on()

    def toggle(self):
        self.bulb.toggle()

    def loadProfile(self, profile):
        with open('profiles/' + profile + '.json', 'r') as f:
            config = json.load(f)
        
        profile = config['profile']
        
        print('Loading ' + profile['name'])

        if ('rgb' in profile):
            print('Setting RGB: ' + str(profile['rgb']))
            self.bulb.set_rgb(profile['rgb'][0], profile['rgb'][1], profile['rgb'][2])

        if('hsv' in profile):
            print('Setting HSV: ' + str(profile['hsv']))
            self.bulb.set_hsv(profile['hsv'][0], profile['hsv'][1], profile['hsv'][2])
        
        if ('color_temp' in profile):
            print('Setting Colour Temp: ' + str(profile['color_temp']))
            self.bulb.set_color_temp(profile['color_temp'])
        
        if ('brightness' in profile):
            print('Setting Brightness: ' + str(profile['brightness']))
            self.bulb.set_brightness(profile['brightness'])

        if ('color_temp' in profile):
            print('Setting Colour Temp: ' + str(profile['color_temp']))
            self.bulb.set_color_temp(profile['color_temp'])
        
        #self.bulb.set_default()
