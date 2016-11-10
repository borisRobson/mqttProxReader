import paho.mqtt.client as mqtt
from configparse import read_mqtt_config
import json
from datetime import datetime
import uuid

def on_connect(client, userdata, flags, rc):
	print "Connected to mqtt broker: " + str(rc)
	mqttc.subscribe("/users/userAdded",1)
	

def on_publish(client, userdata, mid):
	print "Message published"

def on_subscribe(mosq, obj, mid, granted_qos):
	print("subscribed to topics")

def on_message(mosqq, obj, msg):
	print msg.payload


def init():
	print ("init mqtt")
	global mqttc
	MQTT_KEEPALIVE_INTERVAL = 5
	MQTT_TOPICS = [('/users/userAdded',1),('/users/userRemoved',1),('/users/userUpdated',1)]
	#create new instance of client
	uid = uuid.uuid1()
	#print uid
	mqttc = mqtt.Client(client_id=str(uid), clean_session=False)
#	mqttc = mqtt.Client()

	#assign callbacks
	mqttc.on_publish = on_publish
	mqttc.on_connect = on_connect
	mqttc.on_subscribe = on_subscribe
	mqttc.on_message = on_message
	
	#read config file
	config = read_mqtt_config()
	username = config.get('username')
	passwd = config.get('password')
	host = config.get('host')
	strport = config.get('port')
	port = int(strport)
#	print host

	#connect to broker
#	mqttc.username_pw_set(username, passwd)
#	mqttc.connect(host, port)
#	mqttc.username_pw_set("ziuhykxg","TjjJbgP0Ojuy")
#	mqttc.connect("m21.cloudmqtt.com",14408)
	mqttc.connect("10.10.40.118",1883)
#	mqttc.subscribe(MQTT_TOPICS)
#	mqttc.subscribe("/users/userAdded", 1)
#	mqttc.loop_forever()
#	rc = 0
#	while rc == 0:
#		rc = mqttc.loop()

#	return mqttc



def run():
	#mqttc.subscribe("/users/userAdded",1)
	mqttc.loop_forever()


def quit():
	mqttc.loop_stop()
