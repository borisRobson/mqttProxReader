import sys
import kpreader as kpreader
import mqttHandler as mqtt
import dbhandler
import threading
import time
from time import sleep

exitFlag = 0

class myThread(threading.Thread):
	def __init__(self,threadID, name, method):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.method = method
	def run(self):
		while exitFlag == 0:
			print "Starting: " + self.name
			if self.method == "mqtt":
				mqtt.run()
			else:
				kpreader.run()
			print "Exiting: " + self.name

if __name__=="__main__":
	mqttThread = myThread(1, "mqttThread", "mqtt")
	readerThread = myThread(2, "readerThread", "reader")

	mqtt.init()
	kpreader.init()
	dbhandler.init()

	mqttThread.start()
	readerThread.start()

	try:
		while True:
			sleep(1)
	except KeyboardInterrupt:
		pass
	finally:
		mqtt.quit()
		kpreader.quit()

print "exiting main thread"
exitFlag = 1
sys.exit()
	

