"""
    Name: owm_gui.py
    Author: William A Loring
    Created: 08-05-2021
    Purpose: OpenWeatherMap GUI with PySide6
    stick with pyside6 for nuitka
    Command line to rebuild ui to py
    pyside6-uic main_window.ui –o main_ui.py
"""

import sys
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

        """ Initialize PySide6 QT GUI"""
        # Create the GUI
        self.setupUi(self)
        # Set program corner icon
        # self.setWindowIcon(QtGui.QIcon("weather.ico"))
        # Remove title bar
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Create weather object with a reference to current class
        self.weather_class = WeatherClass(self)

        # QAction *act1 = new QAction(this);
        # QAction *act2 = new QAction(act1);
        # act1->setShortcut("Ctrl+O");
        # act2->setShortcut("Ctrl+L");
        # connect(act2, SIGNAL(triggered(bool)), act1, SIGNAL(triggered(bool)));

        QAction
        # Connect the clicked event/signal to the set_weather event handler/slot
        self.btn_get_weather.clicked.connect(self.weather_class.get_location)
        self.btn_get_weather.setShortcut("Return")

        # Exit the program
        self.btn_exit.clicked.connect(self.close)
        self.btn_exit.setShortcut("Esc")
        self.action_exit.triggered.connect(self.close)

        self.action_about.triggered.connect(self.weather_class.about_program)
        self.action_get_weather.triggered.connect(
            self.weather_class.get_location)

        # Add widgets to status bar
        self.status_bar.addPermanentWidget(self.progress_bar)
        # Set statusbar tips
        self.btn_get_weather.setStatusTip("Get current weather")
        self.btn_exit.setStatusTip("Exit")
        self.lineEdit.setStatusTip(
            "Enter Town, State, Country (Scottsbluff, NE, US)")

        # Select the input box
        # Wait for the user to click Get Weather or press Return
        self.set_input()

#--------------------- SELECT INPUT -------------------#
    def contextMenuEvent(self, event):
        # Creating a menu object with the central widget as parent
        menu = QMenu(self)
        # Populating the menu with actions
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

    def mouseReleaseEvent(self, event):
        """ Override the mouseReleaseEvent """
        pass
        # if self._drag_active:
        #     self._drag_active = False


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
