import os.path as path

file = "Resultado.txt"
cadena = "Esta es la cadena que tiene que guardar el archivo"

if path.exists(file):
	print "Existe"
	f = open(file,"a")
	f.write(cadena)
	f.close()
else:
	print "No existe"
	f = open(file,"w")
	f.write(cadena)
	f.close()