import socket
import sys

def recev_file(addresses,nombres,numero):
    count = 0
    counter = 0
    archivos = [bytearray(b'') for x in range(numero)]
    while True:
        data, client_address = sock.recvfrom(200)
        count = 0
        if not data:
            counter += 1
            print(counter, numero)
            if counter == numero:
                break
        while client_address != addresses[count]:
            print (client_address, addresses[count])
            count += 1

        archivos[count].extend(data)

    count = 0
    sizes = []
    while count != numero:
        with open(nombres[count], "wb") as f:
            f.write(archivos[count])
        count += 1
    return "Archivos guardados"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)
print ("Direccion del servidor %s en el puerto %s" % server_address)
sock.bind(server_address)

numeroDeConexiones = 3
count = 0
address = []
names = []
while True:
    data, client_address = sock.recvfrom(200)
    info = data.decode("utf-8")
    address.append(client_address)
    names.append(info)
    count += 1
    if count == numeroDeConexiones:
        print("Comenzando a recivir datos")
        for x in range(numeroDeConexiones):
            sock.sendto(bytes("True",'utf-8'),address[x])
        mensaje = recev_file(address,names,numeroDeConexiones)
        print(mensaje)
        break