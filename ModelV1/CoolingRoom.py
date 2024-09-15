"---------------------------------------IMPORTACION DE LIBRERIAS---------------------------------------"
from CoolProp.CoolProp import PropsSI as cp
import matplotlib.pyplot as plt
import numpy as np
import math

"---------------------------------------CONFIGURACION DEL SIMULADOR---------------------------------------"
tfinal_horas=3#horas
tsalto_minutos=0#min
Qcool_value=5500#W
mass_fruit=256#kg
dt=10#s
"---------------------------------------FUNCIONES---------------------------------------"
"Area superficial en función de la masa del mango"
def fruit_area(mass_fruit):  #mass_fruit en kg
    peso_mango= 0.5          #kg
    densidad_mango = 1100    #kg/m^3
    NuMangos=int(mass_fruit/peso_mango) 
    factor_correccion = 0.7  
    #Factor de corrección por contacto entre mangos y resistencia térmica de la caja"
    volumen_mango = peso_mango / densidad_mango                    # m^3
    radio_mango = (3 * volumen_mango / (4 * math.pi)) ** (1 / 3)   # m
    area_superficial_mango = 4 * math.pi * radio_mango ** 2        # m^2
    area_superficial_total = area_superficial_mango * NuMangos     # m^2
    area_superficial_efectiva = factor_correccion * area_superficial_total  # m^2
    return area_superficial_efectiva

"Calor de Conveccion de la fruta"
def Conv_fruit_room(T_fruit,T_room):
    U=97.595;
    SA_fruit=fruit_area(mass_fruit)#m^2
    return U*SA_fruit*(T_fruit-T_room)
  
"Calor de Conveccion del ambiente a la cámara"
def Conv_amb_room(T_amb,T_room):
    U=6.0594 # W/K
    SA_room=2*(height*width+length*height)+length*width#m^2
    return U*SA_room*(T_amb-T_room)

"Calor de Conveccion del ventilador"
Conv_fan=20#W

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
    #densidad=1100#kg/m^3
    c_p=1950#J/kg-K
    def d_T_fruit(T_fruit,tiempo):
        return (-Q_fruit)/(mass_fruit*c_p)
    return integracion(d_T_fruit,T_fruit,tiempo)

"Integracion por Runge Kutta"
def integracion (dy,y,x):
    k1=dy(y,x) 
    k2=dy(y+dt*k1/2,x+dt/2)
    k3=dy(y+dt*k2/2,x+dt/2)
    k4=dy(y+dt*k3,x+dt)
    return y+(k1+2*k2+2*k3+k4)*dt/6

"---------------------------------------CONFIG ADICIONAL---------------------------------------"
# Propiedades de la camara de refrigeracion
height=2.2; width=4.2; length=3.8 #All units in m
v_room=height*width*length#m^3
P_air=101325#Pa

# Pasar los tiempos a unidades estándar
tfinal=int(tfinal_horas*3600)#sec
n=int(tfinal/dt+1)#numero de elementos para Array
tsalto=tsalto_minutos*60#sec

# Crear los arrays
tiempo=np.zeros(n)
variables_T = ["T_room", "T_fruit", "T_amb"]
data_T={i:np.zeros(n) for i in variables_T}
variables_Q = ["Qfruit", "Qfan", "Qamb_room", "Qcool"]
data_Q={i:np.zeros(n) for i in variables_Q}

##definicion del tiempo y el salto:
tiempo = np.linspace(0, tfinal, int(tfinal/dt)+1)
data_Q["Qcool"]= np.where(tiempo >= tsalto, Qcool_value, 0)

"---------------------------------------CONDICIONES INICIALES---------------------------------------"
tiempo[0]=0
data_T["T_amb"][0]=273.15+27#K
data_T["T_room"][0]=273.15+25#K
data_T["T_fruit"][0]=273.15+25#K

"---------------------------------------BUCLE PRINCIPAL---------------------------------------"
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
    
"---------------------------------------GRAFICAS DE SIMULACION---------------------------------------"

#plt.close('all')    #Se cierran las gráficas existentes

fig, axs = plt.subplots(3, 1, sharex=True, figsize=(5, 6))

axs[0].plot(tiempo/60, data_Q["Qcool"]/1000, 'r')
axs[0].set_title('Q cool')
axs[0].set_ylabel('[kW]')
axs[0].grid(True) 
axs[0].set_ylim(0,Qcool_value*1.1/1000)

# Segundo gráfico
axs[1].plot(tiempo/60, data_T["T_room"]-273.15, 'g')
axs[1].set_title('Temp. habitacion')
axs[1].set_ylabel('[°C]')
axs[1].grid(True) 
axs[1].set_ylim(8, data_T["T_room"][0]-273.15+1)

# Tercer gráfico
axs[2].plot(tiempo/60, data_T["T_fruit"]-273.15, 'b')
axs[2].set_title('Temp. fruta')
axs[2].set_xlabel('Tiempo [min]')
axs[2].set_ylabel('[°C]')
axs[2].grid(True) 
axs[2].set_ylim(8, data_T["T_fruit"][0]-273.15+1)

fig.suptitle('Resultados de Simulación')
plt.show()