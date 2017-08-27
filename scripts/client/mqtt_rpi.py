### work in progress
#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import socket
import time
import sys
from pyfirmata import ArduinoMega, util

board = ArduinoMega('/dev/ttyACM0')

## BEGIN CALLBACK FUNCTIONS

def screen(mosq, obj, msg):
    if (str(msg.payload) == "b\'1\'"):
        board.digital[7].write(1)
        print("Screen Down")

    elif (str(msg.payload) == "b\'0\'"):
        board.digital[7].write(0)
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
mqttc.subscribe("Basement/#", 0)
mqttc.loop_forever()

