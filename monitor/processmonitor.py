import os
import sys
import threading
import time
import random

SYS_FOLDER="/proc"

RED="\x1B[31;40m%s\x1B[0m"
CYAN="\x1B[36;40m%s\x1B[0m"
BLUE="\x1B[34;40m%s\x1B[0m"
GREEN="\x1B[32;40m%s\x1B[0m"
CLEAR_BUFFER="\x1b[2J\x1b[H"
	


def cprint(output):
 	sys.stderr.write(CLEAR_BUFFER)
 	sys.stderr.flush()
	for o in output:
 		sys.stdout.write("%s"%o)
 	sys.stdout.write("\n")
 	sys.stdout.flush()


# class SystemThread(threading.Thread):
# 	def __init__(self,name,delay=1):
# 		threading.Thread.__init__(self)
# 		self.name=name
# 		self.delay=delay
# 		self.finished=False
# 	def completed(self):
# 		raise NotImplementError, "Parent Class please implement in child"
# 	def run(self):
# 		raise NotImplementError, "Parent Class please implement in child"
# 	def stop(self):
# 		raise NotImplementError, "Parent Class please implement in child"
# 	def __str__(self):
# 		return "%s %s %s"%(self.name,self.delay,self.finished)



# class Reader(threading.Thread):
# 	def __init__(self,name,delay=1):
# 		threading.Thread.__init__(self)
# 		self.name=name
# 		self.delay=delay
# 		self.finished=False
# 		self.loop_count = 0
# 	def completed(self):
# 		return self.finished
# 	def run(self):
# 		while not(self.finished):
# 			self.loop_count += 1
# 			time.sleep(self.delay)
# 			if self.loop_count > 20:
# 				self.stop()
# 	def stop(self):
# 		self.finished = True
# 	def write(self):
# 		sys.stdout.write("\r%s %s %s"%(self.name,self.delay,self.finished))
# 	def __str__(self):
# 		return "%s %s %s %s"%(self.name,self.delay,self.finished,self.loop_count)				

# class Master(SystemThread):
# 	def __init__(self,name,delay=1):
# 		SystemThread.__init__(self,name,delay)
# 		self.threads=[]
# 	def completed(self):
# 		return self.finished and len([t for t in self.threads if t.completed()]) == len(self.threads)
# 	def __str__(self):
# 		return ""
# 	def run(self):
# 		if self.threads > 0:
# 			for t in self.threads:
# 				t.start()
# 			while not(self.completed()):
# 				output = []
# 				num_threads=len(self.threads)
# 				num_complete=len([t for t in self.threads if t.completed()])
# 				output.append("\r" + CYAN%self.name + " -> ")
# 				output.append(" number_threads=" + GREEN%num_threads)
# 				output.append(" active=" + GREEN%(num_threads-num_complete))
# 				output.append(" complete="+GREEN%num_complete)
# 				if (num_threads-num_complete) > 0:
# 					output.append("\n" + BLUE%"-----------------------------------------------")
# 				completed_list = []			
# 				for t in self.threads:
# 					if not(t.completed()):
# 						output.append("\n%s"%t)
# 					else:
# 						completed_list.append(t.name)
# 				if len(completed_list) > 0:
# 					output.append("\n" + BLUE%"-----------------------------------------------")
# 					for c in completed_list:
# 						output.append("\n%s"%c)
# 				if num_complete == num_threads or num_threads == 0:
# 					self.stop()
# 				if (num_threads == 1 and self.threads[0].name == "Process Reader - Owner"):
# 					self.stop()
# 				display(output)
# 				time.sleep(self.delay)
# 	def addthread(self,t):
# 		self.threads.append(t)
# 	def stop(self):
# 		for t in self.threads:
# 			t.stop()		
# 		self.finished = True

class process(threading.Thread):

	def __init__(self, proc_id, folder=None):
		threading.Thread.__init__(self)
		
		self.folder = folder #will look to use for checking for tasks

		self.proc_id = proc_id
		self.files = []
		self.data = {}
		
		self.delay = 1
		self.complete = False

	def stop(self):
		self.complete = True

	def run(self):
		while not self.complete:
			time.sleep(self.delay)
 		return True

	def addfiles(self, f):
		self.files.append(f)

	def __str__(self):
		#return "\n".join(s for s in self.files)
		return "%s"%self.proc_id


class ProcessMonitor(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

		self.folder = "/proc"
		self.process_list = ["cmdline"]#,"environ", "fd", "limits","mounts"]

		self.procs = {}

		self.completed = False

		self.depth = 1

		self.count = 0

	def stop(self):
		self.complete = True

	def run(self):

		self.execute()

		while self.count < 240:
			self.display()
			time.sleep(1)

		self.terminate()

 		return True

	def load(self):
		depth = 0
		for root, dirs, files in os.walk(self.folder,1):
			for f in files:
				if f in self.process_list:
					i = root.split(os.path.sep)
					if len(i) == 2:
						i = -1 #Root process
					else:
						i = i[2]
					if i not in self.procs:
   						self.procs[i] = process(i)
   					self.procs[i].addfiles(os.path.join(root, f))

   					depth = root.count(os.path.sep)

   					if depth > self.depth:
   						break;


   	def execute(self):
   		for k in self.procs.keys():
   			self.procs[k].start()

   	def terminate(self):
   		for k in self.procs.keys():
   			print "stoping -> ", k
   			self.procs[k].stop()
   			del self.procs[k]
   		self.stop()

   	def display(self):
   		data = ["-- I am major process  %s--\n"%self.count]
   		for f in self.procs:
   			data.append("%s\t"%self.procs[f])
   		self.count =  self.count + 1
   		cprint(data)


if __name__ == '__main__':
	#print "I am a chicken"
	#contents = get_contents(SYS_FOLDER)
	#files = []
	#folders = []
	#for c in contents:
	#	e = "%s/%s"%(SYS_FOLDER,c)
	#	if os.path.isfile(e):
	#		files.append(e)
	#	if os.path.isdir(e):
	#		folders.append(e)

	#print folders
	#Master = Master("Da-Master",1)
	#Master.addthread(ProcessReader("Process Reader - Owner", 1))
	#for i in range(0,2):
	#	Master.addthread(Reader("Thread test - %s"%i, 20))		
	#Master.start()
	pm = ProcessMonitor()
	pm.load()
	
	pm.start()
	#time.sleep(12)
	#pm.terminate()
	
