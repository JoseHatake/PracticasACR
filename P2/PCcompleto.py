import threading
from asyncio import Semaphore

s = Semaphore()

def consumidor(n):
	counter = 0
	while counter < n:
		s.acquire()
		contador[0] -= 1
		counter += 1
		print "Valor actual: ",contador[0]
		s.release()

def productor(m):
	counter = 0
	while counter < n:
		s.acquire()
		contador[0] += 1
		counter += 1
		print "Valor actual: ",contador[0]
		s.release()

contador = [1]
numeroDeIteraciones = 20

hiloProductor = threading.Thread(target=productor,args=(numeroDeIteraciones))
hiloConsumidor = threading.Thread(target=consumidor,args=(numeroDeIteraciones))

hiloConsumidor.start()
hiloProductor.start()

hiloConsumidor.join()
hiloProductor.join()