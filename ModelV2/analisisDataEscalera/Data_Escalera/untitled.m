clc
clear
close all

load('Ecostar20230104_Escalera.mat')
% load('matlab_20220929_G1.mat')
t1                = Ecostar20230104_Escalera.Time;
Tcond    = Ecostar20230104_Escalera.T_cond;
Tamb   = Ecostar20230104_Escalera.T_amb;
ti         = 500;
tf         = 26884;
q          = tf-ti+1;
te         = [1:q]';
Tamb    = Tamb(ti:tf);  
Tcond    = Tcond(ti:tf);
diff = Tcond - Tamb;
