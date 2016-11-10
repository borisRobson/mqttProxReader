import paho.mqtt.client as mqtt
from configparse import read_mqtt_config
import json
from datetime import datetime
import uuid
from dbhandler import insert

def on_connect(client, userdata, flags, rc):
	print "Connected to mqtt broker: " + str(rc)
	mqttc.subscribe(MQTT_TOPICS)
	

def on_publish(client, userdata, mid):
	print "Message published"

def on_subscribe(mosq, obj, mid, granted_qos):
	print("subscribed to topics: "+ str(MQTT_TOPICS))

def on_message(mosqq, obj, msg):
	print msg.payload
	data = msg.payload
	jsondata = json.loads(data)
	name = jsondata["Name"]
	token = jsondata["TokenId"]
	insert(name, token)

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
	config = read_mqtt_config()
	username = config.get('username')
	passwd = config.get('password')
	host = config.get('host')
	strport = config.get('port')
	port = int(strport)

#	mqttc.username_pw_set("ziuhykxg","TjjJbgP0Ojuy")
#	mqttc.connect("m21.cloudmqtt.com",14408)
	mqttc.connect("10.10.40.118",1883)

def run():	
	mqttc.loop_forever()


def quit():
	mqttc.disconnect()
	mqttc.loop_stop()
