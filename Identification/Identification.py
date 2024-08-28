from scipy import signal
from scipy import io
import numpy as np
import matplotlib.pyplot as plt

# Cargar el archivo .mat
datos = io.loadmat('data.mat')
tiempo = datos['tiempo']
u = datos['u']
y = datos['y']

u1 = signal.detrend(u,0,type = 'constant')
y1 = signal.detrend(y,0,type = 'constant')

plt.figure()
plt.plot(tiempo,u, label='Señal con tendencia')
plt.plot(tiempo,u1, label='Señal sin tendencia')
plt.legend()
plt.title('Eliminación de Tendencia con scipy.signal.detrend')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.grid(True)
plt.show()

plt.figure()
plt.plot(tiempo,y, label='Señal con tendencia')
plt.plot(tiempo,y1, label='Señal sin tendencia')
plt.legend()
plt.title('Eliminación de Tendencia con scipy.signal.detrend')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.grid(True)
plt.show()