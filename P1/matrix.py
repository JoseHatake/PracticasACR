import threading as thr
import random as rnd
import numpy as np
#import os version para windowsn
import multiprocessing

#a = 67		# A's rows
#b = 6		# A cols, B rows
#c = 67		# C cols

print("Ingresar el numero de filas de la primera matriz")
a = input()
print("Ingresar el numero de columnas y filas compartidas entre matrices")
b = input()
print("Ingresar el numero de columnas de la segunda matriz")
c = input()

RESULT = [a,c]	# R[Ar X Bc]

print("Ingresar el numero de hilos que se utilizaran para procesar")
USR = input()
SYS = multiprocessing.cpu_count()

if(a<=USR):
	exit()

def Final(A, B, c, Br, Bc):
	i = 0
	for v in A:
		MR = []
		for col in range(0,Bc):
			MR.append(np.dot(v, ColAt(B, Br, col)))
		RESULT[c+i] = MR
		i += 1

def ColAt(M, r, c):
	vr = []
	for i in range(0, r):
		vr.append(M[i,c])
	return vr

#A = the ROW list; n=thread, t=rows per thread; Br = B's rows; Bc = B's cols; Sc = system threads
def Worker(A, B, n, t, c, Br, Bc):
	t = t / SYS
	r = t % SYS
	threads = [int(t)]
	counter = int(t)
	C = [SYS]
	
	rpt = int(t)
	
	print("THREAD:",n)
	for v in A:
		print(v)
	
	for i in range (SYS):
		C = []
		for j in range (0, rpt):
			C.append(A[rpt*i+j])
		tid = thr.Thread(target=Final, args=(C, B, (rpt*i)+c, Br, Bc))
		threads.append(tid)
		tid.start()
		tid.join()
		
		
def Fill(a,b,c):
	A = np.zeros((a,b))
	B = np.zeros((b,c))
	
	for i in range(a):
		for j in range(b):
			A[i,j] = rnd.randrange(0, 6)
	
	for i in range(b):
		for j in range(c):
			B[i,j] = rnd.randrange(0, 6)

	return A, B
	
A, B = Fill(a,b,c)
RESULT = np.zeros((a,c))

t = a / USR	#ROWS / USER THREADS
r = a % USR	#REMAINDER ROWS
C = [USR]
threads = [int(t)]
counter = int(t)

rpt = int(t)

print(A, "\n")

for i in range(USR): #desde 0 hasta: N threads definidos por el user
	C = [] #declara una lista vacia
	for j in range (0, rpt): #desde 0 hasta: K filas asignadas por thread
		C.append(A[rpt*i+j])  #anade a la lista las proximas K*N filas
	print("MAIN:",rpt*i)
	tid = thr.Thread(target=Worker, args=(C, B, i, rpt, rpt*i, b, c)) #incializa el thread
	threads.append(tid)
	tid.start()
	tid.join()
	
C = []
for k in range(0, r): #desde 0 hasta N filas restantes
	C.append(A[a+k-r]) #anade N filas a la lista
print("EXTRA:",a-r)
tid = thr.Thread(target=Final, args=(C, B, a-r, b, c))
tid.start()
tid.join()

print(RESULT)	