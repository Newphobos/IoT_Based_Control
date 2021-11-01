
import paho.mqtt.client as mqtt
import numpy as np
import matplotlib.pyplot as plt
import 
import nidaqmx
from nidaqmx.constants import TerminalConfiguration


#DAQ settings

task_ai = nidaqmx.Task()
task_ai.ai_channels.add_ai_voltage_chan("DAQAir/ai0",terminal_config=TerminalConfiguration.RSE)
task_ai.start()

task_ao = nidaqmx.Task()
task_ao.ao_channels.add_ao_voltage_chan("DAQAir/ao0",'mychannel',0,5)
task_ao.start()



# MQTT details
brokerAddress = "826eea61073a42b7a79b6b4633c6169b.s2.eu.hivemq.cloud"
userName = "Temp_data"
passWord = "Newphobos4654@"
topic = "AirHeater/tem_C"

# Simulation Parameters
wait = 5  # delay time of the loop
Ts = 0.1 # Sampling Time
Tstop = 500 # End of Simulation Time
N = int(Tstop/Ts) # Simulation length

# Initialization of vectors

T_out_p = 22 # Initial Vaue
t_array = np.zeros(N+1) # Initialization of e vector
u_array = np.zeros(N+1) # Initialization of u vector
T_array = np.zeros(N+1) # Array to store filter temperature
Tenv = 21.5
up = 0 
ep=0 

tempr = Tenv
yf_prev = Tenv



def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))

def Air_Heater_Real():
    
    ToutVolt = task_ai.read()
    if ToutVolt<1:
        ToutVolt = 1
    if ToutVolt>5:
        ToutVolt = 5
    return ToutVolt
    
def clip(u):
    if (u>5):
        u = 5
    if (u<0):
        u=0 
    return u

def PID(ym):
   #PI Controller Settings
    global ep
    
    kp = 0.5
    Ti = 5
    r = 25  # Setpoint temperature
    e = r - ym
    u = up + kp *(e - ep) + (kp/Ti)*Ts*e
    ep = e
    u = clip(u)
    
    task_ao.write(u)
    return u
    
def LP_filter(T):
    #filter parameters
    
    T_s = 0.1
    Tf= 5*T_s
    a = T_s/(Tf+T_s)
    
    y = T
    yf = (1-a)*yf_prev + a*y
    yf_pre = yf
    return yf

# function to convert voltage to degree celcius
def scaling(x,x1,x2,y1,y2):
    y = y1 + (x-x1)*(y2-y1)/(x2-x1)
    return y
    
# Create the client

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(userName, passWord)
client.connect(brokerAddress, 8883)


# Simulation
for k in range(4):
    
   t_k = k*Ts
   
   T_volt = Air_Heater_Real()
   T_degree = scaling(T_volt,1,5,0,50)
   
   temp_f = LP_filter(T_degree)
   yf_prev = temp_f
   
   u_k=PID(temp_f)
   up = u_k

   t_array[k] = t_k
   u_array[k] = u_k
   T_array[k] = temp_f
   
   data =str("{:.2f}".format(temp_f)) + " " + "deg C"
   client.publish(topic,data)
   
   time.sleep(wait)
   
# Plot Process Value
plt.figure(1)
plt.plot(t_array,T_array)
# Formatting the appearance of the Plot
plt.title('Control of Air Heater Model')
plt.xlabel('t [s]')
plt.ylabel('Tout')
plt.grid()
# Plot Control Signal
plt.figure(2)
plt.plot(t_array,u_array)
# Formatting the appearance of the Plot
plt.title('Control Signal')
plt.xlabel('t [s]')
plt.ylabel('u [V]')
plt.grid()
plt.show()
    