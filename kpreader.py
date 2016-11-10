import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import json
from datetime import datetime

def data_callback(channel):
	if GPIO.input(data_pin):
		data.append(0)
	else:
		data.append(1)

def init():
	print ("init reader")
	global data_pin, clock_pin
#	data = []
	#configure pinout and board
	data_pin = 14
	clock_pin = 2
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(data_pin, GPIO.IN)
	GPIO.setup(clock_pin, GPIO.IN)
#	GPIO.add_event_detect(clock_pin, GPIO.RISING, callback=data_callback)

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

def run():
	global data
	while True:
		data = []
		GPIO.remove_event_detect(clock_pin)
		GPIO.wait_for_edge(clock_pin, GPIO.RISING)
		GPIO.add_event_detect(clock_pin, GPIO.RISING, callback=data_callback)
		sleep(0.75)	
		token = parseKeypad(data)
		print token
	
def quit():
	GPIO.cleanup()	
	

	

	

	
	
