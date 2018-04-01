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

			time.sleep(1)
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
