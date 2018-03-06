import threading

s = threading.BoundedSemaphore(1)

def consumidor():
	s.acquire()
	if contador[1] == 1:
		contador[1] = 0
		print "Consumidor - Valor actual: ",contador[0]
	s.release()

def productor():
	s.acquire()
	if contador[1] == 0:
		contador[1] = 1
		contador[0] += 1
		print "Productor - Valor actual: ",contador[0]
	s.release()

contador = []
contador.append(0)
contador.append(0)

for x in xrange(1,20):
	hiloProductor = threading.Thread(target=productor)
	hiloConsumidor = threading.Thread(target=consumidor)

	hiloConsumidor.start()
	hiloProductor.start()

	hiloConsumidor.join()
	hiloProductor.join()