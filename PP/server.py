import psutil
import time
import threading
import socket
import sys
import codecs
import os

srva = ''
srvb = ''
srvc = ''

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

def send_dgram(data, n):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
	sock.sendto(data, (MCAST_GRP, MCAST_PORT))

def file_size(file):
	file.seek(0, os.SEEK_END)
	return file.tell()

def console(conn, addr):
	try:
		while True:
			recv = conn.recv(1024)
			data = recv.decode('utf-8')
			if(len(data) > 0 and len(data) < 16):
				print(data, len(data))
				order, file = data.split(',')
				if(order == 'SEND'):
					conn.sendall(bytes('ACK','utf-8'))
					receiver(file, conn, addr)
					break
				elif(order == 'DOWN'):
					sender(file, conn, addr)
					break
			else:			
				break		
	finally:
		print ("Cerrando socket")
		
def sender(file, conn, addr):
	print('send')
	try:
		cont = []
		with open('rel.txt', "r+") as f:
			cont = f.readlines()

		for line in cont:
			name, s, a, b, c = line.split(',')
			if(name == file):
				print('found')
				break

		size = int(int(s) / 3)
		sres = int(int(s) % 3)

		print(str(size) + ',' + str(sres))
		
		with open(str(1), "rb") as f:
			f.seek(int(a))
			f.tell()
			chnka = f.read(size)
		with open(str(2), "rb") as f:
			f.seek(int(b))
			f.tell()
			chnkb = f.read(size)
		with open(str(3), "rb") as f:
			f.seek(int(c))
			f.tell()
			chnkc = f.read(size + sres)
		
		data = chnka + chnkb + chnkc
		
		conn.send(data)
		print('sent: ' + str(len(data)))
	finally:
		print ("Cerrando socket")
		conn.close()
		
def receiver(file, conn, addr):
	print('recv')
	try:
		data = b''
		chnk = bytearray(b'')
		i = 0
		while True:
			recv = conn.recv(1024)
			data = recv
			if(len(recv) == 0):
				break
			#print(len(data), i)
			#print(type(data), type(recv))
			i += 1
			chnk.extend(data)

		d = int(len(chnk) / 3)
		r = int(len(chnk) % 3)

		print('recv: '+str(len(chnk)) + ' ' + str(d) + ' ' + str(r))
		#write to distributed files
		sizes = []

		with open(str(1), "ab") as f:
			sizes.append(file_size(f))
			f.write(chnk[0:1*d])
			
		with open(str(2), "ab") as f:
			sizes.append(file_size(f))
			f.write(chnk[1*d:2*d])

		with open(str(3), "ab") as f:
			sizes.append(file_size(f))
			f.write(chnk[2*d:(3*d)+r])
		#write sizes relationship btween files
		with open('rel.txt', "a") as f:
			f.write(file + ',' + str(len(chnk)) + ',' + str(sizes[0]) + ',' + str(sizes[1]) + ',' + str(sizes[2]) + '\n')
				
	finally:
		print ("Cerrando socket")
			
# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('localhost', 8090)
print ("Empezando a levantar %s puerto %s" % server_address)
sock.bind(server_address)
sock.listen(1)

while True:
	conn, addr = sock.accept()
	print ("Conexion Aceptada")
	
	t = threading.Thread(target=console,args=[conn,addr])
	t.start()
