# -*- coding: utf-8 -*-

# Copyright (C) 2023 jbleyel, Mr.Servo
#
# OAWeather is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dogtag is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OAWeather.  If not, see <http://www.gnu.org/licenses/>.

# Some parts are taken from msnweathercomponent plugin for compatibility reasons.

from os.path import join, exists, isfile
from traceback import print_exc

from Components.Converter.Converter import Converter
from Components.config import config
from Components.Element import cached

# --------------------------- Logfile -------------------------------

from datetime import datetime
from shutil import copyfile
from os import remove
from os.path import isfile
########################### log file loeschen ##################################

myfile="/tmp/OAWeatherConverter.log"

## If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
############################## File copieren ############################################


###########################  log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus

logstatus = "on"

# ________________________________________________________________________________

def write_log(msg):
    if logstatus == ('on'):
        with open(myfile, "a") as log:

            log.write(datetime.now().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")

            return
    return

# ****************************  test ON/OFF Logfile ************************************************


def logout(data):
    if logstatus == ('on'):
        write_log(data)
        return
    return


# ----------------------------- so muss das commando aussehen , um in den file zu schreiben  ------------------------------
logout(data="start")

class OAWeather(Converter, object):
    logout(data="class")
    CURRENT = 0
    DAY1 = 1
    DAY2 = 2
    DAY3 = 3
    DAY4 = 4
    DAY5 = 5
    DAYS = {
        "current": CURRENT,
        "day1": DAY1,
        "day2": DAY2,
        "day3": DAY3,
        "day4": DAY4,
        "day5": DAY5
    }
    logout(data="class 1")

    def __init__(self, type: str):
        logout(data="init")
        self.enabledebug = config.plugins.OAWeather.debug.value
        Converter.__init__(self, type)
        self.debug("__init__ type:%s" % type)
        self.index = None
        self.mode = None
        self.path = None
        self.logo = None
        self.extension = "png"
        value = type.split(",")
        self.mode = value[0]
        if len(value) > 1:
            logout(data="init 1")
            self.index = self.getIndex(value[1].strip())
            if len(value) > 2 and self.mode in ("weathericon", "yahoocode"):
                logout(data="init 2")
                self.path = value[2].strip()
                if len(value) > 3:
                    logout(data="init 3")
                    self.extension = value[3].strip()
        logout(data="init 4")
        self.debug("__init__ DONE self.mode:%s self.index:%s self.path:%s" % (self.mode, self.index, self.path))
        if config.plugins.OAWeather.debug.value:
            logout(data="init 5")
            self.getText = self.getTextDebug

    def getIndex(self, key: str):
        logout(data="getIndex")
        self.debug("getIndex key:%s" % (key))
        return self.DAYS.get(key, None)

    @cached
    def getTextDebug(self):
        logout(data="gettextdebug")
        self.debug("getText mode:%s index:%s" % (self.mode, self.index))
        text = self.getText()
        self.debug("getText mode:%s index:%s value:%s" % (self.mode, self.index, text))
        return text

    @cached
    def getText(self):
        logout(data="gettext mode")
        logout(data=str(self.mode))
        if self.mode:
            logout(data="gettext 1 index")
            logout(data=str(self.index))
            try:
                if self.index is not None:
                    logout(data="gettext 2")
                    if self.mode == "temperature_high":
                        return self.source.getMaxTemp(self.index)
                    elif self.mode == "temperature_low":
                        return self.source.getMinTemp(self.index)
                    elif self.mode == "temperature_high_low":
                        return self.source.getMaxMinTemp(self.index)


                    elif self.mode == "temperature_text":
                        logout(data="Value of 'day' before calling getKeyforDay: %s" % self.index)
                        #return self.source.getKeyforDay("text", self.index, "")
                        temp_result = self.source.getKeyforDay("text", self.index, "")
                        logout(data="date_result: %s" % temp_result)
                        return temp_result


                    elif self.mode in ("weathericon", "yahoocode"):
                        return self.source.getYahooCode(self.index)
                    elif self.mode == "meteocode":
                        return self.source.getMeteoCode(self.index)
                    elif self.mode == "weekday":
                        return self.source.getKeyforDay("day", self.index)

                    elif self.mode == "weekshortday":
                        logout(data="if weekshortday")
                        return self.source.getKeyforDay("shortDay", self.index)

                    elif self.mode == "date":
                        logout(data="if date")
                        #return self.source.getDate(self.index)
                        date_result = self.source.getDate(self.index)
                        logout(data="date_result: %s" % date_result)
                        return date_result

                    elif self.mode == "precipitation":
                        logout(data="precipitation")
                        return self.source.getPrecipitation(self.index)


                    elif self.mode == "precipitationfull":
                        logout(data="precipitationfull")
                        logout(data="Value of 'day' before calling getKeyforDay: %s" % self.index)
                        #return self.source.getPrecipitation(self.index, True)
                        date1_result = self.source.getPrecipitation(self.index, True)
                        logout(data="date_result: %s" % date1_result)
                        return date1_result
                    else:
                        logout(data="precipitationfull 1")
                        logout(data="Value of 'day' before calling getKeyforDay: %s" % self.index)
                        #return self.source.getKeyforDay(self.mode, self.index, "")
                        date2_result = self.source.getKeyforDay(self.mode, self.index, "")
                        logout(data="date_result: %s" % date2_result)
                        return date2_result

                if self.mode == "weathersource":
                    return self.source.getVal("source")
                elif self.mode == "city":
                    return self.source.getVal("name")
                elif self.mode == "observationPoint":
                    return self.source.getCurrentVal("observationPoint")
                elif self.mode == "observationtime":
                    logout(data="observationtime")
                    return self.source.getObservationTime()
                elif self.mode == "sunrise":
                    return self.source.getSunrise()
                elif self.mode == "sunset":
                    return self.source.getSunset()
                elif self.mode == "isnight":
                    return self.source.getIsNight()
                elif self.mode == "temperature_current":
                    return self.source.getTemperature()
                elif self.mode == "feelslike":
                    return self.source.getFeeltemp()
                elif self.mode == "feelslikefull":
                    return self.source.getFeeltemp(True)
                elif self.mode == "humidity":
                    return self.source.getHumidity()
                elif self.mode == "humidityfull":
                    return self.source.getHumidity(True)
                elif self.mode == "raintext":
                    return self.source.getCurrentVal("raintext", "")
                elif self.mode == "winddisplay":
                    return "%s %s" % (self.source.getWindSpeed(), self.source.getWindDirName())
                elif self.mode == "windspeed":
                    return self.source.getWindSpeed()
                elif self.mode == "winddir":
                    return self.source.getWindDir()
                elif self.mode == "winddirsign":
                    return self.source.getCurrentVal("windDirSign")
                elif self.mode == "winddirarrow":
                    return self.source.getCurrentVal("windDirSign").split(" ")[0]
                elif self.mode == "winddirname":
                    return self.source.getWindDirName()
                elif self.mode == "winddirshort":
                    return self.source.getWindDirShort()
                else:
                    return self.source.getVal(self.mode)

            except Exception as err:
                logout(data="err")
                print("[OAWeather] Converter Error:%s" % str(err))
                print_exc()
            logout(data="gettext 3")
        logout(data="gettext 4")
        return ""

    logout(data="class 3")
    logout(data="gettext 5")

    text = property(getText)
    logout(data="text")
    logout(data=str(text))

    @cached
    def getBoolean(self):
        logout(data="getboolean")
        if self.mode == "raintext":
            return self.source.getCurrentVal("raintext", "") != ""
        elif self.mode in ("daySummary0", "nightSummary0"):
            return self.source.getKeyforDay(self.mode, self.index, "") != ""
        else:
            return False

    boolean = property(getBoolean)

    @cached
    def getIconFilename(self):
        logout(data="geticon")
        if self.mode == "logo":
            try:
                path = join(self.source.pluginpath, "Images", "%s_weather_logo.png" % self.source.logo)
                if isfile(path):
                    return path
            except Exception:
                return ""

        if self.index in (self.CURRENT, self.DAY1, self.DAY2, self.DAY3, self.DAY4, self.DAY5):
            path = self.source.iconpath
            if self.path:
                path = self.path
            if path and exists(path):
                code = self.source.getYahooCode(self.index)
                if code:
                    path = join(path, "%s.%s" % (code, self.extension))
                    if isfile(path):
                        return path
            self.debug("getIconFilename not found mode:%s index:%s self.path:%s path:%s" % (self.mode, self.index, self.path, path))
        return ""

    def debug(self, text: str):
        logout(data="debug")
        if self.enabledebug:
            print("[OAWeather] Converter DEBUG %s" % text)

    logout(data="class 4")
    logout(data="iconfilename")
    iconfilename = property(getIconFilename)
    logout(data="class 5")
    logout(data=str(iconfilename))
    logout(data="iconfilename out")
