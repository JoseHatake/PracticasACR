import threading

s = threading.Semaphore(1)

def consumidor():
	s.acquire()
	print "Consumidor - Valor actual: ",contador[0]
	s.release()

def productor():
	s.acquire()
	contador[0] += 1
	print "Productor - Valor actual: ",contador[0]
	s.release()

contador = [1]

for x in xrange(1,20):
	hiloProductor = threading.Thread(target=productor)
	hiloConsumidor = threading.Thread(target=consumidor)

	hiloConsumidor.start()
	hiloProductor.start()

	hiloConsumidor.join()
	hiloProductor.join()