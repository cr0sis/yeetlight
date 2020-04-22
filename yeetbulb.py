from yeelight import Bulb

class YeetBulb:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.bulb = Bulb(self.ip, effect="smooth", duration=750, auto_on=True)
        
    def __getitem__(self,key):
        return getattr(self, key)

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