import sys
import kpreader as kpreader
import mqttHandler as mqtt
import dbhandler
import threading
import time
from time import sleep

exitFlag = 0

class msgThread(threading.Thread):
	def __init__(self,threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name	
	def run(self):
		while exitFlag == 0:
			print "Starting: " + self.name
			mqtt.run()
			print "Exiting: " + self.name + " " + str(exitFlag)

class ioThread(threading.Thread):
	def __init__(self, threadId, name):
		threading.Thread.__init__(self)
		self.threadID = threadId
		self.name = name
	def run(self):
		while exitFlag == 0:
			print "Starting: " +self.name
			kpreader.run()
			print "Exiting " + self.name
		
			

if __name__=="__main__":
	mqttThread = msgThread(1, "mqttThread")
	readerThread = ioThread(2, "readerThread")

	mqtt.init()
	kpreader.init()
	dbhandler.init()

	mqttThread.daemon = True
	readerThread.daemon = True

	readerThread.start()
	mqttThread.start()

	try:
		while True:
			sleep(1)
	except KeyboardInterrupt:
		pass
	finally:
		exitFlag = 1
		mqtt.quit()
		kpreader.quit()	

print "exiting main thread"
#kpreader.quit()
#ymqtt.quit()
sys.exit()
	

