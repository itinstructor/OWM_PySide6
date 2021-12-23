"""
    Name: weather_console_class.py
    Author: William A Loring
    Created: 07/04/21
    Purpose: OOP console app
    Get lat and lon from Openweather map current weather
"""

from PySide6 import QtGui
from PySide6.QtCore import QRectF, Qt
from PySide6.QtWidgets import QMessageBox
import requests
import weather_utils
# import geocode_owm for reverse geocode
import geocode_geopy
# Request icon from url
import urllib.request


class WeatherClass:

    def __init__(self, owm):
        """
            Add owm reference to access owm from this class
        """
        # Create blank dictionary for weather data
        self.__weather_data = {}
        # Create owm object reference for access
        self.owm = owm

#--------------------------------- GET LOCATION -------------------------------------#
    def get_location(self):
        """
            Get weather location and weather information
        """
        try:
            # Get the text in the lineEdit text box
            location = self.owm.lineEdit.text()
            # Get location input from user
            self.__location = location

            # Build the openweathermap api url
            url = weather_utils.URL + self.__location

            # Get the weather information out as a weather object
            response = requests.get(url)
            # print(response.text)

            # If the status_code is 200, successful connection and data
            if(response.status_code == 200):
                # Load json response into __weather dictionary
                self.__weather_data = response.json()
                # For testing
                # print(self.__weather)
                # Let user know the connection was successful
                # print("\n[+] The connection to OpenWeatherMap was successful.")

            else:
                # If there was a response code other than 200
                title = "Problem"
                message = f"The response status code for OWM weather was: {response.status_code}"
                message += "\nYou may have typed an invalid location."
                message += "\nPlease try again."
                QMessageBox.information(self.owm, title, message)
                # Select the input box, let the user try again
                self.owm.set_input()
        except:
            # Handle connection exception
            title = "Problem"
            message = "[-] Sorry, there was a problem connecting."
            message += "\nPlease try again."
            QMessageBox.information(self.owm, title, message)
            # Select the input box, let the user try again
            self.owm.set_input()

        # Succesful connection to OWM, get the weather
        self.owm.get_weather()

#-------------------------- GET DICTIONARIES ----------------------------#
    def get_dictionaries(self):
        """
            Get individual weather information dictionaries
            from main self.__weather dictionary
        """
        # temp, feels_like, temp_min, temp_max, pressure, humidity
        self.__main_dict = self.__weather_data.get("main")
        # id, main, description, icon
        self.__weather_dict = self.__weather_data.get("weather")[0]
        # Wind speed and direction
        self.__wind_dict = self.__weather_data.get("wind")
        # Cloud information
        self.__clouds_dict = self.__weather_data.get("clouds")
        # Sunrise and Sunset time
        self.__sys_dict = self.__weather_data.get("sys")
        # Latitude and Longitude
        self.__coord_dict = self.__weather_data.get("coord")

#-------------------------- GET WEATHER ----------------------------#
    def get_weather(self):
        """
            Get individual weather items from dictionaries
        """
        # Get time of data calculation
        self.time = weather_utils.convert_time(self.__weather_data.get("dt"))

        # Get description of current weather. Ex: Clear Skies
        self.description = self.__weather_dict.get("description").title()
        # Get fahrenheit temperature
        self.temperature = round(self.__main_dict.get("temp"), 1)
        # Get feels like temperature
        self.feels_like = round(self.__main_dict.get("feels_like"), 1)
        # Get humidity
        self.humidity = self.__main_dict.get("humidity")
        # Get pascals and convert to inches of mercury
        self.pressure = round(self.__main_dict.get('pressure') / 33.86, 2)

        # Get wind speed and direction
        self.wind_speed = round((self.__wind_dict.get("speed")), 1)
        self.degrees = self.__wind_dict.get("deg")
        self.cardinal_direction = weather_utils.degrees_to_cardinal(
            self.degrees)

        # Get cloud cover percentage
        self.clouds = self.__clouds_dict.get("all")

        # Get sunrise and sunset time from API in Unix UTC
        sunrise_time = self.__sys_dict.get("sunrise")
        sunset_time = self.__sys_dict.get("sunset")
        # Add shift in seconds from UTC
        sunrise_time = sunrise_time + self.__weather_data.get("timezone")
        sunset_time = sunset_time + self.__weather_data.get("timezone")
        # Convert from Unix UTC timestamp to Python time
        self.sunrise_time = weather_utils.convert_time(sunrise_time)
        self.sunset_time = weather_utils.convert_time(sunset_time)

        # Get latitude and longitude
        self.latitude = self.__coord_dict.get("lat")
        self.longitude = self.__coord_dict.get("lon")

        # Reverse gecode the address
        self.address = geocode_geopy.reverse_geocode(
            self.latitude, self.longitude)
        # Get OWM weather icon from url
        self.get_weather_icon()

