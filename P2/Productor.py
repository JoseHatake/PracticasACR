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
k = 100
h = 4	

mem_map = memorymap_open(s=n, t=h)
smp = Semaphore(1)
smc = Semaphore(0)
mtx = semaphore()

mtx.open(filename="mutex.txt", value=1, n=h)

def productor(t,c):
	i = 0
	chr = str(c)*n
	smp.acquire()
	while i < k:
		mtx.wait(t)
		mem_map[(t*n):(t+1)*n] = bytes(chr, 'utf-8')
		mtx.post(t)
		i += 1
	smc.release()

tp = []
tc = []

for i in range(0,h):
	t = threading.Thread(target=productor, args=[i,i])
	tp.append(t)
	t.start()

for i in range(0,h):
	tp[i].join()