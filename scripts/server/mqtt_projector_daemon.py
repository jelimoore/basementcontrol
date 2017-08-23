#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import socket
import time
import sys

# different hex defs, from the nec projector code doc
power_on = '020000000002'
power_off = '020100000003'
get_info = '039500000098'

# send data to the projector
def send_projector(ip_value, port_value, hex_data):

        HOST = str(ip_value)
        PORT = int(port_value)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        time.sleep(0.1)
        data = bytes.fromhex(hex_data)
        sock.send(data)

        recv = sock.recv(2048)
        return(recv)

        time.sleep(0.1)

        sock.close()

## BEGIN CALLBACK FUNCTIONS

def pwr(mosq, obj, msg):
    if (str(msg.payload) == "b\'1\'"):
        send_projector("10.0.253.41",7142,power_on)
        print("Projector on")

    elif (str(msg.payload) == "b\'0\'"):
        send_projector("10.0.253.41",7142,power_off)
        print("Projector off")
    #print(str(msg.payload))

def vol(mosq, obj, msg):
    # to be completed
    print("vol")

def input(mosq, obj, msg):
   # to be completed
   print("input")

def unhandled_msg(mosq, obj, msg):
    print("Unhandled Message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

## END CALLBACK FUNCTIONS

mqttc = mqtt.Client()

mqttc.message_callback_add("Basement/AV/Projector/Power", pwr)
mqttc.message_callback_add("Basement/AV/Projector/Volume", vol)
mqttc.message_callback_add("Basement/AV/Projector/Input", input)

# for everything that doesn't match
mqttc.on_message = unhandled_msg

mqttc.connect("10.0.0.24", 1883, 60)

mqttc.subscribe("Basement/AV/Projector/#", 0)

mqttc.loop_forever()