#-------------------------- GET WEATHER ICON FROM URL ----------------------------#
    def get_weather_icon(self):
        """
            Get OWM weather icon from url in weather dictionary
        """
        # Get url for weather icon
        icon_id = self.__weather_dict.get("icon")
        weather_icon_url = f'http://openweathermap.org/img/wn/{icon_id}.png'

        # Get the data from the weather icon url
        data = urllib.request.urlopen(weather_icon_url).read()

        # Create a QT Image object
        self.weather_icon_image = QtGui.QImage()

        # Load the url data into the image object
        self.weather_icon_image.loadFromData(data)

        self.get_air_quality()

#--------------------- DISPLAY WEATHER ON FORM -------------------#
    def display_weather(self):
        """
            Get information from owm_class, display on form
        """
        # Display reverse geocode address to confirm that we have the right location
        self.owm.lbl_reverse_geocode.setText(f'{self.address}')

        # Display weather information on form
        self.owm.lbl_temperature.setText(f'{self.temperature}°F 🌡')
        self.owm.lbl_description.setText(f"{self.description}")
        self.owm.lbl_feels_like.setText(f"{self.feels_like}°F")
        self.owm.lbl_humidity.setText(f"{self.humidity}%")
        self.owm.lbl_pressure.setText(f"{self.pressure} inHg")
        self.owm.lbl_wind.setText(
            f"{self.wind_speed} mph {self.cardinal_direction}")
        self.owm.lbl_cloud_cover.setText(f"{self.clouds}%")
        self.owm.lbl_sunrise.setText(f"{self.sunrise_time}")
        self.owm.lbl_sunset.setText(f"{self.sunset_time}")
        self.owm.lbl_latitude.setText(f"{self.latitude}")
        self.owm.lbl_longitude.setText(f"{self.longitude}")

        # Get and display OpenWeatherMap Icon on form
        self.owm.lbl_weather_icon.setPixmap(QtGui.QPixmap(
            self.weather_icon_image))

        # Display Air Quality Index
        self.owm.lbl_aqi.setText(
            f"{self.aqi} {self.aqi_string}")
        self.owm.lbl_ozone.setText(f"{self.ozone} µg/m³")
        self.owm.lbl_pm25.setText(f"{self.pm25} µg/m³")
        self.owm.lbl_pm10.setText(f"{self.pm10} µg/m³")
        self.owm.lbl_carbon_monoxide.setText(
            f"{self.carbon_monoxide} µg/m³")
        self.owm.lbl_sulphur_dioxide.setText(
            f"{self.sulphur_dioxide} µg/m³")
        self.owm.lbl_nitrogen_dioxide.setText(
            f"{self.nitrogen_dioxide} µg/m³")

