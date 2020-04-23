import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from yeelight import Bulb
from functools import partial
import json
import os
import threading
from yeetbulb import YeetBulb
from timer import Timer

with open('config.json', 'r') as f:
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
        self.setWindowTitle("YeeLight")
        
        # main widget
        self.main_widget = QWidget(self)
        self.main_widget.setProperty('main', True)
        self.setCentralWidget(self.main_widget)
        self.setStyleSheet(open('window.css').read())

        # controls
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setProperty('main', True)
        self.main_widget.setLayout(self.grid_layout)
        self.buildControls()

        # tray menu
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("bulb_off.ico"))
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
            customBtn.clicked.connect(partial(self.setProfile, custom_button['profile']))
            self.grid_layout.addWidget(customBtn, 2, pos)
            pos += 1

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

        if config['tray_menu']['on']:
            on_action = QAction("On", self)
            on_action.triggered.connect(partial(self.turnOn))
            self.tray_menu.addAction(on_action)
        if config['tray_menu']['off']:
            off_action = QAction("Off", self)
            off_action.triggered.connect(self.turnOff)
            self.tray_menu.addAction(off_action)
        if config['tray_menu']['on'] or config['tray_menu']['off']:
            self.tray_menu.addSeparator()

        for custom_item in config['tray_menu']['custom']:
            custom_action = QAction(custom_item['name'], self)
            custom_action.triggered.connect(partial(self.setProfile, custom_item['profile']))
            self.tray_menu.addAction(custom_action)

        if config['tray_menu']['profiles']:
            self.tray_menu.addSeparator()
            profiles_menu = QMenu("profiles", self)
            for file in os.listdir("./profiles"):
                if file.endswith(".json"):
                    with open("./profiles/" + file, 'r') as f:
                        profile = json.load(f)
                        change_profile = QAction(profile['profile']['name'], self)
                        change_profile.triggered.connect(partial(self.setProfile, file.rsplit(".", 1)[0]))
                        profiles_menu.addAction(change_profile)
            profiles_menu.addSeparator()
            update_menu = QAction('Update List', self)
            update_menu.triggered.connect(self.buildTray)
            profiles_menu.addAction(update_menu)
            self.tray_menu.addMenu(profiles_menu)
            self.tray_menu.addSeparator()
        
        if config['tray_menu']['exit']:
            quit_action = QAction("Exit", self)
            quit_action.triggered.connect(qApp.quit)
            self.tray_menu.addAction(quit_action)
        
        self.tray_icon.activated.connect(self.onTrayIconActivated)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def setProfile(self, profile):
        global current
        bulbs[current].loadProfile(profile)
        self.hide()

    def setCurrent(self, bulb):
        global current
        current = bulb
        self.buildTray()
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

    def onTrayIconActivated(self, reason):
        if (reason == 3):
            if config['tray_menu']['left_click'] == "Toggle":
                self.toggle()
            else:
                self.show()
        # print("onTrayIconActivated:", reason)

    def closeEvent(self, event):
        self.hide()

class YeetLight():
    def __init__(self):
        self.updateBulbsTimer = Timer(3, self.updateBulbs)
        # self.updateBulbsTimer.start()

        self.app = QApplication(sys.argv)
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
