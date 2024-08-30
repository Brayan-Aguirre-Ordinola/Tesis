from CoolProp.CoolProp import PropsSI as cp
from Integration import integracion
from Integration import dt
import matplotlib.pyplot as plt
import numpy as np

"__Configuracion General del Simulador__"
tfinal_horas=12#horas
tsalto_minutos=180#min
Qcool_value=50#W
mass_fruit=50#kg

## Propiedades de la camara de refrigeracion
height=2.3#m
width=4.4#m
length=4#m
v_room=height*width*length#m^3
#v_fruta=1#m - "Valor no usado"
SA_room=2*(height*width+length*height)+length*width#m^2
P_air=101325#Pa

"Calor de Conveccion de la fruta"
def Conv_fruit_room(T_fruit,T_room):
    U=100;
    SA_fruit= 1#m^2
    return U*SA_fruit*(T_fruit-T_room)
  
"Calor de Conveccion del ambiente a la cámara"
def Conv_amb_room(T_amb,T_room):
    U=10 # W/K
    return U*(T_amb-T_room)

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
    #densidad=1100#kg/m^3
    c_p=1950#J/kg-K
    def d_T_fruit(T_fruit,tiempo):
        return (-Q_fruit)/(mass_fruit*c_p)
    return integracion(d_T_fruit,T_fruit,tiempo)

"__Configuracion Adicional__"
#Pasar los tiempos a unidades estándar
tfinal=int(tfinal_horas*3600)#sec
n=int(tfinal/dt+1)#numero de elementos para Array
tsalto=tsalto_minutos*60#sec

#Crear los arrays variables_T = ["tiempo", "Troom", "Tfruit", "Tamb"]
tiempo=np.zeros(n)
variables_T = ["T_room", "T_fruit", "T_amb"]
data_T={i:np.zeros(n) for i in variables_T}
variables_Q = ["Qfruit", "Qfan", "Qamb_room", "Qcool"]
data_Q={i:np.zeros(n) for i in variables_Q}

"__Condiciones iniciales de las variables__"
tiempo[0]=0
data_T["T_amb"][0]=300#K
"Temperaturas Dinámicas"
data_T["T_room"][0]=293#K
data_T["T_fruit"][0]=298#K

##definicion del tiempo y el salto:
tiempo = np.linspace(0, tfinal, int(tfinal/dt)+1)
data_Q["Qcool"]= np.where(tiempo >= tsalto, Qcool_value, 0)

"__Bucle Principal__"
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
    
"__Graficas de la simulacion__"

plt.close('all')

fig, axs = plt.subplots(3, 1, sharex=True, figsize=(6, 6))

axs[0].plot(tiempo/60, data_Q["Qcool"], 'r')
axs[0].set_title('u')
axs[0].set_ylabel('Q cool [W]')
axs[0].grid(True) 
axs[0].set_ylim(0,60)


# Segundo gráfico
axs[1].plot(tiempo/60, data_T["T_room"]-273, 'g')
axs[1].set_title('y1')
axs[1].set_ylabel('Temp. habitacion [K]')
axs[1].grid(True) 
#axs[1].set_ylim(-2, 2)

# Tercer gráfico
axs[2].plot(tiempo/60, data_T["T_fruit"]-273, 'b')
axs[2].set_title('y2')
axs[2].set_xlabel('Tiempo [min]')
axs[2].set_ylabel('Temp. fruta [K]')
axs[2].grid(True) 

fig.suptitle('Resultados de Simulación')
plt.show()





