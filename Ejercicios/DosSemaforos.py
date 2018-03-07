import threading

s1 = threading.Semaphore(1)
s2 = threading.Semaphore(0)

def consumidor():
	s2.acquire()
	print "Consumidor - Valor actual: ",contador[0]
	s1.release()

def productor():
	s1.acquire()
	contador[0] += 1
	print "Productor - Valor actual: ",contador[0]
	s2.release()

contador = []
contador.append(0)

for x in xrange(1,20):
	hiloProductor = threading.Thread(target=productor)
	hiloConsumidor = threading.Thread(target=consumidor)

	hiloConsumidor.start()
	hiloProductor.start()

	hiloConsumidor.join()
	hiloProductor.join()