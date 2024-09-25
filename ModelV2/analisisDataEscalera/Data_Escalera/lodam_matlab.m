experiment = 'Data 20230104_Escalera';
Init       = 1;
Fin        = length(Time);
Time       = Time(Init:1:Fin);
Freq       = FCAPIFrqAct(Init:1:Fin);
T_room     = InputTroom(Init:1:Fin);
T_0        = InputT0(Init:1:Fin);
T_dis      = InputTdis(Init:1:Fin);
T_cond     = InputTC(Init:1:Fin);
T_amb      = InputTamb(Init:1:Fin);
P_dis      = InputPdis(Init:1:Fin);
P_suc      = InputPsuc(Init:1:Fin);
Current    = FCAPICurrent(Init:1:Fin);
Power      = FCAPIPower(Init:1:Fin);
T_sh       = InputTsh(Init:1:Fin);
T_sh_dis   = InputTsh_dis(Init:1:Fin);
Ecostar20230104_Escalera = struct('Duration',Time(end)-Time(1),'Time',Time,'Freq',Freq,'T_room',T_room,'T_amb',T_amb,'T_0',T_0,'T_cond',T_cond,'T_dis',T_dis,'P_dis',P_dis,'P_suc',P_suc,'Current',Current,'Power',Power,'T_sh',T_sh,'T_sh_dis',T_sh_dis,'Experiment',experiment);
save ecostar20230104_Escalera.mat Ecostar20230104_Escalera