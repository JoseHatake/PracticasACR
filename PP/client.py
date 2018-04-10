import time
import socket
import sys

def send_file(file):
	with open(file, 'r+b') as f:
		while True:
			cont = f.read(1024)
			if not cont:
				break
			sock.send(cont)
			print('sent'+str(len(cont)))
 
# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket en el puerto cuando el servidor estÃ© escuchando
server_address = ('localhost', 8090)
print ("Conectando a %s puerto %s" % server_address)
sock.connect(server_address)

ORDER = 'DOWN'
#file = 'pr3.pdf'
file = 'tesla.jpg'

if(ORDER == 'SEND'):
	try:
		sock.send(bytes(ORDER + ',' + file ,'utf-8'))
		print('set send order')
		while True:
			recv = sock.recv(1024)
			data = recv.decode('utf-8')
			if(len(data) > 0):
				print(data)
				if(data[0:3] == 'ACK'):
					send_file(file)
					break
			else:
				break
	finally:
		print ("Cerrando socket")
		
elif(ORDER == 'DOWN'):
	data = b''
	chnk = bytearray(b'')
	sock.send(bytes(ORDER + ',' + file,'utf-8'))
	
	while True:
		recv = sock.recv(1024)
		data = recv
		if(len(recv) == 0):
			break
		chnk.extend(data)
		
	print(len(chnk))
	with open('recv_' + file, "wb") as f:
		f.write(chnk)
	