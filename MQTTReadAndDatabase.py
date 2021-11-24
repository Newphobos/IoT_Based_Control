import pyodbc
import time
from datetime import datetime
import database
import paho.mqtt.client as mqtt



# MQTT details
brokerAddress = "826eea61073a42b7a79b6b4633c6169b.s2.eu.hivemq.cloud"
userName = "Temp_data"
passWord = "Newphobos4654@"
topic = "AirHeater/tem_C"

client = mqtt.Client()
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(userName, passWord)
client.connect(brokerAddress, 8883)

# Connect to Database
connectionString = database.GetConnectionString()
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()

query = "INSERT INTO MEASUREMENT_DATA(TimeStamp,MeasurementValue,SensorId,Unit) VALUES(?,?,?,?)"



def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))
        
def on_message(client, userdata, msg):
    global value
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    value = msg.payload.decode("utf-8")
    now = datetime.now()
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    measurementDateTime = str(now.strftime(datetimeformat))
    
    # Insert Data into Database
    parameters = measurementDateTime,value,sensorId,unit1
    cursor.execute(query, parameters)
    cursor.commit()

sensorId = 1
unit1 = "degree C"
Ts = 1 # Sampling Time

client.on_connect = on_connect
client.on_message = on_message  
client.subscribe(topic)
# Wait
time.sleep(Ts)
    
client.loop_forever()
    