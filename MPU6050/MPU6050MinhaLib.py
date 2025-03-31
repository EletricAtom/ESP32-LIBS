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
dispositivosI2C =  i2c.scan() 					 #Estamos identificando os endereços dos dispositovos conectados ao barramento i2c

print(dispositivosI2C)							   #Estamos imprimindo quais foram os dispositovos encontados no barramento I2C

'''
i2c.writeto_mem(80,2,b'\xFF')					 # Essa funçao de escrita pode ser encontrada no documentação do micropython ela é responsavel por fazer a escriat no endereço de memoria
#(dispositivo,endereço,dado)
sleep(0.006)									         #Estava dando um erro desgraçado devido a não estar esperando o tempo de gravação
a = i2c.readfrom_mem(80,2,1)					 #Após o dado gravado podemos efetuar a leitura
print(a)
'''
#Forma de escrever em hexadecimal b'\xFF'
'''
FUNDOS DE ESCALA
// Configura Giroscópio para fundo de escala desejado
  /*
    (0b00000000); // fundo de escala em +/-250°/s
    (0b00001000); // fundo de escala em +/-500°/s
    (0b00010000); // fundo de escala em +/-1000°/s
    (0b00011000); // fundo de escala em +/-2000°/s
    
// Configura Acelerometro para fundo de escala desejado
  /*
      (0b00000000); // fundo de escala em +/-2g
      (0b00001000); // fundo de escala em +/-4g
      (0b00010000); // fundo de escala em +/-8g
      (0b00011000); // fundo de escala em +/-16g
      
      /* Alterar divisão conforme fundo de escala escolhido:
      Acelerômetro
      +/-2g = 16384
      +/-4g = 8192
      +/-8g = 4096
      +/-16g = 2048

      Giroscópio
      +/-250°/s = 131
      +/-500°/s = 65.6
      +/-1000°/s = 32.8
      +/-2000°/s = 16.4
'''
i2c.writeto_mem(0x68,0x6B,b'\00')
i2c.writeto_mem(0x68,0x1B,b'\x18')
i2c.writeto_mem(0x68,0x1C,b'\x18')

'''
  AccX = //0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  AccY = //0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AccZ = //0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Temp = //0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GyrX = //0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyrY = //0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GyrZ = //0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
'''

#Muito importante lembrar de usar a função types() para saber o tipo de dado
# Podemos criar um array de bytes  variavel = bytearray([17,23,12])
#Para pegar ym byte e converte-lo para int basta selecionar a posição dentro do array "inteiro = variavel[1]"

while True:
    #medidas = i2c.readfrom_mem(0x68,0x3b,14) #Ao todo são Bytes de dados 
    Aceleracaox = i2c.readfrom_mem(0x68,0x3b,2)
    Aceleracaox = (Aceleracaox[0]+Aceleracaox[1])/2048
    
    Aceleracaoy = i2c.readfrom_mem(0x68,0x3d,2)
    Aceleracaoy = (Aceleracaoy[0]+Aceleracaoy[1])/2048
    
    Aceleracaoz = i2c.readfrom_mem(0x68,0x3f,2)
    Aceleracaoz = (Aceleracaoz[0]+Aceleracaoz[1])/2048    
 
    temperatura = i2c.readfrom_mem(0x68,0x41,2) #Tratamento (temperatura[0]+temperatura[1])/16.8  conversão para inteiro
    temperatura = (temperatura[0]+temperatura[1])/16.8

    Giroscopiox = i2c.readfrom_mem(0x68,0x43,2)
    Giroscopiox = (Giroscopiox[0]+Giroscopiox[1])/131
    
    Giroscopioy = i2c.readfrom_mem(0x68,0x45,2)
    Giroscopioy = (Giroscopioy[0]+Giroscopioy[1])/131
    
    Giroscopioz = i2c.readfrom_mem(0x68,0x47,2)
    Giroscopioz = (Giroscopioz[0]+Giroscopioz[1])/131
    
    print(f'ax = {Aceleracaox},ay = {Aceleracaoy},az = {Aceleracaoz},T = {temperatura},gx = {Giroscopiox},gy = {Giroscopioy},gz = {Giroscopioz}')
    
    
    sleep(0.5)


