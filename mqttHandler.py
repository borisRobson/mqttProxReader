import paho.mqtt.client as mqtt
from configparse import read_mqtt_config
import json
from datetime import datetime
import uuid
from dbhandler import *

def on_connect(client, userdata, flags, rc):
	#subsrcibe inside connect callback
	#if connection is lost, this will call on reconnect
	#and automatically re-subscribe
	print "Connected to mqtt broker: " + str(rc)
	mqttc.subscribe(MQTT_TOPICS)
	

def on_publish(client, userdata, mid):
	print "Message published"

def on_subscribe(mosq, obj, mid, granted_qos):
	print("subscribed to topics: "+ str(MQTT_TOPICS))

def on_message(mosqq, obj, msg):
	#convert payload to json
	data = msg.payload
	jsondata = json.loads(data)
	#get name & token
	name = jsondata["Name"]
	token = jsondata["TokenId"]
	topic = msg.topic
	#parse topic and perform correct action
	if topic.find("Added") != -1:
		insert(name, token)
	elif topic.find("Removed") != -1:
		remove(name)
		print("Removed user: {0}").format(name)

def publish_event(topic,msg):
	mqttc.publish(topic, msg, 1)
	

def init():
	print ("init mqtt")
	global mqttc
	global MQTT_TOPICS
	MQTT_KEEPALIVE_INTERVAL = 5
	MQTT_TOPICS = [('/users/userAdded',1),('/users/userRemoved',1),('/users/userUpdated',1)]
	#create new instance of client
	uid = uuid.uuid1()
	#print uid
	mqttc = mqtt.Client(client_id=str(uid), clean_session=False)

	#assign callbacks
	mqttc.on_publish = on_publish
	mqttc.on_connect = on_connect
	mqttc.on_subscribe = on_subscribe
	mqttc.on_message = on_message
	
	#read config file
	config = read_mqtt_config('config.ini', 'cloudmqtt')
	username = config.get('username')
	passwd = config.get('password')
	host = config.get('host')
	strport = config.get('port')
	port = int(strport)
	print "{0} : {1}".format(host, port)

	mqttc.username_pw_set(str(username), str(passwd))
#	mqttc.connect("m21.cloudmqtt.com",14408)
#	mqttc.connect("10.10.40.118",1883)
	mqttc.connect(str(host), port)

def run():	
	mqttc.loop_forever()


def quit():
	mqttc.disconnect()
	mqttc.loop_stop()
