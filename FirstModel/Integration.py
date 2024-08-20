"""
Archivo que tiene los métodos de integracion
Estos resuelven una ecuacion diferencial ordinaria del siguiente tipo:
                                dy=f(y,x)
Para usar correctamente se debe recordar que las variables deben indicarse 
en el mismo orden cómo se está expresando la función.
"""
dt=0.1
"Integracion por euler"
def integracion (dy,y,x):
    k1=dy(y,x)
    return y+k1*dt
    
"Integración por Runge Kutta"
def integracion1 (dy,y,x):
    k1=dy(y,x) 
    k2=dy(y+dt*k1/2,x+dt/2)
    k3=dy(y+dt*k2/2,x+dt/2)
    k4=dy(y+dt*k3,x+dt)
    return y+(k1+2*k2+2*k3+k4)*dt/6
