import socket
import asyncio
import cmd, sys
import threading as thread
from queue import Queue

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
			locks[sel].put(0)
		
	def do_stop(self, arg):
		'Stops client monitor: STOP 10'
		sel = int(arg.split(' ')[0])
		if(sel >= len(locks)):
			print('Numero de clientes conectados:', sel)
		else:
			locks[sel].put(1)
		
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

def servicio(conn,client_address,queue):
	try:
		print ("Conexion desde", client_address)
		# Recibe los datos en trozos y reetransmite
		while True:
			num = queue.get()
			while True:
				if(num == 0):
					sent = conn.sendall(bytes('show',"utf-8"))
					recv = conn.recv(1024)
					data = recv.decode('utf-8')
					if(len(data) > 0 and queue.empty()):
						print ("Cliente: " + str(client_address[0]) + " Recibido: " + data + '\r')
					else:
						break
				else:
					break
	finally:
		# Cerrando conexion
		conexiones.remove(conn)
		locks.remove(queue)
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
	queue = Queue()
	locks.append(queue)
	
	t = thread.Thread(target=servicio,args=[conn,addr,queue])
	t.start()
	
	
	
