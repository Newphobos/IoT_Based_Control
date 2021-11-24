# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 15:32:34 2021

@author: kcnab
"""

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import database
import pyodbc
import random

# MQTT details
brokerAddress = "826eea61073a42b7a79b6b4633c6169b.s2.eu.hivemq.cloud"
userName = "Temp_data"
passWord = "Newphobos4654@"
topic = "AirHeater/tem_C"

client = mqtt.Client()
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(userName, passWord)
client.connect(brokerAddress, 8883)

#database connection strings
connectionString = database.GetConnectionString()
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()


value = 0
wait = 1

def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))
        
def on_message(client, userdata, msg):
    global value
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    value = msg.payload.decode("utf-8")

while True:
    # now = datetime.now()
    # datetimeformat = "%Y-%m-%d %H:%M:%S"
    #measurementDateTime = now.strftime(datetimeformat)
    measurementDateTime = datetime.now()
   
    #query = "INSERT INTO MEASUREMENT_DATA(TimeStamp,MeasurementValue,SensorId) VALUES(measurementDateTime,value,random.randint(1,20))"
    query = "INSERT INTO MEASUREMENT_DATA(TimeStamp,MeasurementValue,SensorId) VALUES(measurementDateTime,value,random.randint(1,20))"
    cursor.execute(query)
    cursor.commit()
    client.on_connect = on_connect
    client.on_message = on_message  
    client.subscribe(topic)

#client.loop_forever()


