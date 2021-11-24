import pyodbc
import random
import time
from datetime import datetime
import database
# Connect to Database
connectionString = database.GetConnectionString()
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()
#query = "INSERT INTO MEASUREMENT_DATA (SensorName, MeasurementValue, MeasurementDateTime) VALUES (?,?,?)"
query = "INSERT INTO MEASUREMENT_DATA(TimeStamp,MeasurementValue,SensorId) VALUES(?,?,?)"

sensorId = 1
Ts = 10 # Sampling Time
N = 20
for k in range(N):
    # Generate Random Data
    LowLimit = 20
    UpperLimit = 25
    measurementValue = random.randint(LowLimit, UpperLimit)
    #Find Date and Time
    now = datetime.now()
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    measurementDateTime = str(now.strftime(datetimeformat))
    # Insert Data into Database
    parameters = measurementDateTime,measurementValue,sensorId
    cursor.execute(query, parameters)
    cursor.commit()
    # Wait
    time.sleep(Ts)
    