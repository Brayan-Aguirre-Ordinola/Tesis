import scipy.io
import numpy as np
import matplotlib.pyplot as plt

# Cargar el archivo .mat
datos = scipy.io.loadmat('data.mat')

# Imprimir las claves del archivo .mat para ver qué variables están disponibles
print(datos.keys())

# Supongamos que los datos están en una variable llamada 'data'
# Puedes acceder a ellos así:
data = datos['data']  # Reemplaza 'data' con el nombre real de la variable en tu archivo .mat

# Imprimir las primeras filas de los datos para inspeccionar
print(data)

# Suponiendo que 'data' tiene dos columnas: tiempo y señal
# Puedes separar las columnas de la siguiente manera:
tiempo = data[:, 0]  # Primera columna (ej. tiempo)
senal = data[:, 1]   # Segunda columna (ej. señal)

# Graficar la señal
plt.plot(tiempo, senal)
plt.title('Señal Importada del Archivo .mat')
plt.xlabel('Tiempo')
plt.ylabel('Señal')
plt.grid(True)
plt.show()
