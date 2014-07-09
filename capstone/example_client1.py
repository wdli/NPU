#!/usr/bin/python
#
# This is a simple paho mqtt client in python
#
# Usage: launch this client, find another machine and use the following
#        publish a message to this client:
#
#        e.g curl -X PUT --data-binary "Hello my client LID" http://eclipse.mqttbridge.com/test/lid
#
# To see the message published by this client:(NOTworking yet)
#
# e.g curl http://eclipse.mqttbridge.com/test/lid
#
#

import paho.mqtt.client as mqtt
import time

MOSQUITTO_SERVER = "10.10.36.87"
MOSQUITTO_SERVER_PORT = 1884 

PUB_TOPIC="hello-from-lid/test"

def on_connect(client, userdata, rc):
    """
    when the server sends a CONNACK response
    """
    print ("Connected with result " + str(rc))
    #client.subscribe("$SYS/#")
    client.subscribe("test/lid/#")


def on_message(client, userdata, msg):
    """
    When the server publish a message
    """
    print("on_message: "+msg.topic+" "+str(msg.payload))


def on_publish(client, userdata, mid):
    """
    Callback when the publish is made
    """
    print("Callback on_publish: Client message published, message ID %d " % (mid))
    
#
# Client initialization
#
client            = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

#
# connect to a MQTT server
#
print ("Connecting to the MQTT broker: %s on port: %s" %( MOSQUITTO_SERVER, MOSQUITTO_SERVER_PORT))
#client.connect("iot.eclipse.org",1883,60)
client.connect(MOSQUITTO_SERVER,MOSQUITTO_SERVER_PORT,60)

print ("Start forever loop...")
client.loop_start() # Start a looping thread not to block the main thread

while True:

    time.sleep(10)
    try:
        print("---")
        #result, mid = client.publish("test/lid/", "Hi Server from LID client!")
        PUB_MSG=time.ctime()
        result, mid = client.publish(PUB_TOPIC, PUB_MSG, 0, True)
        if result == mqtt.MQTT_ERR_SUCCESS:
            print (" Message %d has been successfully published on topic: %s with msg: %s" %
                   (mid, PUB_TOPIC, PUB_MSG))
        else:
            print (" Message publish failed")
    
    except Exception, e:
        print ("Publish exception %s" % (e))
    
    
    
