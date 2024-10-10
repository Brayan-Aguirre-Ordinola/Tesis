import numpy as np
import matplotlib.pyplot as plt

a=np.array([2,3,4,4,6,7,8,9,11,12,13,14,15,16]);
b=np.array([8.878,10.43,12.981,12.566,16.354,18.204,20.065,22.886,26.918,28.561,30.665,32.410,34.559,36.312])
def sim(x1,x2):
    y=[x1*x+x2 for x in a]
    return y
def mse(y_p,y):
    e=[x-y for x,y in zip(y_p,y)]
    j=np.dot(e,e)/len(y)
    return j
n_datos=len(a)
epocas=300
betha1=np.zeros(epocas)
betha2=np.zeros(epocas)
costFunction=np.zeros(epocas)
betha1[0]=0
betha1[1]=4
betha2[0]=0
betha2[1]=5
alpha=5e-5
deltab1=0.1 
deltab2=0.1
y_pred_temp1=np.zeros(n_datos)
y_pred_temp2=np.zeros(n_datos)

for i in range(2,epocas):
    y_pred_temp1=sim(betha1[i-1],betha2[i-1])
    costFunction[i-1]=mse(y_pred_temp1,b)
    if i==3 and costFunction[i-1]>costFunction[i-2]:
        print('Elegir un menor valor de velocidad de aprendizaje')
        break
    sumaj=0
    y_inc_betha1=sim(betha1[i-1],betha2[i-2])
    for j in range(n_datos):
        sumaj+=(y_pred_temp1[j]-b[j])*(y_inc_betha1[j]-y_pred_temp2[j])
    sumak=0
    y_inc_betha2=sim(betha1[i-2],betha2[i-1])
    for k in range(n_datos):
        sumak+=(y_pred_temp1[j]-b[j])*(y_inc_betha2[j]-y_pred_temp2[j])
    betha1[i]=betha1[i-1]-2*alpha*sumaj/(betha1[i-1]-betha1[i-2])
    betha2[i]=betha2[i-1]-2*alpha*sumak/(betha2[i-1]-betha2[i-2])
    y_pred_temp2=y_pred_temp1[:]
    
plt.close('all')
fig,(ax1,ax2)=plt.subplots(2,1,figsize=(8,6))
ax1.plot(betha1[1:],costFunction[1:],label='Betha1')
ax1.set_xlabel('Betha1')
ax1.set_ylabel('mse')
ax1.set_title('Titulo1')
ax1.legend()

ax2.plot(betha2[1:],costFunction[1:],label='Betha1')
ax2.set_xlabel('Betha2')
ax2.set_ylabel('mse')
ax2.set_title('Titulo2')
ax2.legend()
plt.tight_layout()
plt.show()