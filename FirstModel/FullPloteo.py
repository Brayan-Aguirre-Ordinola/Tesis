# Ploteo de todas las gráficas:
""" Posible código para ploteo de todas las gráficas:
# Plotear todas las gráficas de data_T en una distribución 2x2
plt.figure(figsize=(8, 6))  # Tamaño de la figura

for i, (key, data) in enumerate(data_T.items(), 1):
    plt.subplot(2, 2, i)  # Crear subplots en una cuadrícula de 2x2
    plt.plot(tiempo, data)
    plt.title(f'{key}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Temperatura (K)')
    plt.grid(True)

plt.tight_layout()  # Ajustar la disposición para evitar solapamientos
plt.show()

# Plotear todas las gráficas de data_Q en una distribución 2x2
plt.figure(figsize=(8, 6))  # Tamaño de la figura

for i, (key, data) in enumerate(data_Q.items(), 1):
    plt.subplot(2, 2, i)  # Crear subplots en una cuadrícula de 2x2
    plt.plot(tiempo[1:], data[1:])  # Omitir el primer valor de 'tiempo' que es 0
    plt.title(f'{key}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Tasa de Calor (W)')
    plt.grid(True)

plt.tight_layout()  # Ajustar la disposición para evitar solapamientos
plt.show()
"""