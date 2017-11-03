#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 20:10:48 2017

@author: orange
"""
import RPi.GPIO as GPIO
import time
from twilio.rest import Client
def action(channel):
    '''
    Send the message to user from the formatted local time and the gas information.
    Message will be send via an API from twilio. 
    '''
    print('Sensor detected dangerous gases!') # show in the terminal for developer to check
    tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" Sensor detected dangerous gases!"
    message = client.messages.create(to="+12019939219",
                                 from_="+19148254932",
                                 body= tm)
def detect():
    '''
    Sensor of gas detection connects to raspberry Pi via GPIO 18 (BCM)
    '''
    channel = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(channel, GPIO.RISING) # add a rising edge trigger detection
    GPIO.add_event_callback(channel,action) 
account_sid = "AC668ad57d6ea31eaa2e55d5ae12e76aea"
auth_token  = "e6425114fd48bf72867ebfa111a27066"
client = Client(account_sid, auth_token)
"""
Account info for twilio API
"""
detect()
try:
    while True:    #loop is used for continuous testing
        print('Safe')
        time.sleep(1)
except KeyboardInterrupt:
    pass
GPIO.cleanup()
