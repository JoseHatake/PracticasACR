import socket
import asyncio
import cmd, sys
import threading as thread

conexiones = []
locks = []

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
			if(not locks[sel].locked()):
				print('Recibiendo información del ID:', sel)
				print(locks[sel])
				locks[sel].acquire()
				print(locks[sel])
			else:
				print('El hilo no está bloqueado:', sel)
		
	def do_stop(self, arg):
		'Stops client monitor: STOP 10'
		sel = int(arg.split(' ')[0])
		if(sel >= len(locks)):
			print('Numero de clientes conectados:', sel)
		else:
			if(locks[sel].locked()):
				print('Bloqueando información del ID:', sel)
				locks[sel].release()
				print(locks[sel].locked())
			else:
				print('El hilo está bloqueado:', sel)
		
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

def servicio(conn,client_address,lock):
	try:
		print ("Conexion desde", client_address)
		
		# Recibe los datos en trozos y reetransmite
		while True:
			recv = conn.recv(1024)
			data = recv.decode('utf-8')
			if(len(data) > 0 and not lock.locked()):
				if data != "exit":
					print ("Cliente: " + str(client_address[0]) + " Recibido: " + data)
				else:
					print ("Cerrando la conexion con: ", client_address)
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
	lock = asyncio.Semaphore(1)
	locks.append(lock)
	print(lock.locked())
	
	t = thread.Thread(target=servicio,args=[conn,addr,lock])
	t.start()
	
	
	
	
	
	
	
	
	
