import threading

def lector():
	for x in xrange(1,20):
		print "El contador tienen el valor de : ",contador[0]

def escritor():
	for x in xrange(1,20):
		print "Se incrementa el valor en 1"
		contador[0] = contador[0] + 1

contador = []
contador.append(0)

hiloLector = threading.Thread(target=lector)
hiloEscritor = threading.Thread(target=escritor)

hiloEscritor.start()
hiloLector.start()

hiloEscritor.join()
hiloLector.join()