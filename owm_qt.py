"""
    Name: owm_gui.py
    Author: William A Loring
    Created: 08-05-2021
    Purpose: OpenWeatherMap GUI with PySide6
    stick with pyside6 for nuitka
    Command line to rebuild ui to py
    pyside6-uic main_window.ui -o main_ui.py
"""

import sys
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
# from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu
# Import gui py file created by QT Designer
from main_ui import Ui_MainWindow
# Import controller class
from owm_class import WeatherClass
# Qt dark palette
import dark_palette


class OWM(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(OWM, self).__init__()
        self.initializeUI()
        # Create weather object with a reference to current class
        self.weather_class = WeatherClass(self)

        # Connect the clicked event/signal to the get_location event handler/slot
        self.btn_get_weather.clicked.connect(self.weather_class.get_location)

        # Exit the program
        self.btn_exit.clicked.connect(self.close)
        self.action_exit.triggered.connect(self.close)
        self.btn_exit.setShortcut("Escape")

        self.action_about.triggered.connect(self.weather_class.about_program)
        self.action_get_weather.triggered.connect(
            self.weather_class.get_location)

        # Remove sizing grip from status bar
        self.status_bar.setSizeGripEnabled(False)
        # Add widgets to status bar
        self.status_bar.addPermanentWidget(self.progress_bar)
        # Set statusbar tips
        self.btn_get_weather.setStatusTip("Get current weather (Press Enter)")
        self.btn_exit.setStatusTip("Exit Program (Press Esc)")
        self.lineEdit.setStatusTip(
            "Enter Town, State, Country (Scottsbluff, NE, US)")

        # Select the input box
        # Wait for the user to click Get Weather or press Return
        self.set_input()

#--------------------- INITIALIZE UI -------------------#
    def initializeUI(self):
        """ Initialize PySide6 QT GUI"""
        # Create the GUI
        self.setupUi(self)
        # Remove title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        # Don't allow window to be resized
        self.setFixedSize(self.size())

#--------------------- SETUP CONTEXT MENU -------------------#
    def contextMenuEvent(self, event):
        """ 
            Override the contextMenuEvent
            Setup a context or right click menu
        """
        # Creating a menu object with the central widget as parent
        menu = QMenu(self)
        # Populating the menu with actions defined in init
        menu.addAction(self.action_about)
        menu.addAction(self.action_get_weather)
        menu.addAction(self.action_exit)
        # Launching the menu
        menu.exec(event.globalPos())

#--------------------- SELECT INPUT -------------------#
    def set_input(self):
        """ Set focus and select lineEdit, wait for user input"""
        self.lineEdit.setFocus()
        self.lineEdit.selectAll()
        self.progress_bar.setValue(0)

#--------------------- GET WEATHER -------------------#
    def get_weather(self):
        """ Get and display weather on form """
        self.progress_bar.setValue(33)
        self.weather_class.get_dictionaries()
        self.weather_class.get_weather()
        self.weather_class.draw_weather_arrow()
        self.progress_bar.setValue(66)
        self.weather_class.display_weather()
        self.progress_bar.setValue(100)
        # Set focus and select lineEdit for next user entry
        self.lineEdit.setFocus()
        self.lineEdit.selectAll()

#-------- OVERRIDE MOUSE EVENTS TO MOVE PROGRAM WINDOW -------------#
    def mousePressEvent(self, event):
        """ Override the mousePressEvent """
        # Store the current position of the mouse in previous position
        self.previous_pos = event.globalPosition()

    def mouseMoveEvent(self, event):
        """ Override the mouseMoveEvent """
        # Subtract the previous position from the current position
        delta = event.globalPosition() - self.previous_pos
        # Add the delta calculation to the current position
        self.move(self.x() + delta.x(), self.y()+delta.y())
        # Store the current position
        self.previous_pos = event.globalPosition()
        # self._drag_active = True

#-------- OVERRIDE KEYPRESS EVENTS TO CAPTURE KEYSTROKES -------------#
    # Overide the keyPressEvent
    def keyPressEvent(self, event):
        # Get location for weather
        if event.key() == QtCore.Qt.Key_Enter or QtCore.Qt.Key_Return:
            self.weather_class.get_location()


#--------------------- START APPLICATION -------------------#
def main():
    # Create application object
    owm = QApplication(sys.argv)
    # Set a QT style
    owm.setStyle('Fusion')
    # Set colors to darkPalette, from external py file
    owm.setPalette(dark_palette.darkPalette)
    # Create program object
    window = OWM()

    # Make program visible
    window.show()
    # Execute the program, setup clean exit of program
    sys.exit(owm.exec())


main()