#------------------------------- AIR QUALITY INDEX -------------------------------------#
    def get_air_quality(self):
        """ 
            Get Air Quality Index from OpenWeatherMap with API call
            How do I calculate the AQI from pollutant concentration data? 
            The AQI is the highest value calculated for each pollutant as follows:
            Identify the highest concentration among all of the monitors
            within each reporting area and truncate as follows:
              Ozone (ppm) – truncate to 3 decimal places
              PM2.5 (μg/m3) – truncate to 1 decimal place
              PM10 (μg/m3) – truncate to integer
              CO (ppm) truncate to 1 decimal place
              SO2 (ppb) – truncate to integer
              NO2 (ppb) – truncate to integer 
        """
        params = {
            "lat": self.latitude,
            "lon": self.longitude
        }
        # Build request with url and parameters
        url = weather_utils.AQI_ENDPOINT
        try:
            response = requests.get(url, params)
            # print(response.text)

            # If the status_code is 200, successful connection and data
            if(response.status_code == 200):
                # Load json response into dictionary
                data = response.json()
                # Air Quality Index from OWM
                self.aqi = data.get("list")[0].get("main").get("aqi")

                # Ground level ozone, convert ug/m3 to ppm truncate to 3 decimal places
                # Get and truncate the ug/m3 data
                self.ozone = round(data.get("list")[0].get(
                    "components").get("o3"), 3)

                # Fine particulates truncate to 1 decimal place
                self.pm25 = round(data.get("list")[0].get(
                    "components").get("pm2_5"), 1)

                # Coarse particulates truncate to nearest integer
                self.pm10 = round(data.get("list")[0].get(
                    "components").get("pm10"))

                # Carbon Monoxide round to 1 decimal place
                carbon_monoxide = data.get(
                    "list")[0].get("components").get("co")
                self.carbon_monoxide = round(carbon_monoxide, 1)

                # Sulphur Dioxide round to nearest integer
                sulphur_dioxide = data.get(
                    "list")[0].get("components").get("so2")
                self.sulphur_dioxide = round(sulphur_dioxide)

                # Nitrogen Dioxide round to nearest integer
                nitrogen_dioxide = data.get(
                    "list")[0].get("components").get("no2")
                self.nitrogen_dioxide = round(nitrogen_dioxide)

                # Convert AQI to text
                if self.aqi == 1:
                    self.aqi_string = "Good"
                elif self.aqi == 2:
                    self.aqi_string = "Fair"
                elif self.aqi == 3:
                    self.aqi_string = "Moderate"
                elif self.aqi == 4:
                    self.aqi_string = "Poor"
                elif self.aqi == 5:
                    self.aqi_string = "Very Poor"
            else:
                title = "Problem"
                message = f"The response status code for OWM AQI was: {response.status_code}"
                message += "\nPlease try again."
                QMessageBox.information(self.owm, title, message)
        except:
            title = "Problem"
            message = "[-] Sorry, there was a problem connecting with OWM AQI."
            message += "\nPlease try again."
            QMessageBox.information(self.owm, title, message)

    #--------------------- DRAW WEATHER ARROW -------------------#
    def draw_weather_arrow(self):
        # Get the size of the label, create pixmap the same size
        pixmap = QtGui.QPixmap(self.owm.lbl_wind_arrow.size())
        # Clear the pixmap
        pixmap.fill(Qt.transparent)
        # Create a QPainter object to draw on the pixmap
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Create a pen color, width, type of line
        pen = QtGui.QPen(Qt.blue, 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawEllipse(15, 15, 50, 50)

        # Change brush and pen color
        painter.setBrush(Qt.red)
        painter.setPen(Qt.NoPen)

        # Create rectangle to draw pie shape in
        rect = QRectF(10, 10, 60, 60)

        # Set the start angle + 80 degrees as drawPie starts at 90 degrees
        # multiply by 16, the drawing angle increments in 1/16 of a degree
        # Convert from clockwise to counterclockwise
        startAngle = ((-self.degrees + 80) % 360) * 16

        spanAngle = 20 * 16
        # Draw weather direction
        painter.drawPie(rect, startAngle, spanAngle)
        # End drawing, paint to pixmap
        painter.end()
        # Set pixmap to label
        self.owm.lbl_wind_arrow.setPixmap(pixmap)

#----------------------- ABOUT MESSAGE BOX -------------------#
    def about_program(self):
        title = "OWM Weather App"
        message = "Built with: Python 3.9.9 and PySide 6.12."
        message += "\nAuthor: Bill Loring"
        QMessageBox.about(self.owm, title, message)
