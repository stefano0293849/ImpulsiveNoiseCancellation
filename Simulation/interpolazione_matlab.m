%simulate this program after had simulated the simulink model
%after had commented the red block


%first solution with cubic interpolation(bad)

% touti=tout ;
% zs= audio==0 ;
% audio(zs)= [] ;
% tout( zs) = [] ;
% output= interp1( tout, audio, touti, 'cubic') ;


%second solution with autoregressive interpolation model (ARIMA)
audio_interp=audio;
audio_interp(~audio_interp)=nan;
%y = fillgaps(audio);  %lento
y = fillgaps(audio_interp,4000);




