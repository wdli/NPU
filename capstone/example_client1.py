#!/usr/bin/python
#
# This is a simple paho mqtt client in python
#
# Usage: launch this client, find another machine and use the following
#        publish a message to this client:
#
#        e.g curl -X PUT --data-binary "Hello my dear client cute" http://eclipse.mqttbridge.com/test
#


import paho.mqtt.client as mqtt


def on_connect(client, userdata, rc):
    """
    when the server sends a CONNACK response
    """
    print ("Connected with result " + str(rc))
    #client.subscribe("$SYS/#")
    client.subscribe("test/#")


def on_message(client, userdata, msg):
    """
    When the server publish a message
    """
    print(msg.topic+" "+str(msg.payload))


#
# Client initialization
#
client            = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print ("Connecting to the MQTT broker...")
client.connect("iot.eclipse.org",1883,60)

print ("Start forever loop...")
client.loop_forever()