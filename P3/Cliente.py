import psutil
import time
import socket
import sys
 
# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('localhost', 10000)
print ("Conectando a %s puerto %s" % server_address)
sock.connect(server_address)

print ('-' + "Hi! This is a text-based GUI!".center(78, 'h') + '-')
print ('+' + "-" * 78 + '+')
print ('|' + "OPTIONS".center(78) + '|')
print ('+' + "-" * 78 + '+')
print ('|' + "1 - Quit".center(78) + '|')
for i in range(1, 7):
    print ('|' + " " * 78 + '|')
print ('+' + "-" * 78 + '+')

try:
	while True:
		recv = sock.recv(1024)
		data = recv.decode('utf-8')
		infoCompleta = ""
		if(len(data) > 0):
			cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
			cpu_logical = psutil.cpu_count()
			cpu_physical = psutil.cpu_count(logical=False)
			cpu_states = psutil.cpu_stats()
			cpu_freq = psutil.cpu_freq()
			
			mem = psutil.virtual_memory()
			diu = psutil.disk_io_counters(perdisk=True)
			users = psutil.users()
			pids = psutil.pids()
			serv = 20 #modificar para windows
			
			infoCompleta = str(cpu_usage) + "&"
			infoCompleta += str(mem.percent) + "&"
			infoCompleta += str(len(pids)) + "&"
			infoCompleta += str(serv)


			sock.sendall(bytes(str(infoCompleta),"utf-8"))

			#sock.sendall(bytes(str(cpu_usage),"utf-8"))
			#sock.sendall(bytes(str(cpu_logical),"utf-8"))
			#sock.sendall(bytes(str(cpu_physical),"utf-8"))
			#sock.sendall(bytes(str(cpu_states),"utf-8"))
			#sock.sendall(bytes(str(cpu_freq),"utf-8"))
			#sock.sendall(bytes(str(mem),"utf-8"))
			#sock.sendall(bytes(str(diu),"utf-8"))
			#sock.sendall(bytes(str(users),"utf-8"))
			
			time.sleep(5)
		else:
			continue

finally:
    print ("Cerrando socket")
sock.close()

psutil.cpu_times()

cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
cpu_logical = psutil.cpu_count()
cpu_physical = psutil.cpu_count(logical=False)

cpu_states = psutil.cpu_stats()
cpu_freq = psutil.cpu_freq()

mem = psutil.virtual_memory()
diu = psutil.disk_io_counters(perdisk=True)

users = psutil.users()

pids = psutil.pids()

for pid in pids:
	print(psutil.Process(pid).name())
