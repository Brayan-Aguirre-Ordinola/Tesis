clc
clear
close all
%% Carga de los datos
load('Ecostar20230104_Escalera.mat')

t1                = Ecostar20230104_Escalera.Time;
t                 =  [1:size(t1,1)]';
% Data de entrada:
Fcomp_complete    = Ecostar20230104_Escalera.Freq;
Potcomp_complete  = Ecostar20230104_Escalera.Power;
% Temperaturas:
Troom_complete   = Ecostar20230104_Escalera.T_room;
Tamb_complete     = Ecostar20230104_Escalera.T_amb;
Tevap_complete    = Ecostar20230104_Escalera.T_0;        
Tsh_complete      = Ecostar20230104_Escalera.T_sh;
Tsuc_complete     = Ecostar20230104_Escalera.T_sh_dis;  
Tdisc_complete    = Ecostar20230104_Escalera.T_dis;     
Tcond_complete    = Ecostar20230104_Escalera.T_cond;    
% Presiones:
Pdisc_complete    = Ecostar20230104_Escalera.P_dis;      
Psuc_complete     = Ecostar20230104_Escalera.P_suc;     

Ts                = 1;                                         
p                 = size(Psuc_complete,1);

Time               = Ecostar20230104_Escalera.Time;
%% Data para simulink

ti         = 500;
tf         = 26884;
q          = tf-ti+1;
%tiempo
te         = [1:q]';
% Data de entrada:
Fcomp_simulink    = Fcomp_complete(ti:tf);   % Frecuencia del compresor [Hz]
Potcomp_simulink  = Potcomp_complete(ti:tf); % Potencia del compresor [kW]
% Temperaturas:
Troom_simulink   = Troom_complete(ti:tf);  % T del aire en la cámara de refrigeracion [°C]
Tamb_simulink     = Tamb_complete(ti:tf);    % T ambiente [°C]
Tevap_simulink    = Tevap_complete(ti:tf);   % T de R404a en el evaporador [°C]
Tsh_simulink      = Tsh_complete(ti:tf);     % T      
Tsuc_simulink     = Tsuc_complete(ti:tf);    % T de R404a al ingresar al compresor [°C]
Tdisc_simulink    = Tdisc_complete(ti:tf);   % T de R404a a la salida del compresor [°C]
Tcond_simulink    = Tcond_complete(ti:tf);   % T de R404a en el condensador[°C]
% Presiones:
Pdisc_simulink    = Pdisc_complete(ti:tf);   % P de R404a a la salida del compresor [bar]
Psuc_simulink     = Psuc_complete(ti:tf);    % P de R404a al ingresar al compresor [bar]

%% Data para exportar
data=[te,Fcomp_simulink,Potcomp_simulink,Troom_simulink,Tamb_simulink,Tevap_simulink,Tsh_simulink,Tsuc_simulink,Tdisc_simulink,Tcond_simulink,Psuc_simulink,Pdisc_simulink];
%% Ploteo de gráficas
%{
figure(1)
subplot(2,1,1)
plot(te,Pdisc_simulink)
title('Pcomp-Out Experimento')
ylabel('Bar')
xlabel('s')
grid on

subplot(2,1,2)
plot(te,Tdisc_simulink)
title('Tcomp-Out Experimento')
ylabel('°C')
xlabel('s')
grid on


%%
figure(2)
subplot(2,1,1)
plot(te,Psuc_simulink)
title('Pcomp-in Experimento')
ylabel('°C')
xlabel('s')
grid on

subplot(2,1,2)
plot(te,Tsuc_simulink)
title('Tcomp-in Experimento')
ylabel('°C')
xlabel('s')
grid on
%%
figure(3)
subplot(3,1,1)
plot(te,Tcond_simulink)
title('Tcond-Experimento')
ylabel('°C')
xlabel('s')
grid on

subplot(3,1,2)
plot(te,Tevap_simulink)
title('Tevap-Experimento')
ylabel('°C')
xlabel('s')
grid on

subplot(3,1,3)
plot(te,Tamb_simulink)
title('Tamb-Experimento')
ylabel('°C')
xlabel('s')
grid on

%%
figure(4)
subplot(3,1,1)
plot(te,Fcomp_simulink)
title('FComp-Experimento')
ylabel('Hz')
xlabel('s')
grid on

subplot(3,1,2)
plot(te,Potcomp_simulink)
title('PotComp-Experimento')
ylabel('kW')
xlabel('s')
grid on

subplot(3,1,3)
plot(te,Ttecho_simulink+0.8)
title('Troom')
ylabel('°C')
xlabel('s')
grid on

%%
figure(5)
subplot(2,1,1)
plot(te,Fcomp_simulink)
title('FComp-Experimento')
ylabel('Hz')
xlabel('s')
grid on

subplot(2,1,2)
plot(te,dif_amb_cond)
title('DeltaT')
ylabel('°C')
xlabel('s')
grid on
%%
figure(6)
plot(te,Beta_compresion)
title('Razon de compresion')
ylabel('-')
xlabel('s')
grid on
%%
figure(7)
plot(te,(Fcomp_simulink*0.1+5)./dif_amb_cond)
title('Relación lineal entre frecuencia y diff temp')
ylabel('-')
xlabel('s')
grid on
%}