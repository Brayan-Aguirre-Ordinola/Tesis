from CoolProp.CoolProp import PropsSI as cp
from Integration import integracion
from Integration import dt
import matplotlib.pyplot as plt
import numpy as np

" Configuracion Inicial del Simulador"
tfinal_horas=24#horas
tfinal=int(tfinal_horas*3600)#sec
n=int(tfinal/dt+1)#numero de elementos para Array
tsalto_minutos=60#min
tsalto=tsalto_minutos*60#sec
Qcool_value=50#W

## Propiedades de la camara de refrigeracion
height=2.3#m
width=4.4#m
length=4#m
v_room=height*width*length#m^3
#v_fruta=1#m - "Valor no usado"
SA_room=2*(height*width+length*height)+length*width#m^2
P_air=101325#Pa
U_room= 10  # W/K

## Propiedades de la fruta
#densidad=1100#kg/m^3
masa=200#densidad*v_fruta (kg)
c_p=1950#J/kg-K
SA_fruit=  #m^2
U_fruit=15   # W/K
"Calor de Conveccion de la fruta"
def Conv_fruit_room(T_fruit,T_room):
    return U_room*SA_room*(T_fruit-T_room)
  
"Calor de Conveccion del ambiente a la cámara"
def Conv_amb_room(T_amb,T_room):
    return U_fruit*SA_fruit*(T_amb-T_room)

"Calor de Conveccion del ventilador"
Conv_fan=5 #W

"Funcion que calcula la nueva temperatura del room"
def Id_T_room(Q_fruit,Q_fan,Q_room,Q_cool,T_room,tiempo):
    densidad=cp('D', 'T', T_room, 'P', P_air, 'Air')#kg/m^3
    masa=densidad*v_room#kg
    c_p=cp('C', 'T', T_room, 'P', P_air, 'Air')#J/kg-K
    def d_T_room(T_room,tiempo):
        return (Q_fruit+Q_fan+Q_room-Q_cool)/(masa*c_p)
    return integracion(d_T_room,T_room,tiempo)

"Funcion que calcula la nueva temperatura de la fruta"
def Id_T_fruit(Q_fruit,T_fruit,tiempo):
    
    def d_T_fruit(T_fruit,tiempo):
        return (-Q_fruit)/(masa*c_p)
    return integracion(d_T_fruit,T_fruit,tiempo)

#Crear los arraysvariables_T = ["tiempo", "Troom", "Tfruit", "Tamb"]

tiempo=np.zeros(n)

variables_T = ["T_room", "T_fruit", "T_amb"]
data_T={i:np.zeros(n) for i in variables_T}

variables_Q = ["Qfruit", "Qfan", "Qamb_room", "Qcool"]
data_Q={i:np.zeros(n) for i in variables_Q}

# Condiciones iniciales de las variables
tiempo[0]=0
data_T["T_amb"][0]=300#K
"Temperaturas Dinámicas"
data_T["T_room"][0]=293#K
data_T["T_fruit"][0]=298#K

##definicion del tiempo y el salto:
tiempo = np.linspace(0, tfinal, int(tfinal/dt)+1)
data_Q["Qcool"]= np.where(tiempo >= tsalto, Qcool_value, 0)

for i in range(dt,tfinal+dt,dt):
    j=int(i/dt) # ubicación del dato
    #Se calculan los calores:
    data_Q["Qfruit"][j]=(Conv_fruit_room(data_T["T_fruit"][j-1],data_T["T_room"][j-1]))
    data_Q["Qamb_room"][j]=(Conv_amb_room(data_T["T_amb"][j-1],data_T["T_room"][j-1]))
    data_Q["Qfan"][j]=(Conv_fan)
   
    #Se calculan las nuevas temperaturas:
    data_T["T_room"][j]=(Id_T_room(data_Q["Qfruit"][j-1],data_Q["Qfan"][j-1],data_Q["Qamb_room"][j-1],data_Q["Qcool"][j-1],data_T["T_room"][j-1],tiempo[j-1]))
    data_T["T_fruit"][j]=(Id_T_fruit(data_Q["Qfruit"][j-1],data_T["T_fruit"][j-1],tiempo[j-1]))
    data_T["T_amb"][j]=data_T["T_amb"][j-1]

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
