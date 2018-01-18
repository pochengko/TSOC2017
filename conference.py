# -*- coding: utf-8 -*-
__author__ = 'krishnateja'

import logging
from flaskext.mysql import MySQL
from flask import Flask, render_template
from flask_ask import Ask, statement, question

mysql = MySQL()

app = Flask(__name__)
app.config.from_object(__name__)
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
app.config['MYSQL_DATABASE_DB'] = 'db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_conference():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("TemperatureIntent")
def ask_if_speaker(sensor):
    if sensor == 'school':
       sensor = 'C'
    else:
        sensor = sensor
    cursor = mysql.connect().cursor()
    cursor.execute(
        "SELECT temp, hum, PM25, PM10 from LoRa WHERE sensor LIKE '%" + sensor +"%' ORDER BY timestamp DESC Limit 1 ;")

    data = cursor.fetchall()
    #((data[0])[0]):temp, ((data[0])[1]):hum, ((data[0])[2]):PM25, ((data[0])[3]):PM10
    if data is None:
        message = "There was no data by that time."
    elif ((data[0])[0]) > 29:
        message = "The temperature is " + str((data[0])[0]) + " degrees Celsius, " \
                  "and the humidity is " + str((data[0])[1]) + " percents now. " \
                  "It's raining fire. Would you want me to turn on the air conditioner?"
    elif ((data[0])[0]) < 17:
        message = "The temperature is " + str((data[0])[0]) + " degrees Celsius, " \
                  "and the humidity is " + str((data[0])[1]) + " percents now. " \
                  "It's freezing. Would you want me to turn on the heater?"
    else:
        if ((data[0])[1]) > 39 and ((data[0])[1]) < 51:
            message = "The temperature is " + str((data[0])[0]) + " degrees Celsius, " \
                      "and the humidity is " + str((data[0])[1]) + " percents now. " \
                      "At this temperature, relative humidity at 40 to 50 percents it is suitable for human"
        elif ((data[0])[1]) < 40 :
            message = "The temperature is " + str((data[0])[0]) + " degrees Celsius, " \
                      "and the humidity is " + str((data[0])[1]) + " percents now. " \
                      "Be careful. the air is too dry."
        elif ((data[0])[1]) > 50 :
            message = "The temperature is " + str((data[0])[0]) + " degrees Celsius, " \
                      "and the humidity is " + str((data[0])[1]) + " percents now. " \
                      "Be careful. the air is too wet."
        #return statement(message)

    return statement(message)


@ask.intent("HumidityIntent")
def ask_if_speaker(sensor):
    if sensor == 'school':
       sensor = 'C'
    else:
        sensor = sensor
    cursor = mysql.connect().cursor()

    cursor.execute(
        "SELECT temp, hum, PM25, PM10 from LoRa WHERE sensor LIKE '%" + sensor +"%' ORDER BY timestamp DESC Limit 1 ;")

    data = cursor.fetchall()
    if data is None:
        message = "There was no data by that time."
    elif ((data[0])[0]) > 29:
        message = "The temperature is " + str((data[0])[0]) + " degrees Celsius, " \
                  "and the humidity is " + str((data[0])[1]) + " percents now. " \
                  "It's raining fire. Would you want me to turn on the air conditioner?"
    elif ((data[0])[0]) < 17:
        message = "The temperature is " + str((data[0])[0]) + " degrees Celsius, " \
                  "and the humidity is " + str((data[0])[1]) + " percents now. " \
                  "It's freezing. Would you want me to turn on the heater?"
    else:
        if ((data[0])[1]) > 39 and ((data[0])[1]) < 51:
            message = "The temperature is " + str((data[0])[0]) + " degrees Celsius, " \
                      "and the humidity is " + str((data[0])[1]) + " percents now. " \
                      "At this temperature, relative humidity at 40 to 50 percents it is suitable for human"
        else:
            message = "The temperature is " + str((data[0])[0]) + " degrees Celsius, " \
                      "and the humidity is " + str((data[0])[1]) + " percents now. " \
                      "Be careful. It is abnormal for humidity data."
        #return statement(message)

    return statement(message)


@ask.intent("AirqualityIntent")
def ask_if_speaker(sensor):
    #sensor = sensor

    if sensor == 'school':
       sensor = 'C'
    else:
        sensor = sensor

    cursor = mysql.connect().cursor()

    cursor.execute(
        "SELECT temp, hum, PM25, PM10 from LoRa WHERE sensor LIKE '%" + sensor +"%' ORDER BY timestamp DESC Limit 1 ;")

    data = cursor.fetchall()
    if data is None:
        message = "There was no data by that time."
    elif ((data[0])[2]) > 20:
        message = "The airquality about PM2.5 is " + str((data[0])[2]) + " per cubic meters of microgram. Due to the serious air pollution, it is recommended that you should wear a mask."
    else:
        message = "The airquality about PM2.5 is " + str((data[0])[2]) + " per cubic meters of microgram."

    return statement(message)


@ask.intent("PowerIntent")
def ask_if_speaker(sensor):
    sensor = sensor
    cursor = mysql.connect().cursor()

    cursor.execute(
        "SELECT SUBSTRING(SUM(P/1000)/3600, 1, 3), SUBSTRING(FLOOR((SUM(P/1000)/3600)*1.63), 1, 1), SUBSTRING(121-(SUM(P/1000)/3600), 1, 3) FROM PDU WHERE 1;")

    data = cursor.fetchall()
    if data is None:
        message = "There was no data by that time."
    else:
        message = "Accumulated use of electricity in this month is " + str((data[0])[0]) + " kilowatt-hour. " \
                  "The price will be " + str((data[0])[1]) + " NT dollars, " \
                  "and it is still " + str((data[0])[2]) + " kilowatt-hour to the next stage of valuation."


    return statement(message)

if __name__ == '__main__':
    app.run(debug=True)
