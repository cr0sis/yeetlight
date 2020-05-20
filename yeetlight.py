import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import *
from yeelight import Bulb
from functools import partial
import json
import os
import threading
from yeetbulb import YeetBulb
from timer import Timer

basedir = os.path.dirname(sys.argv[0])

with open(basedir + '/config.json', 'r') as f:
    config = json.load(f)

bulbs = []
for bulb in config['bulbs']:
    bulbs.append(YeetBulb(bulb['name'], bulb['ip']))

current = config['default'] or 0

class MainWindow(QMainWindow):
    check_box = None
    tray_icon = None
 
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen)
        self.setFixedSize(QSize(480, 160))
        self.setWindowTitle("YeetLight")
        
        # main widget
        self.main_widget = QWidget(self)
        self.main_widget.setProperty('main', True)
        self.setCentralWidget(self.main_widget)
        self.setStyleSheet(open(basedir + '/window.css').read())

        # controls
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setProperty('main', True)
        self.main_widget.setLayout(self.grid_layout)
        self.buildControls()

        # tray menu
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(basedir + '/bulb_off.ico'))
        self.tray_menu = QMenu()
        self.buildTray()

        screen = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = screen.width() - widget.width()
        y = (screen.height() - 60) - widget.height()
        self.move(x, y)

    def buildControls(self):
        global current

        if 'on' in config['buttons'] and config['buttons']['on'] == True:
            onBtn = QPushButton('On')
            onBtn.setProperty('big', True)
            onBtn.clicked.connect(self.turnOn)
            self.grid_layout.addWidget(onBtn, 1, 0)
        if 'off' in config['buttons'] and config['buttons']['off'] == True:
            offBtn = QPushButton('Off')
            offBtn.setProperty('big', True)
            offBtn.clicked.connect(self.turnOff)
            self.grid_layout.addWidget(offBtn, 1, 1)
        if 'hide' in config['buttons'] and config['buttons']['hide'] == True:
            hideBtn = QPushButton('Hide')
            hideBtn.setProperty('big', True)
            hideBtn.clicked.connect(self.hide)
            self.grid_layout.addWidget(hideBtn, 1, 2)
        pos = 0
        for custom_button in config['buttons']['custom']:
            customBtn = QPushButton(custom_button['name'])
            customBtn.setProperty('custom', True)
            if 'bg' in custom_button or 'fg' in custom_button:
                customBtn.setStyleSheet("background-color: " + custom_button['bg'] + "; color: " + custom_button['fg'] + ";")
            customBtn.clicked.connect(partial(self.loadJson, custom_button['preset']))
            self.grid_layout.addWidget(customBtn, 2, pos)
            pos += 1
        if 'brightness' in config['buttons'] and config['buttons']['brightness'] == True:
            self.brightness_slider = QSlider(Qt.Horizontal)
            self.brightness_slider.setMinimum(0)
            self.brightness_slider.setMaximum(100)
            # if bulbs[current].bulb.get_properties(['current_brightness']):
            #     self.brightness_slider.setValue(bulbs[current].bulb.get_properties(['current_brightness'][0]))
            self.brightness_slider.setTickPosition(QSlider.TicksBelow)
            self.brightness_slider.setTickInterval(25)
            self.brightness_slider.setTracking(False)
                
            self.grid_layout.addWidget(self.brightness_slider, 3, 0, 1, 3)
            self.brightness_slider.valueChanged.connect(partial(self.setBrightness, True))

    def buildTray(self):
        global current
        self.tray_menu.clear()
        bulbs_menu = QMenu(bulbs[current]['name'], self)
        if len(bulbs) > 1:
            for id, bulb in enumerate(bulbs):
                change_current = QAction(bulb.name, self)
                change_current.triggered.connect(partial(self.setCurrent, id))
                bulbs_menu.addAction(change_current)
        self.tray_menu.addMenu(bulbs_menu)
        self.tray_menu.addSeparator()

        if 'on' in config['tray_menu'] and config['tray_menu']['on']:
            on_action = QAction("On", self)
            on_action.triggered.connect(partial(self.turnOn))
            self.tray_menu.addAction(on_action)
        if 'off' in config['tray_menu'] and config['tray_menu']['off']:
            off_action = QAction("Off", self)
            off_action.triggered.connect(self.turnOff)
            self.tray_menu.addAction(off_action)
        if ('on' in config['tray_menu'] or 'off' in config['tray_menu']) and (config['tray_menu']['on'] or config['tray_menu']['off']):
            self.tray_menu.addSeparator()

        if 'custom' in config['tray_menu']:
            for custom_item in config['tray_menu']['custom']:
                custom_action = QAction(custom_item['name'], self)
                custom_action.triggered.connect(partial(self.loadJson, basedir + '/presets/' + custom_item['preset']))
                self.tray_menu.addAction(custom_action)

        if 'presets' in config['tray_menu'] and config['tray_menu']['presets']:
            self.tray_menu.addSeparator()
            presets_menu = self.dirMenu('/presets', 'Presets')
            presets_menu.addSeparator()
            update_menu = QAction('Update List', self)
            update_menu.triggered.connect(self.buildTray)
            presets_menu.addAction(update_menu)
            self.tray_menu.addMenu(presets_menu)
            self.tray_menu.addSeparator()

        if 'profiles' in config['tray_menu'] and config['tray_menu']['profiles']:
            self.tray_menu.addSeparator()
            profiles_menu = self.dirMenu('/profiles', 'Profiles')
            profiles_menu.addSeparator()
            update_menu = QAction('Update List', self)
            update_menu.triggered.connect(self.buildTray)
            profiles_menu.addAction(update_menu)
            self.tray_menu.addMenu(profiles_menu)
            self.tray_menu.addSeparator()
        
        if 'brightness' in config['tray_menu'] and config['tray_menu']['brightness']:
            self.tray_menu.addSeparator()
            brightness_menu = QMenu("Brightness", self)
            brightness_100 = QAction("100%", self)
            brightness_100.triggered.connect(partial(self.setBrightness, False, 100))
            brightness_menu.addAction(brightness_100)
            brightness_75 = QAction("75%", self)
            brightness_75.triggered.connect(partial(self.setBrightness, False, 75))
            brightness_menu.addAction(brightness_75)
            brightness_50 = QAction("50%", self)
            brightness_50.triggered.connect(partial(self.setBrightness, False, 50))
            brightness_menu.addAction(brightness_50)
            brightness_25 = QAction("25%", self)
            brightness_25.triggered.connect(partial(self.setBrightness, False, 25))
            brightness_menu.addAction(brightness_25)
            brightness_0 = QAction("0%", self)
            brightness_0.triggered.connect(partial(self.setBrightness, False, 0))
            brightness_menu.addAction(brightness_0)
            self.tray_menu.addMenu(brightness_menu)
            self.tray_menu.addSeparator()

        set_colour = QAction("Set Colour", self)
        set_colour.triggered.connect(self.setColour)
        self.tray_menu.addAction(set_colour)
        
        if 'exit' in config['tray_menu'] and config['tray_menu']['exit']:
            quit_action = QAction("Exit", self)
            quit_action.triggered.connect(qApp.quit)
            self.tray_menu.addAction(quit_action)
        
        self.tray_icon.activated.connect(self.onTrayIconActivated)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def dirMenu(self, directory, name):
        dir_menu = QMenu(name, self)
        for item in os.listdir(basedir + directory):
            if os.path.isdir(basedir + directory + '/' + item):
                sub_menu = self.dirMenu(directory + '/' + item, item)
                dir_menu.addMenu(sub_menu)
            if item.endswith(".json"):
                with open(basedir + directory + '/' + item, 'r') as f:
                    jason_file = json.load(f)
                    change_preset = QAction(jason_file['name'], self)
                    change_preset.triggered.connect(partial(self.loadJson, basedir + directory + '/' + item))
                    dir_menu.addAction(change_preset)
        return dir_menu

    def loadJson(self, file):
        global current
        with open(file, 'r') as f:
            json_config = json.load(f)

        if 'preset' in json_config:
            bulbs[current].loadPreset(file)

        if 'profile' in json_config:
            for item in json_config['profile']:
                if 'preset' in item:
                    bulbs[item['bulb']].loadPreset(basedir + '/presets/' + item['preset'] + '.json')
                if 'rgb' in item:
                    bulbs[item['bulb']].bulb.set_rgb(item['rgb'][0], item['rgb'][1], item['rgb'][2])
                if 'brightness' in item:
                    bulbs[item['bulb']].bulb.set_brightness(item['brightness'])
                if 'off' in item:
                    bulbs[item['bulb']].bulb.turn_off()
        self.hide()

    def setCurrent(self, bulb):
        global current
        current = bulb
        self.buildTray()
        self.buildControls()
        self.hide()

    def turnOn(self):
        global current
        bulbs[current].bulb.turn_on()
        self.hide()

    def turnOff(self):
        global current
        bulbs[current].bulb.turn_off()
        self.hide()

    def toggle(self):
        global current
        bulbs[current].bulb.toggle()
        self.hide()

    def setBrightness(self, slider, brightness = 100):
        global current
        if slider:
            bulbs[current].bulb.set_brightness(self.brightness_slider.value())
        else:
            bulbs[current].bulb.set_brightness(brightness)

    def onTrayIconActivated(self, reason):
        if (reason == 3):
            if config['tray_menu']['left_click'] == "Toggle":
                self.toggle()
            else:
                if (self.isVisible()):
                    self.hide()
                else:
                    self.show()
        # print("onTrayIconActivated:", reason)

    def setColour(self):
        self.picker = ColorPicker(self)
        color = self.picker.getColor()
        if color.isValid():
            bulbs[current].bulb.set_rgb(color.red(), color.green(), color.blue())
        self.hide()

    def closeEvent(self, event):
        self.hide()

class ColorPicker(QColorDialog):
    def __init__(self, parent=None):
        super(ColorPicker, self).__init__(parent)
        self.ui = QColorDialog()
        self.ui.accepted.connect(self.accept)
        self.ui.rejected.connect(self.reject)

class YeetLight():
    def __init__(self):
        self.updateBulbsTimer = Timer(3, self.updateBulbs)
        # self.updateBulbsTimer.start()

        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.mw = MainWindow()

    def updateBulbs(self):
        global bulbs
        for bulb in bulbs:
            bulb.updateProperties()

    def run(self):
        sys.exit(self.app.exec_())
        # self.updateBulbsTimer.stop()
 
if __name__ == "__main__":
    yeet = YeetLight()
    yeet.run()
