# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 15:15:40 2021

@author: kcnab
"""

import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters

Ts = 0.1 # Sampling Time
Tstop = 500 # End of Simulation Time
N = int(Tstop/Ts) # Simulation length

# Initialization of vectors

T_out_p = 22 # Initial Vaue
t_array = np.zeros(N+1) # Initialization of e vector
u_array = np.zeros(N+1) # Initialization of u vector
T_array = np.zeros(N+1)
Tenv = 21.5
up = 0
ep=0

tempr = Tenv
yf_prev = Tenv

def Air_Heater(U):
    
    #Model Parameters
    Kh = 3.5
    theta_t = 22
      
    T_out = T_out_p + Ts*(1/theta_t*(-T_out_p + Kh * U + Tenv));
    return T_out;
    
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


# Simulation
for k in range(N+1):
    
   t_k = k*Ts
   
   T_k = Air_Heater(up)
   T_out_p = T_k
   
   temp_f = LP_filter(T_k)
   yf_prev = temp_f
   
   u_k=PID(temp_f)
   up = u_k

   t_array[k] = t_k
   u_array[k] = u_k
   T_array[k] = T_k
    
   
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
    