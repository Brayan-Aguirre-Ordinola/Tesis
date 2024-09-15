clc
clear
close all

load('Ecostar20230104_Escalera.mat')
% load('matlab_20220929_G1.mat')

t1                = Ecostar20230104_Escalera.Time;
t                 =  [1:size(t1,1)]';

Fcomp_complete    = Ecostar20230104_Escalera.Freq;
Potcomp_complete  = Ecostar20230104_Escalera.Power;

Ttecho_complete   = Ecostar20230104_Escalera.T_room;
Tamb_complete     = Ecostar20230104_Escalera.T_amb;
Tevap_complete    = Ecostar20230104_Escalera.T_0;        % T de R404a en el evaporador [°C]
Tsh_complete      = Ecostar20230104_Escalera.T_sh;
Tsuc_complete     = Ecostar20230104_Escalera.T_sh_dis;   % T de R404a al ingresar al compresor [°C]
Tdisc_complete    = Ecostar20230104_Escalera.T_dis;      % T de R404a a la salida del compresor [°C]
Tcond_complete    = Ecostar20230104_Escalera.T_cond;     % T de R404a en el condensador[°C]

Pdisc_complete    = Ecostar20230104_Escalera.P_dis;      % [bar]
Psuc_complete     = Ecostar20230104_Escalera.P_suc;      % [bar]

Ts                = 1;                 
p                 = size(Psuc_complete,1);



Time               = Ecostar20230104_Escalera.Time;

%% Eje horizontal = Hora

% figure(9)
% subplot (3,1,1)
% plot(Time,Ttecho_complete+0.8)
% grid on
% title('Troom')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% subplot(3,1,2)
% plot(Time,Tamb_complete)
% grid on
% title('Tamb')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% subplot(3,1,3)
% plot(Time,Fcomp_complete)
% title('Fcomp')
% ylabel('Hz')
% xlabel('s')
% grid on
% 
% figure(10)
% subplot(2,1,1)
% plot(Time,Psuc_complete)
% title('Psuc')
% ylabel('Bar')
% xlabel('s')
% grid on
% 
% subplot(2,1,2)
% plot(Time,Tsuc_complete)
% title('Tsuc')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% figure(11)
% subplot(3,1,1)
% plot(Time,Pdisc_complete)
% title('Pdisc')
% ylabel('Bar')
% xlabel('s')
% grid on
% 
% subplot(3,1,2)
% plot(Time,Tdisc_complete)
% title('Tdisc')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% subplot(3,1,3)
% plot(Time,Tamb_complete)
% title('Tamb')
% ylabel('°C')
% xlabel('s')
% grid on



%% Data Completa Eje Horizontal = segundos
% figure(1)
% subplot(3,1,1)
% plot(t,Pdisc_complete)
% title('Pcomp-Out')
% ylabel('Bar')
% xlabel('s')
% grid on
% 
% subplot(3,1,2)
% plot(t,Psuc_complete)
% title('Pcomp-In')
% ylabel('Bar')
% xlabel('s')
% grid on
% 
% subplot(3,1,3)
% plot(t,Ttecho_complete)
% title('Ttecho')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% figure(2)
% subplot(3,1,1)
% plot(t,Tdisc_complete)
% title('Tcomp-Out')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% subplot(3,1,2)
% plot(t,Tsh_complete)
% title('Tsh')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% 
% subplot(3,1,3)
% plot(t,Tsuc_complete)
% title('Tcomp-In')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% figure(3)
% subplot(3,1,1)
% plot(t,Tcond_complete)
% title('Tcond')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% subplot(3,1,2)
% plot(t,Tevap_complete)
% title('Tevap')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% grid on
% subplot(3,1,3)
% plot(t,Tamb_complete)
% title('Tamb')
% ylabel('°C')
% xlabel('s')
% grid on
% 
% figure(4)
% subplot(3,1,1)
% plot(t,Fcomp_complete)
% title('Fcomp')
% ylabel('Hz')
% xlabel('s')
% grid on
% 
% subplot(3,1,2)
% plot(t,Potcomp_complete)
% title('Potcomp')
% ylabel('kW')
% xlabel('s')
% grid on
% 
% subplot(3,1,3)
% plot(t,Ttecho_complete)
% title('Ttecho')
% ylabel('°C')
% xlabel('s')
% grid on
 
%% Data para simulink
 
ti         = 500;
tf         = 26884;
q          = tf-ti+1;
te         = [1:q]';

Fcomp_simulink    = Fcomp_complete(ti:tf);
Potcomp_simulink  = Potcomp_complete(ti:tf);
Ttecho_simulink   = Ttecho_complete(ti:tf);
Tamb_simulink     = Tamb_complete(ti:tf);  
Tevap_simulink    = Tevap_complete(ti:tf);   % T de R404a en el evaporador [°C]
Tsh_simulink      = Tsh_complete(ti:tf);      
Tsuc_simulink     = Tsuc_complete(ti:tf);    % T de R404a al ingresar al compresor [°C]
Tdisc_simulink    = Tdisc_complete(ti:tf);   % T de R404a a la salida del compresor [°C]
Tcond_simulink    = Tcond_complete(ti:tf);   % T de R404a en el condensador[°C]

Pdisc_simulink    = Pdisc_complete(ti:tf);   % [bar]
Psuc_simulink     = Psuc_complete(ti:tf);    % [bar]

Tdisc_s           = [te,Tdisc_simulink];
Tsuc_s            = [te,Tsuc_simulink];
Tcond_in_s        = [te,Tcond_simulink];
Tamb_s            = [te,Tamb_simulink];
T_evap_ref_s      = [te,Tevap_simulink];       % T de R404a en el evaporador [°C]
T_techo_s         = [te,Ttecho_simulink];
Pdisc_s           = [te,Pdisc_simulink];
Psuc_s            = [te,Psuc_simulink];
Pow_comp_s        = [te,Potcomp_simulink];
freq_comp_s       = [te,Fcomp_simulink];

dif_amb_cond      = Tcond_simulink-Tamb_simulink;
diff_average=mean(dif_amb_cond)
%% Data recortada
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
%}
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