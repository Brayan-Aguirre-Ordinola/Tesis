"---------------------------------IMPORTACION DE LIBRERIAS---------------------------------"
from CoolProp.CoolProp import PropsSI as cp
import matplotlib.pyplot as plt
import numpy as np
import math
import os
from datetime import datetime
import scipy.io
"-----------------------------EXTRACCION DE DATA DE VALIDACION-----------------------------"
"Funcion para extraer la data"
def data_val(name,n):
    n=3000
    # Cargar el archivo .mat
    data = scipy.io.loadmat(name)["P_eval_cal2"]
    tiempo = data[:n, 0]
    temp_eva = data[:n, 1]
    #pres_eva = data[:n, 2]
    T_room = data[:n, 3]
    return tiempo, temp_eva,T_room

tiempo_simulacion, temp_eva_real,T_room_real=data_val('data.mat', 3000) ##Modificar la temperatura del evaporador y corregir calidad

"------------------------------CONFIGURACION PARA VALIDACION-------------------------------"
dt=int(tiempo_simulacion[1]-tiempo_simulacion[0])             #s
tfinal_horas=len(tiempo_simulacion)*dt/3600     #horas
tsalto_minutos=0    #min
mass_fruit=0        #kg
diff_ave=8.8        #°C

"----------------------------------CONDICIONES INICIALES-----------------------------------"
T_amb_inicial=28.4    #°C
T_room_inicial=25   #°C
T_fruit_inicial=T_room_real[0]  #°C

"----------------------------------VALORES PARA CALIBRAR-----------------------------------"
U_amb=2.8
U_fruta=10
"----------------------------------------FUNCIONES-----------------------------------------"

"Area superficial en función de la masa del mango"
def fruit_area(mass_fruit):  #mass_fruit en kg
    peso_mango= 0.5          #kg
    densidad_mango = 1100    #kg/m^3
    NuMangos=int(mass_fruit/peso_mango) #Numero de Mangos
    factor_correccion = 0.7  
    #Factor de corrección por contacto entre mangos y resistencia térmica de la caja"
    volumen_mango = peso_mango / densidad_mango                             # m^3
    radio_mango = (3 * volumen_mango / (4 * math.pi)) ** (1 / 3)            # m
    area_superficial_mango = 4 * math.pi * radio_mango ** 2                 # m^2
    area_superficial_total = area_superficial_mango * NuMangos              # m^2
    area_superficial_efectiva = factor_correccion * area_superficial_total  # m^2
    return area_superficial_efectiva

"Calor de Conveccion de la fruta"
def Conv_fruit_room(T_fruit,T_room):
    U=97.595 #W/K
    SA_fruit=fruit_area(mass_fruit)#m^2
    if (mass_fruit<=0):
        return 0 #En caso de que la cámara esté vacía, la convección sera de 0
    else:
        return U_fruta*SA_fruit*(T_fruit-T_room)

"Calor de Conveccion del ambiente a la cámara"
def Conv_amb_room(T_amb,T_room):
    U=6.0594 #W/K
    SA_room=2*(height*width+length*height)+length*width#m^2
    return U_amb*SA_room*(T_amb-T_room)

"Calor de Conveccion del ventilador"
Conv_fan=100#W

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

"Función que calcula el calor en el evaporador"
def Q_dot_evaporador(T_e,T_c):
    W_comp=2e3  #W
    eta_is=0.75  #-
    q_e=1       #-
    q_c=0.1     #-
    h_1=cp('H','T', T_e,'Q',q_e,'R134A') #J/kg      #entalpía a la salida del evaporador
    h_2=cp('H','T', T_c,'Q',q_c,'R134A') #J/kg      #entalpía a la salida del condensador
    s_e=cp('S','T', T_e,'Q',q_e,'R134A') #J/kg-K    #entropía a la entrada del compresor
    h_3=cp('H','T', T_c,'S',s_e,'R134A') #J/kg      #entalpía del proceso de compresión isoentrópica
    return W_comp*eta_is*((h_1-h_2)/(h_3-h_1))

"---------------------------------CONFIGURACION ADICIONAL----------------------------------"
# Propiedades de la camara de refrigeracion
height=2.2; width=4.2; length=3.8 #All units in m
v_room=height*width*length      #m^3
P_air=101325                    #Pa

# Pasar los tiempos a unidades estándar
tfinal=int(tfinal_horas*3600-1)   #sec
n=int(tfinal/dt+1)              #numero de elementos para Array
tsalto=tsalto_minutos*60        #sec

# Crear los arrays
tiempo=np.zeros(n)
variables_T=["T_room","T_fruit","T_amb","T_eva","T_cond"]
data_T={i:np.zeros(n) for i in variables_T}
variables_Q=["Qfruit","Qfan","Qamb_room","Qcool"]
data_Q={i:np.zeros(n) for i in variables_Q}

