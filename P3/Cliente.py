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
        message = input()
        if message != "exit":
            sock.sendall(bytes(message,"utf-8"))
        else:
            sock.sendall(bytes(message,"utf-8"))
            break
 
finally:
    print ("Cerrando socket")
    sock.close()