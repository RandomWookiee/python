import zmq
import time
from multiprocessing import Process

class Proc():

	def __init__(self,name,master=False):
		self.context = zmq.Context()
		self.master = master
		self.name = name
		self.address = "tcp://127.0.0.1:21000"

		self.run = True
		if self.master:
			self.socket = self.context.socket(zmq.REP)
			self.socket.bind(self.address)
			print "bound to ", self.address
		else:
			self.socket = self.context.socket(zmq.REQ)
			self.socket.connect(self.address)
			print "sending to ", self.address
		

	def __del__(self):
		self.run = False

	def recv(self):
		print "Recv method called"
		while self.run:
			message = self.socket.recv()
			print "Received -> ", message
			self.socket.send("Response to %s"%message)
		print "shutdown has started"

	def send(self):
		i = 0
		while self.run:
			message = "sending from %s message number %s"%(self.name,i)
			print "sending -> ", message
			self.socket.send(message)
			message = self.socket.recv()
			print "response -> ", message
			i = i + 1
		print "giving up on this"


def server():
	p = Proc("master server",True)
	p.recv()

def client(name):
	p = Proc(name,False)
	p.send()

if __name__ == '__main__':
	m = Process(target=server)
	m.start()

	time.sleep(1)
	
	c = Process(target=client,args=('first client',))
	c.start()

	time.sleep(30)
	c.terminate()
	m.terminate()
		

