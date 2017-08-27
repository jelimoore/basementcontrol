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
volume = '0310000005050000'
vga = '0203000002010109'
analogvid = '020300000201060E'
dvi = '0203000002011A22'

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

def pwr(mosq, obj, msg):
    if (str(msg.payload) == "b\'1\'"):
        send_projector("10.0.253.41",7142,power_on)
        print("Projector on")

    elif (str(msg.payload) == "b\'0\'"):
        send_projector("10.0.253.41",7142,power_off)
        print("Projector off")
    print(str(msg.payload))

def vol(mosq, obj, msg):
    volnum = str(msg.payload)
    vol = volnum[2:-1] # cut the first two and last character, the string comes out as " b'1' "
    volhex = hex(int(vol)) # turn the cut string into an int, then into hex
    volhex_no_0 = volhex[2:] # cut the "0x" from the hex string

    if (int(volhex, 16) < 16 ):
        padded_volhex_no_0 = "0" + volhex_no_0
        checksum = 29 + int(padded_volhex_no_0, 16)
        projector_data = str(volume) + str(padded_volhex_no_0) + "00" + hex(int(checksum))[2:]
        print(send_projector("10.0.253.41",7142,projector_data))
        print(projector_data)
        print(checksum)
        print("\r")
    else:
        checksum = 29 + int(volhex_no_0, 16)
        projector_data = str(volume) + str(volhex_no_0) + "00" + hex(int(checksum))[2:]
        print(send_projector("10.0.253.41",7142,projector_data))
        print(projector_data)
        print(checksum)
        print("\r")

def input_vga(mosq, obj, msg):
    send_projector("10.0.253.41",7142,vga)

def input_analog(mosq, obj, msg):
    send_projector("10.0.253.41",7142,analogvid)

def input_dvi(mosq, obj, msg):
    send_projector("10.0.253.41",7142,dvi)

def unhandled_msg(mosq, obj, msg):
    print("Unhandled Message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

mqttc = mqtt.Client()

mqttc.message_callback_add("Basement/AV/Projector/Power", pwr)
mqttc.message_callback_add("Basement/AV/Projector/Volume", vol)
mqttc.message_callback_add("Basement/AV/Projector/Input/VGA", input_vga)
mqttc.message_callback_add("Basement/AV/Projector/Input/Analog", input_analog)
mqttc.message_callback_add("Basement/AV/Projector/Input/DVI", input_dvi)

mqttc.on_message = unhandled_msg				# for everything that doesn't match

mqttc.connect("10.0.0.24", 1883, 60)

mqttc.subscribe("Basement/AV/Projector/#", 0)

mqttc.loop_forever()
