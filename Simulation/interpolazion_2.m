clear;
y = audioread('ProvaSparo3.wav');
x_in = y;
y=y(:,1);
y_db= max(0,log(y.^2+1e-7)+12); %scala logaritmica per comprendere meglio i picchi da filtrare 
gwin = 6000; %finestra che usiamo per addestrare LPC 
flen = 256; %l'ordine (lunghezza) LPC

plot(y_db);
figure;

[flb,fla]= butter(1,0.00003); %coefficienti per filtro lento che segue il volume medio del suono
[fvb,fva]= butter(2,0.02); %coefficienti per filtro veloce che viene usato per meccanismo di trigger

%filtraggio
yfl = filter(flb,fla,y_db);
yfv = filter(fvb,fva,y_db);
%plot (yfl);
%figure;
plot (yfv-yfl); %mostriamo il segnale che viene usato per il trigger per studiare la soglia di attivazione ottima
figure;

%meccanismo di trigger: quando il segnale del filtro veloce supera quello
%del filtro lento di "abbastanza" vuol dire che c'è un rumore da togliere
%A questo punto dobbiamo riconoscere l'attimo di fine filtraggio che è
%quando il segnale veloce rimane sotto una certa soglia in confronto a
%quello lento per "abbastanza" tempo
stato = 0;
inizi = [];
fini = [];

for i = (gwin+1):length(y)
    if stato == 0
        if yfv(i) > yfl(i)+5
            stato = 1;
            inizi = [inizi,i];
        end
    else 
        if yfv(i) < yfl(i)+0.5
            stato = stato+1;
            if stato==2500
                stato=0;
                fini = [fini,i];
            end
        else
            stato=1;
        end
    end
end
     
%inizi
%fini

        
%loop for che itera su tutti gli intervalli di rumore rilevati         
        

for i = 1:length(fini)
    
lx1 = fini(i)-inizi(i)+3500; %3500 e 1500 dopo vengono messi come prototipi per anticipare /posticipare il "periodo di buco"
iniziocolpo=inizi(i);
inizio= iniziocolpo-gwin-1500;
ye= y(inizio:inizio+lx1+gwin); %ye contiene una prima parte di suono "buono" e il resto è rumore usiamo la prima parte per addestrare la LPC sullo spettro di frequenze originali
a = lpc(ye(1:gwin),flen);
ee = filter(a,1,ye); %LPC inverso (applico filtro inverso). In questo i buchi possono venir riempiti con del rumore bianco 
sg=sqrt(mean(ee(1:gwin).^2)); %calcolo dell'ampiezza del rumore (RMS) 
ee((gwin+1):end)=randn(lx1+1,1)*sg; %usare RMS per generare del ruore nei buchi
ere = filter(1,a,ee); %passiamo tutto nel filtro LPC originale per ripristinare la prima parte e far assumere alla seconda uno spettro corretto 
% size (ee)
% size (ere)
y(inizio:inizio+lx1+gwin)= ere; %sostituiamo nel segnale la parte elaborata
end

plot(y);

