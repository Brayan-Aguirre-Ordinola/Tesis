"---------------------------------IMPORTACION DE LIBRERIAS---------------------------------"
from CoolProp.CoolProp import PropsSI as cp
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.io
import time

"------------------------------LECTURA Y ASIGNACION DE DATOS-------------------------------"
data = scipy.io.loadmat("data.mat")["data"]
n=int(26e3) #Número de Datos
#Protección contra sobretiempos
if n>len(data):
    n=len(data)
#Creación de Diccionarios
variables_U=["Pot_compresor"]
data_U={i:np.zeros(n) for i in variables_U}
variables_T=["T_room","T_amb","T_evap","T_cond","T_fruit"]
data_T={i:np.zeros(n) for i in variables_T}
variables_Q=["Qfruit","Qfan","Qamb_room","Qcool"]
data_Q={i:np.zeros(n) for i in variables_Q}
#Asignación de Datos
tiempo = data[:n, 0]
data_U["Pot_compresor_real"] = data[:n, 2]
data_T["T_room_real"] = data[:n, 3]
#Ajuste de temperaturas para ser usadas por CoolProp
data_T["T_evap"]=np.array([T+273.15 for T in data[:n, 5]])
data_T["T_amb"]=np.array([T+273.15 for T in data[:n, 4]])
data_T["T_cond"]=np.array([T+273.15 for T in data[:n, 9]])

"------------------------------CONFIGURACION PARA VALIDACION-------------------------------"
dt=int(tiempo[1]-tiempo[0])#s
mass_fruit=0 #kg
U_fruta=10 #No necesario

"----------------------------------VALORES PARA CALIBRAR-----------------------------------"
U_amb=0.5
Conv_fan=390
eta_is=0.09 
q_e=0.8    
q_c=0.1
refrigerant='R134A'
"-----------------------------------FUNCIONES GENERALES------------------------------------"
"Integracion por Runge Kutta"
def integracion (dy,y,x):
    k1=dy(y,x) 
    k2=dy(y+dt*k1/2,x+dt/2)
    k3=dy(y+dt*k2/2,x+dt/2)
    k4=dy(y+dt*k3,x+dt)
    return y+(k1+2*k2+2*k3+k4)*dt/6

"Area superficial en función de la masa del mango"
def fruit_area(mass_fruit):  #mass_fruit en kg
    peso_mango= 0.5          #kg
    densidad_mango = 1100    #kg/m^3
    NuMangos=int(mass_fruit/peso_mango) #Numero de Mangos
    factor_correccion = 0.7  
    #Factor de corrección por contacto entre mangos y resistencia térmica de la caja
    volumen_mango = peso_mango / densidad_mango                             # m^3
    radio_mango = (3 * volumen_mango / (4 * math.pi)) ** (1 / 3)            # m
    area_superficial_mango = 4 * math.pi * radio_mango ** 2                 # m^2
    area_superficial_total = area_superficial_mango * NuMangos              # m^2
    area_superficial_efectiva = factor_correccion * area_superficial_total  # m^2
    return area_superficial_efectiva

"Funcion de métricas"
def metricas(y_real, y_pred):
    # Asegurarse que las series tengan la misma longitud
    assert len(y_real) == len(y_pred), "Las series deben tener la misma longitud"
    # Error de predicción final (FPE)
    e = len(y_real)
    fpe = np.var(y_real - y_pred) * (e + 1) / (e - 1)
    # Error cuadrático medio (MSE)
    mse = np.mean((y_real - y_pred)**2)
    # Porcentaje de ajuste (FIT)
    fit = 100 * (1 - np.linalg.norm(y_real - y_pred) / np.linalg.norm(y_real - np.mean(y_real)))
    return fpe, mse, fit
"------------------------------------FUNCIONES DE CALOR------------------------------------"
"Calor de Convección de la fruta"
def Conv_fruit_room(T_fruit,T_room):
    #U=97.595 #W/K
    SA_fruit=fruit_area(mass_fruit)#m^2
    if (mass_fruit<=0):
        return 0 #En caso de que la cámara esté vacía, la convección sera de 0
    else:
        return U_fruta*SA_fruit*(T_fruit-T_room)

"Calor de Convección del ambiente a la cámara"
def Conv_amb_room(T_amb,T_room):
    #U=6.0594 #W/K
    SA_room=2*(height*width+length*height)+length*width#m^2
    return U_amb*SA_room*(T_amb-T_room)

