import socket
import sys
import threading as thread

conexiones = []

def servicio(connection,client_address):
    numeroServicio = 0
    try:
        print ("Concexion desde", client_address)
        conexiones[0] += 1
        numeroServicio = conexiones[0]
        # Recibe los datos en trozos y reetransmite
        while True:
            data = connection.recv(1024)
            info = data.decode("utf-8")
            if info != "exit":
                print ("Cliente (",numeroServicio,"): ",client_address," - Recibido : ", info)
            else:
                print ("Cerrando la conexion con: ", client_address)
                break
    finally:
        # Cerrando conexion
        connection.close()

# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('localhost', 10000)
print ("Empezando a levantar %s puerto %s" % server_address)
sock.bind(server_address)
sock.listen(1)

conexiones.append(0)

while True:
    # Esperando conexion
    print ("Esperando para conectarse")
    connection, client_address = sock.accept()

    t = thread.Thread(target=servicio,args=[connection,client_address])
    t.start()
