'''
Este é um exemplo de como usar a biblioeta uasyncio para microcontroladores
È melhor executar tarefas assim pois as duas threads frequentemente levam os microcontroladores
a travamentos
'''
from random import randint
import uasyncio,time

#Antes de criar qualquer função é preciso dizer que ela será async
#Criando uma função simples
async def josiel():
    for c in range(10):
        a = randint(0,100)
        print(f'Josiel {a}')
        await uasyncio.sleep(0.2)
#Criando uma segunda função que executa um calculo qualquer
async def calcula():
    for c in range(5):
        c += 10
        print(c)
        await uasyncio.sleep(1) #É importante usar o sleep da biblioteca uasyncio para não pausar os outros codigos


async def funcao_v():
    #Aqui eu irei criar as tarefas que serão assíncronas
    a = uasyncio.create_task(calcula())
    b = uasyncio.create_task(josiel())
    
    #Precimos indicar que deve ocorrer a finalização das tarefas, se houver algum retorno isso se torna obrigatorio
    await a
    await b
#Chamamos a bilbiote para executar as tarefas de forma assíncrona
print(time.localtime())

uasyncio.run(funcao_v())

async def soma(a,b):
    soma = a + b
    print(soma)
    await uasyncio.sleep(1)
    
async def subtrai(a,b):
    subtrai = a - b
    print (subtrai)
    await uasyncio.sleep(1)
    
async def chama(j,k):
    a = uasyncio.create_task(soma(k,j))
    b = uasyncio.create_task(subtrai(j,k))
    await a
    await b
    
contador = 0

while True:
    contador += 1
    a = contador
    b = 2*a
    a = a * randint(0,100)
    print(a)
    
    
    uasyncio.run(chama(a,b))






