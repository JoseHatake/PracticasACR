import threading
import time
import mmap
from asyncio import Semaphore

class semaphore:
	def __init__(self):
		self.map = []
		self.sem = []
		
	def open(self, filename, value, n):
		with open(filename, "wb") as fp:
			for x in range(0,n):
				fp.write(bytes(str(value), 'utf-8'))
		
		with open(filename, "r+b") as fp:
			self.map = mmap.mmap(fp.fileno(), 0)
			
			for x in range(0,n):
				self.sem.append(Semaphore(int(self.map[x])))
		
	def wait(self, t):
		self.sem[t].acquire()
		self.map[t:t+1] = bytes(str('0'), 'utf-8')
		
	def post(self, t):
		self.sem[t].release()
		self.map[t:t+1] = bytes(str('1'), 'utf-8')
		
def memorymap_open(s, t):
	mm = [[y for x in range(s)]for y in range (t)]

	f = open("hello.txt", "wb")
	for x in range(0,t):
		for y in range (0,s):
			f.write(bytes(str(mm[x][y]), 'utf-8'))

	f.close()
	f = open("hello.txt", "r+b")
	return mmap.mmap(f.fileno(), 0)

n = 20
k = 10000
h = 3
m = 4

mem_map = memorymap_open(s=n, t=h)
#smp = Semaphore(1)
#smc = Semaphore(0)
buff0 = []
buff1 = []
buff2 = []

mtx = semaphore()
smp = semaphore()
smc = semaphore()

smp.open(filename="producer.txt", value=1, n=n)
smc.open(filename="consumer.txt", value=0, n=n)
mtx.open(filename="mutex.txt", value=1, n=m)

def consumidor(t):
	#f = open(str(t) + '.txt', 'w+')
	tmp = ""
	i = 0
	smc.wait(t)
	while i < k:
		mtx.wait(t)
		#print("Consumer: " + str(mem_map[(t*n):(t+1)*n]))
		#f.write(str(mem_map[(t*n):(t+1)*n], 'utf-8') + '\n')
		tmp = str(mem_map[(t*n):(t+1)*n], 'utf-8')
		if tmp[0] == "0":
			buff0.append(tmp + "\n")
		elif tmp[0] == "1":
			buff1.append(tmp + "\n")
		else:
			buff2.append(tmp + "\n")
		mtx.post(t)
		i += 1
	smp.post(t)

def productor(t,c):
	i = 0
	chr = str(c)*n
	smp.wait(t)
	while i < k:
		t = (t + 1) % 3
		mtx.wait(t)
		mem_map[(t*n):(t+1)*n] = bytes(chr, 'utf-8')
		mtx.post(t)
		i += 1
	smc.post(t)

tp = []
tc = []

for i in range(0,h):
	t = threading.Thread(target=productor, args=[i,i])
	tp.append(t)
	t.start()
	
for i in range(0,h):
	t = threading.Thread(target=consumidor, args=[i])
	tc.append(t)
	t.start()

for i in range(0,h):
	tp[i].join()

for i in range(0,h):
	tc[i].join()

f1 = open(str(0) + '.txt', 'w+')
f2 = open(str(1) + '.txt', 'w+')
f3 = open(str(2) + '.txt', 'w+')

for x in buff0:
	f1.write(x)
for x in buff1:
	f2.write(x)
for x in buff2:
	f3.write(x)

f1.close()
f2.close()
f3.close()
