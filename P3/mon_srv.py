import socket
import asyncio
import cmd, sys
import threading as thread
from queue import Queue

conexiones = []
locks = []

LOK = asyncio.Semaphore(1)

class ServerShell(cmd.Cmd):
	intro = 'Server Ready, type help for a list of permitted commands.\n'
	prompt = 'SERVER>>'
	file = None

	def do_list(self, arg):
		'A list of current connected clients: LIST'
		for conn in conexiones:
			print('Conn: '+str(conexiones.index(conn))+' '+str(conn.getsockname())+'\n')
		
	def do_show(self, arg):
		'Shows client monitor: SHOW 10'
		sel = int(arg.split(' ')[0])
		if(sel >= len(locks)):
			print('Numero de clientes conectados:', sel)
		else:
<<<<<<< HEAD
			if(not locks[sel].acquire(blocking=False)):
				print('Recibiendo información del ID:', sel)
				objSem = locks[sel]
				print(objSem.acquire(blocking=False))
				objSem.acquire(blocking=True)
				print(objSem.acquire(blocking=False))
			else:
				print('El hilo no está bloqueado:', sel)
=======
			locks[0].put(0)
>>>>>>> 19f1281d3d8953c8a1dd3cd29a54bdc5eb490182
		
	def do_stop(self, arg):
		'Stops client monitor: STOP 10'
		sel = int(arg.split(' ')[0])
		if(sel >= len(locks)):
			print('Numero de clientes conectados:', sel)
		else:
<<<<<<< HEAD
			if(locks[sel].acquire(blocking=False)):
				print('Bloqueando información del ID:', sel)
				locks[sel].release()
				print(locks[sel].acquire(blocking=False))
			else:
				print('El hilo está bloqueado:', sel)
=======
			locks[0].put(1)
>>>>>>> 19f1281d3d8953c8a1dd3cd29a54bdc5eb490182
		
	def do_exit(self, arg):
		'Ends client connection: END 10'
		sel = int(arg.split(' ')[0])
		if(sel >= len(locks)):
			print('Numero de clientes conectados:', sel)
		else:
			conexiones.remove(conn)
			locks.remove(lock)
			conn.close()


def console():
	ServerShell().cmdloop();

def servicio(conn,client_address):
	try:
		print ("Conexion desde", client_address)
		flag = True
		# Recibe los datos en trozos y reetransmite
		while True:
<<<<<<< HEAD
			recv = conn.recv(1024)
			data = recv.decode('utf-8')
			
			if flag != lock.acquire(blocking=False):
				print(lock.acquire(blocking=False))
			flag = lock.acquire()
			if(len(data) > 0 and lock.acquire(blocking=False)):
				if data != "exit":
					print ("Cliente: " + str(client_address[0]) + " Recibido: " + data)
=======
			num = locks[0].get()
			while True:
				if(num == 0):
					recv = conn.recv(1024)
					data = recv.decode('utf-8')
					if(len(data) > 0 and locks[0].empty()):
						print ("Cliente: " + str(client_address[0]) + " Recibido: " + data)
					else:
						break
>>>>>>> 19f1281d3d8953c8a1dd3cd29a54bdc5eb490182
				else:
					break
	finally:
		# Cerrando conexion
		conexiones.remove(conn)
		locks.remove(lock)
		conn.close()

#Crea thread de interaccion
t = thread.Thread(target=console)
t.start()
		
# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('localhost', 10000)
print ("Empezando a levantar %s puerto %s" % server_address)
sock.bind(server_address)
sock.listen(1)

while True:
	# Esperando conexion
	print ("Esperando para conectarse")
	conn, addr = sock.accept()
	#Agregar conexion a lista de conexiones vigentes
	conexiones.append(conn)
	#Agregar nuevo candado por cliente conectado
<<<<<<< HEAD
	lock = thread.Semaphore(1)
	locks.append(lock)
	print(lock.acquire(blocking=False))
=======
	locks.append(Queue())
>>>>>>> 19f1281d3d8953c8a1dd3cd29a54bdc5eb490182
	
	t = thread.Thread(target=servicio,args=[conn,addr])
	t.start()
	
	
	
	
	
	
	
	
	