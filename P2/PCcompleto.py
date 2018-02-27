import threading

s = threading.Semaphore(1)

def consumidor():
	counter = 0
	while counter < 20:
		s.acquire()
		contador[0] -= 1
		counter += 1
		print "Valor actual: ",contador[0]
		s.release()

def productor():
	counter = 0
	while counter < 20:
		s.acquire()
		contador[0] += 1
		counter += 1
		print "Valor actual: ",contador[0]
		s.release()

contador = [1]
numeroDeIteraciones = 20

hiloProductor = threading.Thread(target=productor)
hiloConsumidor = threading.Thread(target=consumidor)

hiloConsumidor.start()
hiloProductor.start()

hiloConsumidor.join()
hiloProductor.join()