"Potencia en el compresor"
def Pot_compresor(T_e,T_c):
    P_oe=('P','T', T_e,'Q',0,refrigerant)#Pa
    P_ic=('P','T', T_c,'Q',0,refrigerant)#Pa
    return P_oe,P_ic

"Calor en el evaporador"
def Q_dot_evaporador(W_comp,T_e,T_c):
    h_1=cp('H','T', T_e,'Q',q_e,refrigerant) #J/kg      #entalpía a la salida del evaporador
    h_2=cp('H','T', T_c,'Q',q_c,refrigerant) #J/kg      #entalpía a la salida del condensador
    s_e=cp('S','T', T_e,'Q',q_e,refrigerant) #J/kg-K    #entropía a la entrada del compresor
    h_3=cp('H','T', T_c,'S',s_e,refrigerant) #J/kg      #entalpía del proceso de compresión isoentrópica
    return W_comp*eta_is*((h_1-h_2)/(h_3-h_1))

"Calor de Convección del ventilador"
#Conv_fan=400#W

"---------------------------FUNCIONES DE CÁLCULO DE TEMPERATURAS---------------------------"
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

"---------------------------------CONFIGURACION ADICIONAL----------------------------------"
# Propiedades de la camara de refrigeracion
height=2.2; width=4.2; length=3.8 #All units in m
v_room=height*width*length#m^3
P_air=101325#Pa

# Pasar los tiempos a unidades estándar
tfinal=int(tiempo[-1])   #sec
n=int(tfinal/dt+1) #numero de elementos para Array

"--------------------------CONFIGURACION DE CONDICIONES INICIALES--------------------------"
tiempo[0]=1
data_T["T_room"][0]=data_T["T_room_real"][0]+273.15#K
data_T["T_fruit"][0]=0+273.15#K

"-------------------------------------BUCLE PRINCIPAL--------------------------------------"
def simulacion(U_amb,Conv_fan,eta_is,q_e,q_c):
    start_time = time.time()
    for i in range(dt,tfinal,dt):
        j=int(i/dt) # ubicación del dato
        #Se calculan los calores:
        if (mass_fruit>=0):
            data_Q["Qfruit"][j-1]=(Conv_fruit_room(data_T["T_fruit"][j-1],data_T["T_room"][j-1]))
        data_Q["Qamb_room"][j-1]=(Conv_amb_room(data_T["T_amb"][j-1],data_T["T_room"][j-1]))
        data_Q["Qfan"][j-1]=(Conv_fan)
        data_Q["Qcool"][j-1]=Q_dot_evaporador(data_U["Pot_compresor_real"][j-1]*1000,data_T["T_evap"][j-1],data_T["T_cond"][j-1])
       
        #Se calculan las nuevas temperaturas:
        data_T["T_room"][j]=(Id_T_room(data_Q["Qfruit"][j-1],data_Q["Qfan"][j-1],
                                       data_Q["Qamb_room"][j-1],data_Q["Qcool"][j-1],
                                       data_T["T_room"][j-1],tiempo[j-1]))
        if (mass_fruit>0):
            data_T["T_fruit"][j]=(Id_T_fruit(data_Q["Qfruit"][j-1],data_T["T_fruit"][j-1],
                                             tiempo[j-1]))
        end_time = time.time()
        execution_time = end_time - start_time
        return metricas(data_T["T_room_real"]+273.15, data_T["T_room"]),execution_time

"----------------------------------GRAFICAS DE SIMULACION----------------------------------"
def graficar():
    plt.close('all')    #Se cierran las gráficas existentes
    
    if (mass_fruit<=0):
        n_plots=2
    else:
        n_plots=3
    fig, axs = plt.subplots(n_plots, 1, sharex=True, figsize=(7, 7))
    
    axs[0].plot(tiempo/60, data_T["T_evap"]-273.15, 'r')
    axs[0].set_title('Temp. a la salida del evaporador')
    axs[0].set_ylabel('[°C]')
    axs[0].grid(True) 
    
    # Segundo gráfico
    axs[1].plot(tiempo/60, data_T["T_room"]-273.15, 'g',label="Simulación")
    axs[1].plot(tiempo/60, data_T["T_room_real"], 'b',label="Real")
    axs[1].set_title('Temp. habitacion')
    axs[1].set_ylabel('[°C]')
    axs[1].grid(True) 
    #axs[1].set_ylim(np.min(data_T["T_room"])-274.15, np.max(data_T["T_room"])-272.15)
    axs[1].legend() 
    fig.suptitle('Resultados de Simulación')
    plt.show()
