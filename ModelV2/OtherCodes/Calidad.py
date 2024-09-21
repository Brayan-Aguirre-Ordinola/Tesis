import numpy as np
import CoolProp.CoolProp as CP
import scipy.io

def data_val(name,n):
    # Cargar el archivo .mat
    data = scipy.io.loadmat(name)["data_evaporador"]
    tiempo = data[:n, 0]
    temp_eva = data[:n, 1]
    pres_eva = data[:n, 2]
    return tiempo, temp_eva+273.15, pres_eva*1e5

tiempo, temp_eva, pres_eva = data_val("data_evaporador.mat", 3000)

def densidad (temperatura,presion):
    densidad=cp('D', 'T', temperatura, 'P', presion, 'Air')


for i in range (len(tiempo)+1):
    den[i]=densidad(data_T["T_room"][i],101325)