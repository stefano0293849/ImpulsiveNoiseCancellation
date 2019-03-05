%Program to plot compressed data algorithm and original audio file

%Read the original audio file
[signal,fs] = audioread('audio\rec_original_compressed.wav');
dt = 1/fs;
signal = signal(:,1);

%Read the filtered audio file
[signal_compr,fs] = audioread('audio\rec_clipping_compressed.wav');
signal_compr = signal_compr(:,1);

%Time original audio
t_orig = 0:dt:(length(signal)*dt)-dt;

%Time filtered audio
t_compr = 0:dt:(length(signal_compr)*dt)-dt;

figure;

%Gunshot peak points, used as refereance
P= [5.18 5.18 ; 7.19 7.19 ; 9.6 9.6 ; 11.6 11.6 ; 13.99 13.99 ; 16 16 ; 18.4 18.4 ; 20.38 20.38 ; 22.83 22.83 ; 24.83 24.83 ; 27.26 27.26  ; 29.24 29.24 ; 31.73 31.73 ; 33.71 33.71 ; 36.11 36.11 ; 38.108 38.108 ; 40.57 40.57 ; 42.56 42.56 ; 44.98 44.98 ; 46.93 46.96  ];
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




%Plot the filtered compression algorithm audio in the time domain
f2 = subplot(2,1,2);
plot(f2,t_compr,signal_compr);
xlabel('Seconds','FontSize',10,'FontWeight','bold','Color','k');
ylabel('Amplitude','FontSize',10,'FontWeight','bold','Color','k');
title(f2,'Compressed Filtered Audio Wave');
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


%Plot the PSD of the filtered audio with compressed algorithm
f4 = subplot(2,1,2);
pspectrum(signal_compr,fs,'spectrogram','FrequencyLimits',[20 20000],'TimeResolution',1)
title(f4,'Compressed Filtered Audio Wave');
for ii = 1:nloop
    line(P(ii,:),get(f4,'YLim'),'Color','red','LineStyle','--','LineWidth',0.5)
end