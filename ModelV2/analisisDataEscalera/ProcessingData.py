"---------------------------------IMPORTACION DE LIBRERIAS---------------------------------"
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI as cp

"------------------------------LECTURA Y ASIGNACION DE DATOS-------------------------------"
data = scipy.io.loadmat("data.mat")["data"]
n=int(27e3)
if n>len(data):
    n=len(data)

variables_U=["Frec_compresor","Pot_compresor"]
data_U={i:np.zeros(n) for i in variables_U}
variables_T=["T_room","T_amb","T_evap","T_cond","T_entrada_compresor","T_salida_compresor"]
data_T={i:np.zeros(n) for i in variables_T}
variables_P=["P_entrada_compresor","P_salida_compresor"]
data_P={i:np.zeros(n) for i in variables_P}

tiempo = data[:n, 0]
data_U["Frec_compresor"] = data[:n, 1]
data_U["Pot_compresor"] = data[:n, 2]
data_T["T_room"] = data[:n, 3]
data_T["T_amb"] = data[:n, 4]
data_T["T_evap"] = data[:n, 5]
#data_T["T_sh"] = data[:n, 6]
data_T["T_entrada_compresor"] = data[:n, 7]
data_T["T_salida_compresor"] = data[:n, 8]
data_T["T_cond"] = data[:n, 9]
data_P["P_entrada_compresor"] = data[:n, 10]
data_P["P_salida_compresor"] = data[:n, 11]
plt.close('all')
"""
"-----------------------------------GRAFICAS ESENCIALES------------------------------------"
plt.figure(figsize=(10, 6))
for i, (key, data) in enumerate(data_U.items(), 1):
    plt.subplot(2, 1, i)  
    plt.plot(tiempo[1:], data[1:]) 
    plt.title(f'{key}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Tasa de Calor (W)')
    plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
for i, (key, data) in enumerate(data_T.items(), 1):
    plt.subplot(3, 2, i)
    plt.plot(tiempo[1:], data[1:])  
    plt.title(f'{key}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
plt.tight_layout()  
plt.show()

plt.figure(figsize=(10, 6))
for i, (key, data) in enumerate(data_P.items(), 1):
    plt.subplot(2, 1, i)
    plt.plot(tiempo[1:], data[1:])
    plt.title(f'{key}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Presión (bar)')
    plt.grid(True)
plt.tight_layout()
plt.show()


"------------------------------------ANALISIS POSTERIOR------------------------------------"
"Relación entre la temperatura del condensador y la temperatura ambiente"
diff_temperatura=data_T["T_cond"]-data_T["T_amb"]
diferencia_media=sum(diff_temperatura)/len(diff_temperatura)
plt.figure(figsize=(10, 6))  
plt.plot(tiempo/60,diff_temperatura)
plt.title('Diferencia de temperatura ambiente y en el condensador')
plt.xlabel('Tiempo (min)')
plt.ylabel('Delta temp. (°C)')
plt.grid(True)
plt.tight_layout()  
plt.show()

"Relacionde compresion"
beta_compresion=resultado = [x / y for x, y 
                             in zip(data_P["P_salida_compresor"], data_P["P_entrada_compresor"])]
plt.figure(figsize=(10, 6))  
plt.plot(tiempo/60,beta_compresion)
plt.title('Relación de compresión')
plt.xlabel('Tiempo (min)')
plt.ylabel('Beta (-)')
plt.grid(True)
plt.tight_layout()  
plt.show()

"Entalpía a la entrada del compresor"
h_entrada_compresion=resultado = [cp('H','T',x+273.15,'P',y*1e5,'R134A')/1000 for x, y 
                             in zip(data_T["T_entrada_compresor"], data_P["P_entrada_compresor"])]

plt.figure(figsize=(10, 6))
plt.plot(tiempo/60,h_entrada_compresion)
plt.title('Entalpía a la entrada del compresor')
plt.xlabel('Tiempo (min)')
plt.ylabel('Entalpía (kJ/kg)')
plt.grid(True)
plt.tight_layout()  

"Entalpía a la salida del compresor"
h_salida_compresion=resultado = [cp('H','T',x+273.15,'P',y*1e5,'R134A')/1000 for x, y 
                             in zip(data_T["T_salida_compresor"], data_P["P_salida_compresor"])]

plt.figure(figsize=(10, 6))
plt.plot(tiempo/60,h_salida_compresion)
plt.title('Entalpía a la salida del compresor')
plt.xlabel('Tiempo (min)')
plt.ylabel('Entalpía (kJ/kg)')
plt.grid(True)
plt.tight_layout() 
plt.legend() 


"Entalpía adquirida en el compresor"
h_ganada = [h_salida_compresion[i] - h_entrada_compresion[i] for i in range(len(h_entrada_compresion))]

# Crear el gráfico
plt.plot(tiempo/60,h_ganada, label='Entalpía', color='blue')
plt.plot(tiempo/60,data_U["Pot_compresor"], label='Potencia del compresor', color='red')
plt.title('Entalpía ganada en el compresor')
plt.xlabel('tiempo')
plt.ylabel('Entalpía [KJ/Kg]')
plt.grid(True)
plt.legend()
plt.show()

"Entalpía a la salida del evaporador"
h_salida_compresion=resultado = [cp('H','T',x+273.15,'P',y*1e5,'R134A')/1000 for x, y 
                             in zip(data_T["T_evap"], data_P["P_entrada_compresor"])]
plt.figure(figsize=(10, 6))
plt.plot(tiempo/60,h_salida_compresion)
plt.title('Entalpía a la salida del evaporador')
plt.xlabel('Tiempo (min)')
plt.ylabel('Entalpía (kJ/kg)')
plt.grid(True)
plt.tight_layout()  
plt.show()

"Entalpía a la entrada del condensador"
h_entrada_compresion=resultado = [cp('H','T',x+273.15,'P',y*1e5,'R134A')/1000 for x, y 
                             in zip(data_T["T_cond"], data_P["P_salida_compresor"])]
plt.figure(figsize=(10, 6))
plt.plot(tiempo/60,h_entrada_compresion)
plt.title('Entalpía a la entrada del condensador')
plt.xlabel('Tiempo (min)')
plt.ylabel('Entalpía (kJ/kg)')
plt.grid(True)
plt.tight_layout()  
plt.show()
"""