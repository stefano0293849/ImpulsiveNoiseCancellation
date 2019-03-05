%Program to plot  old data algorithm and original audio file

%Read the original audio file
[signal,fs] = audioread('audio\rec_original_old.wav');
dt = 1/fs;
signal = signal(:,1);

%Read the filtered audio file
[signal_old,fs] = audioread('audio\rec_clipping_old.wav');
signal_old = signal_old(:,1);

%Time original audio
t_orig = 0:dt:(length(signal)*dt)-dt;

%Time filtered audio
t_old = 0:dt:(length(signal_old)*dt)-dt;

figure;

%Gunshot peak points, used as refereance
P= [5.67 5.67 ; 7.68 7.68 ; 10.13 10.13 ; 12.11  12.11  ;  14.55 14.55 ; 16.53 16.53 ;  18.97 18.97 ; 20.96 20.96 ; 23.39 23.39 ;  25.37 25.37 ; 27.77 27.77 ; 29.73 29.73 ; 32.13 32.13 ; 34.11 34.11 ; 36.56 36.56 ; 38.54 38.54 ; 40.94 40.94 ; 42.96 42.96 ; 45.39 45.39  ];
nloop = size(P,1);

%Plot the original audio in the time domain
f1 = subplot(2,1,1);
plot(f1,t_orig,signal);
xlabel('Seconds','FontSize',10,'FontWeight','bold','Color','k');
ylabel('Amplitude','FontSize',10,'FontWeight','bold','Color','k');
title(f1,'Original Audio Wave');
for ii = 1:nloop
    line(P(ii,:),get(f1,'YLim'),'Color','red','LineStyle','--','LineWidth',0.5)
end




%Plot the filtered old audio algorithm in the time domain
f2 = subplot(2,1,2);
plot(f2,t_old,signal_old);
xlabel('Seconds','FontSize',10,'FontWeight','bold','Color','k');
ylabel('Amplitude','FontSize',10,'FontWeight','bold','Color','k');
title(f2,'Old Data Filtered Audio Wave');
for ii = 1:nloop
    line(P(ii,:),get(f2,'YLim'),'Color','red','LineStyle','--','LineWidth',0.5)
end



figure

%Plot the PSD of the original audio
f3 = subplot(2,1,1);
pspectrum(signal,fs,'spectrogram','FrequencyLimits',[20 20000],'TimeResolution',1)
title(f3,'Original Audio Wave');
for ii = 1:nloop
    line(P(ii,:),get(f3,'YLim'),'Color','red','LineStyle','--','LineWidth',0.5)
end


%Plot the PSD of the filtered audio with old data algorithm
f4 = subplot(2,1,2);
pspectrum(signal_old,fs,'spectrogram','FrequencyLimits',[20 20000],'TimeResolution',1)
title(f4,'Old Data Filtered Audio Wave');
for ii = 1:nloop
    line(P(ii,:),get(f4,'YLim'),'Color','red','LineStyle','--','LineWidth',0.5)
end