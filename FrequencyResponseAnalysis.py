import math
import numpy as np
import matplotlib.pyplot as plt
import control


#process parameters
Kh = 3.5
theta_t = 22
theta_d = 2

#Transfer function of the process
num_p = np.array([Kh])
den_p = np.array([theta_t,1])
Hp1 = control.tf(num_p,den_p)
print ('Hp1(s) =', Hp1)

#Transfer function PI controller
Kp = 0.52
Ti = 18
num_c = np.array([Kp*Ti,Kp])
den_c = np.array([Ti,0])
Hc = control.tf(num_c,den_c)
print ('Hc(s) =', Hc)

# Transfer Function Lowpass Filter
Tf = 1
num_f = np.array ([1])
den_f = np.array ([Tf , 1])
Hf = control.tf(num_f , den_f)
print ('Hf(s) =', Hf)


# The Loop Transfer function
L = control.series(Hc, Hp1, Hf)
print ('L(s) =', L)


#Tracking transfer function

T = control.feedback(L,1)
print('T(s) = ',T)

# Calculating stability margins and crossover frequencies
gm , pm , w180 , wc = control.margin(L)
# Convert gm to Decibel
gmdb = 20 * np.log10(gm)
print("wc =", f'{wc:.2f}', "rad/s")
print("w180 =", f'{w180:.2f}', "rad/s")
print("GM =", f'{gm:.2f}')
print("GM =", f'{gmdb:.2f}', "dB")
print("PM =", f'{pm:.2f}', "deg")
# Find when System is Marginally Stable (Kritical Gain -Kc)
Kc = Kp*gm
print("Kc =", f'{Kc:.2f}')

# Bode Diagram with Stability Margins
plt.figure(1)
control.bode(L, dB=True, deg=True, margins=True) 


#Poles and Zeros
plt.figure(2)
control.pzmap(T)
p = control.pole(T)
z = control.zero(T)
print("poles = ",p)
