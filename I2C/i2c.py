'''
Josiel Moreira da Silva
Codigo Para leitura e gravação do sensor MPU6050 e de quebra escrita e leitura de Memorias
É possivel consultar as funções na propia documentação do micropython.
O objetivo é estabelecer a comunicação entre dispositivos no propio barramento I2C. Podemos neste barramento conectar centenas de dispositivos
basta compreender que cada dispositivo terá o seu propio endereço. Podemos usar a implementaçao do SoftI2C importando ela da biblioteca machine
é uma implentação por software. Com SoftI2C.scan() podemos encontrar todos endereços dos dispositivos que estão conectados ao barramento.



'''

'''----------------------------------------Importações-------------------------------------------------------------------------------------'''
from machine import Pin,SoftI2C
from time import sleep

'''-----------------------------------------Inicio do Codigo-------------------------------------------------------------------------------'''
i2c = SoftI2C(sda=Pin(21),scl=Pin(22),freq=9600) #Estamos iniciando o Protocolo i2c com sda no pino 21 e scl no pino 22 e baudrate de 9600
dispositivosI2C =  i2c.scan() 					 #Estamos identificando os endereços dos dispositivos conectados ao barramento i2c

print(dispositivosI2C)							 #Estamos imprimindo quais foram os dispositovos encontados no barramento I2C


i2c.writeto_mem(80,2,b'\xFF')					 # Essa funçao de escrita pode ser encontrada no documentação do micropython ela é responsavel por fazer a escrita no endereço de memoria

sleep(0.006)									 #Estava dando um erro desgraçado devido a não estar esperando o tempo de gravação
a = i2c.readfrom_mem(80,2,1)					 #Após o dado gravado podemos efetuar a leitura


print(a)
