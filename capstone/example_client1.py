#!/usr/bin/python
#
# This is a simple paho mqtt client in python
#
# Usage: launch this client, find another machine and use the following
#        publish a message to this client:
#
#        e.g curl -X PUT --data-binary "Hello my dear client cute" http://eclipse.mqttbridge.com/test
#
# To see the message published by this client:(NOTworking yet)
#
# e.g curl http://eclipse.mqttbridge.com/test
#
#

import paho.mqtt.client as mqtt
import time

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
print ("Connecting to the MQTT broker...")
client.connect("iot.eclipse.org",1883,60)

print ("Start forever loop...")
#client.loop_forever()
client.loop_start() # Start a looping thread not to block the main thread

while True:

    time.sleep(10)
    try:
        print("---")
        result, mid = client.publish("test/lid/", "Hi Server from LID client!")
        if result == mqtt.MQTT_ERR_SUCCESS:
            print (" Message %d has been successfully published" % (mid))
        else:
            print (" Message publish failed")
    
    except Exception, e:
        print ("Publish exception %s" % (e))
    
    
    
