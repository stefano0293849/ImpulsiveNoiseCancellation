%Program to plot zero algorithm and original audio file

%Read the original audio file
[signal,fs] = audioread('audio\rec_original_zero.wav');
dt = 1/fs;
signal = signal(:,1);

%Read the filtered audio file
[signal_zero,fs] = audioread('audio\rec_clipping_zero.wav');
signal_zero = signal_zero(:,1);

%Time original audio
t_orig = 0:dt:(length(signal)*dt)-dt;

%Time filtered audio
t_zero = 0:dt:(length(signal_zero)*dt)-dt;

figure;

%Gunshot peak points, used as refereance
P= [8.66 8.66 ; 11 11 ;  13 13 ; 15.44 15.44 ; 17.46 17.46 ; 19.9 19.9 ; 21.90 21.90 ; 24.3 24.3  ; 26.3 26.3 ;  28.73 28.73 ; 30.69 30.69 ; 33.1 33.1 ; 35.11 35.11 ; 37.52 37.52 ; 39.5  39.5 ; 41.96 41.96 ; 43.95 43.95 ; 46.43 46.43 ; 48.41 48.41 ];
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



%Plot the filtered zero audio in the time domain
f2 = subplot(2,1,2);
plot(f2,t_zero,signal_zero);
xlabel('Seconds','FontSize',10,'FontWeight','bold','Color','k');
ylabel('Amplitude','FontSize',10,'FontWeight','bold','Color','k');
title(f2,'Zero Filtered Audio Wave');
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


%Plot the PSD of the filtered audio with zero algorithm
f4 = subplot(2,1,2);
pspectrum(signal_zero,fs,'spectrogram','FrequencyLimits',[20 20000],'TimeResolution',1)
title(f4,'Zero Filtered Audio Wave');
for ii = 1:nloop
    line(P(ii,:),get(f4,'YLim'),'Color','red','LineStyle','--','LineWidth',0.5)
end
