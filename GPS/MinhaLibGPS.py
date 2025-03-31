from machine import UART
from time import sleep
'''Para usar o gps devemos entender as sentenças NMEA
$: Isso indica o início da sentença NMEA
GPGGA: Dados de correção do sistema de posicionamento global
103005 : Esta é a hora UTC quando os dados foram acessados em HH:MM:SS. Neste caso, a hora
10:30:05 UTC
3807.038, N : Latitude 38 graus 07.038′ N
07128.99030, E : Longitude 71 graus 28.00030′ E
1: correção de GPS
07 : Número de satélites rastreados
1.43: Diluição horizontal da posição
134.5, M : Mostra a altitude (m) acima do nível do mar
42,9, M: Altura do geóide (nível médio do mar)
Campo vazio: tempo em segundos desde a última atualização do DGPS
Campo vazio: número de identificação da estação DGPS
*78 : os dados da soma de verificação
'''

uart1 = UART(2, baudrate=9600, tx=17, rx=16)



Encontrar_Gps = True
sleep(2)
Leitura_GPS = uart1.read()
k = str(Leitura_GPS)

while Encontrar_Gps:
    j = k.split('$')
    for i,l in enumerate(j):
        #print(i,l)
        if i == 3:
            #print(l.split(','))
            M_GPGGA = l.split(',')  #Refernte ao GPGGA que é a lista que contem os dados em que estamos interessados
            #Será exibido a seguinte frase ['GPGGA', '142957.00', '2059.03327', 'S', '04738.39422', 'W', '1', '06', '2.42', '878.5', 'M', '-7.0', 'M', '', '*48\\r\\n']
            print(f'O Horario UTC: {M_GPGGA[1]}\n Latitude {M_GPGGA[2]} S\n Longitude {M_GPGGA[4]} W\n Numero de Satelites {M_GPGGA[7]}\n Altitude em relacao ao nivel do mar {M_GPGGA[9]} m')

    sleep(1)
'''while Encontrar_Gps:
    sleep(1)
    print(uart1.read())'''
