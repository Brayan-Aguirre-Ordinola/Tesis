import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Definir la función de transferencia continua
num = [1]   # Numerador
den = [1, 3, 2]  # Denominador
sistema_continuo = signal.TransferFunction(num, den)

# Definir el tiempo de muestreo
Ts = 0.5  # Tiempo de muestreo

# Convertir a sistema discreto usando el método Tustin
sistema_discreto = signal.cont2discrete((sistema_continuo.num, sistema_continuo.den), Ts, method='bilinear')

# Extraer numerador y denominador del sistema discreto
num_discreto, den_discreto, dt = sistema_discreto

# Aplicar un escalón al sistema discreto
t, y = signal.dstep((num_discreto, den_discreto, dt))

# Convertir los arrays de salida a una forma manejable
t = np.squeeze(t)  # Eliminar dimensiones innecesarias
y = np.squeeze(y)  # Eliminar dimensiones innecesarias

# Graficar la respuesta escalón del sistema discreto
plt.stem(t, y, use_line_collection=True)
plt.title("Respuesta Escalón del Sistema Discreto")
plt.xlabel("Tiempo [n*T_s]")
plt.ylabel("Salida")
plt.grid(True)
plt.show()

