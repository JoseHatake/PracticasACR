import threading as thr
import random as rnd
import numpy as np
#import os
import multiprocessing

print("Ingresar el numero de filas de la primera matriz")
a = int(input())
print("Ingresar el numero de columnas y filas compartidas entre matrices")
b = int(input())
print("Ingresar el numero de columnas de la segunda matriz")
c = int(input())

RESULT = [a,c]	# R[Ar X Bc]

print("Ingresar el numero de hilos que se utilizaran para procesar")
USR = input()
SYS = multiprocessing.cpu_count()

if(a<=USR):
	exit()

def Final(A, B, c, Br, Bc):
	i = 0
	#for v in A:
	#	print(v)
	for v in A:
		MR = []
		for col in range(0,Bc):
			MR.append(np.dot(v, ColAt(B, Br, col)))
		print(c+i)
		RESULT[c+i] = MR
		i += 1

def ColAt(M, r, c):
	vr = []
	for i in range(0, r):
		vr.append(M[i,c])
	return vr

#A = the ROW list; n=thread, a=rows per thread; Br = B's rows; Bc = B's cols; Sc = system threads
def Worker(A, B, n, a, c, Br, Bc):
	t = int(a / SYS)
	r = int(a % SYS)
	threads = [int(t)]
	counter = int(t)
	C = [SYS]
	
	
	for i in range (SYS):
		C = []
		for j in range (0, t):
			C.append(A[t*i+j])
		tid = thr.Thread(target=Final, args=(C, B, (t*i)+c, Br, Bc))
		print("THREAD:",(t*i)+c)
		threads.append(tid)
		tid.start()
		tid.join()
	
	C = []
	for k in range(0, r): #desde 0 hasta N filas restantes
		C.append(A[a+k-r]) #anade N filas a la lista
	print("THR EXTRA:",a*(n+1)-r)
	tid = thr.Thread(target=Final, args=(C, B, a*(n+1)-r, Br, Bc))
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

t = int(a / USR)	#ROWS / USER THREADS
r = int(a % USR)	#REMAINDER ROWS
C = [USR]
threads = [int(t)]
counter = int(t)

rpt = int(t)

for i in range(USR): #desde 0 hasta: N threads definidos por el user
	C = [] #declara una lista vacia
	for j in range (0, rpt): #desde 0 hasta: K filas asignadas por thread
		C.append(A[rpt*i+j])  #anade a la lista las proximas K*N filas
	print("MAIN:",rpt*i+j, t, r)
	tid = thr.Thread(target=Worker, args=(C, B, i, rpt, rpt*i, b, c)) #incializa el thread
	threads.append(tid)
	tid.start()
	tid.join()
	
C = []
for k in range(0, r): #desde 0 hasta N filas restantes
	C.append(A[a+k-r]) #anade N filas a la lista
tid = thr.Thread(target=Final, args=(C, B, a-r, b, c))
tid.start()
tid.join()

np.savetxt(fname="results.txt",X=RESULT,fmt='%d')