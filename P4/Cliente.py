import socket
import sys

def send_file(file):
    with open(file, 'r+b') as f:
        while True:
            cont = f.read(200)
            sock.sendto(cont,servidor_address)
            if not cont:
            	print(cont)
            	return "Archivo enviado!"

#Se instancia el servidor y se publica para que se le puedan enviar paquetes
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_address = ('localhost', int(sys.argv[1]))
print ("Direccion del cliente %s en el puerto %s" % client_address)
sock.bind(client_address)
#Se instancia el servidor y se publica para que se le puedan enviar paquetes

servidor_address = ('localhost', 10000)

print("Ruta del archivo a mandar al servidor: ")
archivo = input()
aux = archivo.split('/')
nombre = aux[len(aux)-1]
sock.sendto(bytes(nombre ,'utf-8'),servidor_address)
data, servidor_address = sock.recvfrom(200)
info = data.decode("utf-8")
if info == "True":
    mensaje = send_file(archivo)
    print(mensaje)
    