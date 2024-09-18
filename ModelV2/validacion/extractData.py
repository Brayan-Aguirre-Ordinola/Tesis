import scipy.io
import numpy as np
import matplotlib.pyplot as plt
def data_val(name,n):
    n=3000
    # Cargar el archivo .mat
    data = scipy.io.loadmat(name)["P_eval_cal2"]
    tiempo = data[:n, 0]
    temp_eva = data[:n, 1]
    #pres_eva = data[:n, 2]
    T_room = data[:n, 3]
    return tiempo, temp_eva,T_room
tiempo, temp_eva,T_room=data_val('data.mat', 3000)
# Crear dos subplots que compartan el eje X
fig, ax1 = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

# Primera gráfica: Tiempo vs Temperatura del evaporador
ax1[0].plot(tiempo, temp_eva, label='Temperatura del evaporador', color='b')
ax1[0].set_ylabel('Temperatura (°C)')
ax1[0].set_title('Tiempo vs Temperatura y Presión del Evaporador')
ax1[0].legend()
ax1[0].grid(True)

# Segunda gráfica: Tiempo vs Presión del evaporador
ax1[1].plot(tiempo, T_room, label='Temperatura del room', color='g')
ax1[1].set_xlabel('Tiempo (s)')
ax1[1].set_ylabel('Temperatura (°C)')
ax1[1].legend()
ax1[1].grid(True)

# Mostrar la gráfica
plt.tight_layout()  # Ajustar los subplots para que no se solapen
plt.show()