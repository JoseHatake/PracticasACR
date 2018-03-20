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
        print("Mensaje a enviar")
        #message = input()
        message = "Hola como estas"
        if message != "exit":
            sock.sendall(bytes(message,"utf-8"))
        else:
            sock.sendall(bytes(message,"utf-8"))
            break
            
	print("Mensaje a enviar")
	message = input()
		
	while True:
		cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
		cpu_logical = psutil.cpu_count()
		cpu_physical = psutil.cpu_count(logical=False)
		cpu_states = psutil.cpu_stats()
		cpu_freq = psutil.cpu_freq()
		
		mem = psutil.virtual_memory()
		diu = psutil.disk_io_counters(perdisk=True)

		users = psutil.users()
		
		sock.sendall(bytes(str(cpu_usage),"utf-8"))
		sock.sendall(bytes(str(cpu_logical),"utf-8"))
		sock.sendall(bytes(str(cpu_physical),"utf-8"))
		sock.sendall(bytes(str(cpu_states),"utf-8"))
		sock.sendall(bytes(str(cpu_freq),"utf-8"))
		sock.sendall(bytes(str(mem),"utf-8"))
		sock.sendall(bytes(str(diu),"utf-8"))
		sock.sendall(bytes(str(users),"utf-8"))
		
		time.sleep(1)
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
