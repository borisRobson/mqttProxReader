import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import json
from datetime import datetime
from dbhandler import getUser
from mqttHandler import publish_event
from configparse import read_config


#read value on rising clock pulse
#fill data array
def data_callback(channel):
	if GPIO.input(data_pin):
		data.append(0)
	else:
		data.append(1)

def init():
	print ("init reader")
	global data_pin, clock_pin,rled_pin,gled_pin
	global DOOR_NUM
	DOOR_NUM = 1
	GPIO.setwarnings(False)

	#configure pinout and board-mode
	config = read_config('config.ini', 'hardware')
	data_pin = int(config.get('data_pin'))
	clock_pin = int(config.get('clock_pin'))
	rled_pin = int(config.get('rled_pin'))
	gled_pin = int(config.get('gled_pin'))

#	data_pin = int(dbdata_pin)
#	clock_pin = int(dbclock_pin)
#	rled_pin = int(dbrled_pin)
#	gled_pin = int(dbgled_pin)
#	print ("pins: {0}, {1}, {2}, {3}".format(data_pin,clock_pin, rled_pin, gled_pin))

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(data_pin, GPIO.IN)
	GPIO.setup(clock_pin, GPIO.IN)	

	#set initial output state to low
	outputs = (rled_pin, gled_pin)
	GPIO.setup(rled_pin, GPIO.OUT)
	GPIO.setup(gled_pin, GPIO.OUT)
	GPIO.output(outputs, GPIO.LOW)


def parseKeypad(data):
	print("parsing...")
	i = 0
 	c = data[i]
	#cycle through data until first '1' bit	
	while c != 1:
		i += 1
		c = data[i]

	byte_len = 5
	value_len = 4
	data_byte = []
	reader_value = []

	#convert binary to int
	while i != len(data):	
		#section off data array into bytes
		data_byte = data[i : i +value_len]
		out = 0
		index = len(data_byte)
		#reader is lsb first
		#start at end and work backwords
		while index != 0:
			out = (out << 1) | data_byte[index -1]
			index -= 1

		#read next byte
		i += byte_len
		reader_value.append(out)

	reader_index = 0
	stx = 0
	etx = 0

	#get index of start and stop bits
	while reader_index != len(reader_value):
		if etx != 0:
			break
		if reader_value[reader_index] == 11:
			stx = reader_index + 1
		if reader_value[reader_index] == 15:
			etx = reader_index
		reader_index += 1

	#concat int array to string
	token = ''.join(str(x) for x in reader_value[stx:etx])
	data = []
	return token

#light selected lef for 1s
def light_led(led):
	GPIO.output(led, GPIO.HIGH)
	sleep(1)
	GPIO.output(led, GPIO.LOW)


def run():
	global data
	global read
	read = True
	print("run pins: {0},{1},{2},{3}".format(data_pin ,clock_pin, rled_pin, gled_pin))

	while read:
		data = []
		#remove any existing edge_detect,
		#this allows the program to repeat
		GPIO.remove_event_detect(clock_pin)
		#block until level change detected
		GPIO.wait_for_edge(clock_pin, GPIO.RISING)
		GPIO.add_event_detect(clock_pin, GPIO.RISING, callback=data_callback)
		#wait for pulses to finish
		sleep(0.5)	
		token = parseKeypad(data)
		user = 	getUser(token)
		topic = "/doors/accessevents"
		msg = ""
		#if getUser returns nothing, token not recognised
		if len(user) == 0:
			msg = ("token id: {0} not recognised @ door no. {1}").format(str(token), str(DOOR_NUM))
			publish_event(topic,msg)
			print(msg)
			light_led(rled_pin)
		#else get username and light green led
		else:
			name = user[0]
			time = datetime.now().time()
			msg = "{0} Accessed door no. {1}  @ {2}".format(name,str(DOOR_NUM), time)
			publish_event(topic,msg)
			print(msg)
			light_led(gled_pin)

	
def quit():
	print("GPIO Cleanup")
	read = False
#	GPIO.cleanup()	
	return

	

	

	

	
	