##definicion del tiempo y el salto:
tiempo = np.linspace(0, tfinal, int(tfinal/dt)+1)
data_T["T_eva"]=temp_eva_real+273.15-20

"--------------------------CONFIGURACION DE CONDICIONES INICIALES--------------------------"
tiempo[0]=0
data_T["T_amb"][0]=T_amb_inicial+273.15#K
data_T["T_room"][0]=T_room_inicial+273.15#K
data_T["T_fruit"][0]=T_fruit_inicial+273.15#K
data_T["T_cond"][0]=data_T["T_amb"][0]+diff_ave;

"-------------------------------------BUCLE PRINCIPAL--------------------------------------"
for i in range(dt,tfinal+dt,dt):
    j=int(i/dt) # ubicación del dato
    #Se calculan los calores:
    data_Q["Qfruit"][j]=(Conv_fruit_room(data_T["T_fruit"][j-1],data_T["T_room"][j-1]))
    data_Q["Qamb_room"][j]=(Conv_amb_room(data_T["T_amb"][j-1],data_T["T_room"][j-1]))
    data_Q["Qfan"][j]=(Conv_fan)
    data_Q["Qcool"][j]=Q_dot_evaporador(data_T["T_eva"][j-1],data_T["T_cond"][j-1])
   
    #Se calculan las nuevas temperaturas:
    data_T["T_room"][j]=(Id_T_room(data_Q["Qfruit"][j-1],data_Q["Qfan"][j-1],
                                   data_Q["Qamb_room"][j-1],data_Q["Qcool"][j-1],
                                   data_T["T_room"][j-1],tiempo[j-1]))
    if (mass_fruit>0):
        data_T["T_fruit"][j]=(Id_T_fruit(data_Q["Qfruit"][j-1],data_T["T_fruit"][j-1],
                                         tiempo[j-1]))
    data_T["T_amb"][j]=data_T["T_amb"][j-1]
    data_T["T_cond"][j]=data_T["T_amb"][j-1]+diff_ave
    
"----------------------------------GRAFICAS DE SIMULACION----------------------------------"

plt.close('all')    #Se cierran las gráficas existentes

if (mass_fruit<=0):
    n_plots=2
else:
    n_plots=3
fig, axs = plt.subplots(n_plots, 1, sharex=True, figsize=(7, 7))

axs[0].plot(tiempo/60, data_T["T_eva"]-273.15, 'r')
axs[0].set_title('Temp. a la salida del evaporador')
axs[0].set_ylabel('[°C]')
axs[0].grid(True) 

# Segundo gráfico
axs[1].plot(tiempo/60, data_T["T_room"]-273.15, 'g')
axs[1].set_title('Temp. habitacion')
axs[1].set_ylabel('[°C]')
axs[1].grid(True) 
axs[1].set_ylim(np.min(data_T["T_room"])-274.15, data_T["T_room"][0]-272.15)
if (n_plots==3):
# Tercer gráfico
    axs[2].plot(tiempo/60, data_T["T_fruit"]-273.15, 'b')
    axs[2].set_title('Temp. fruta')
    axs[2].set_xlabel('Tiempo [min]')
    axs[2].set_ylabel('[°C]')
    axs[2].grid(True) 
    axs[2].set_ylim(np.min(data_T["T_fruit"])-274.15, data_T["T_fruit"][0]-272.15)

fig.suptitle('Resultados de Simulación')
plt.show()

"------------------------------------GUARDAR EL ARCHIVO------------------------------------"
# Se crea una carpeta y se guarda el archivo
current_time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
folder_name = f'Intento_val_{current_time}'
os.makedirs(folder_name)
plot_path = os.path.join(folder_name, 'ResultadoDeSimulacion.png')
fig.savefig(plot_path)

# Crear archivo txt para guardar las variables a, b y c
txt_path = os.path.join(folder_name, 'DatosDeSimulacion.txt')
with open(txt_path, 'w') as f:
    f.write(f'Tiempo de simulación : {tfinal_horas} horas.\n')
    f.write(f'Tiempo de muestreo : {dt} segundos.\n')
    #f.write(f'Temperatura del evaporador a la salida: {Te_value-273.15} °C \n')
    f.write('Condiciones Iniciales de Simulación: \n')
    f.write(f'Temperatura ambiente : {T_amb_inicial} °C \n')
    f.write(f'Temperatura de la cámara : {T_room_inicial} °C \n')
    f.write(f'Temperatura de la fruta : {T_fruit_inicial} °C \n')
    f.write(f'Temperatura del condensador : {tfinal_horas} °C \n')
    f.write('Valores de Constantes variables: \n')
    f.write(f'U del ambiente : {U_amb} °C \n')
    f.write(f'U del ambiente : {U_fruta} °C \n')
    f.write(f'Q ventilador : {Conv_fan} °C \n')
    