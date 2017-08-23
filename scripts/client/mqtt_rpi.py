### work in progress
#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import socket
import time
import sys
import RPi.GPIO as gpio

# initiate GPIO
gpio.setmode(gpio.BCM)
gpio.setup(25, gpio.OUT)


## BEGIN CALLBACK FUNCTIONS

def screen(mosq, obj, msg):
    if (str(msg.payload) == "b\'1\'"):
        #send gpio event
        print("Screen Down")

    elif (str(msg.payload) == "b\'0\'"):
        #send gpio event
        print("Screen Up")
    #print(str(msg.payload))

def unhandled_msg(mosq, obj, msg):
    print("Unhandled Message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

## END CALLBACK FUNCTIONS

mqttc = mqtt.Client()

mqttc.message_callback_add("Basement/AV/ProjectorScreen/State", screen)

# for everything that doesn't match
mqttc.on_message = unhandled_msg

mqttc.connect("10.0.0.24", 1883, 60)

mqttc.subscribe("Basement/AV/#", 0)

mqttc.loop_forever()

