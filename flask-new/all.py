
import RPi.GPIO as GPIO
import time
from twilio.rest import Client
import pymongo
from pymongo import MongoClient

def fire():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12,GPIO.IN)
    if (GPIO.input(12)) == 0:  # low level means detecting fire
        return('Detecting fire')
    else:
        return('No fire')
    
def sound():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16,GPIO.IN)
    if GPIO.input(16) == 0:  # low level means detecting sound
        return('Detecting sound') 
    else:
        return('No sound')

def light():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25,GPIO.IN)
    if GPIO.input(25) == 0:  # low level means detecting light
        return('Detecting light')
    else:
        return('No light')

def human():    # test if there is someone in the house
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN)  # this sensor is connected to Raspberry Pi through GPIO 23
    if GPIO.input(23)==True: # a notifaction will be posted on website if the sensor return data.
        return('Someone is in your home! CALL 911 ?')
    else:
        return('No one at home')
        
# ----------------------------------------------------------------------------
def showht():
    """
    Due to the instability of temperture & humidity sensor, 40 loop is used for find out the right data.
    DTH11 Sensor is connected to raspberry pi via GPIO 17.
    """
    
    for n in range(40): 
        channel =17
        data = []     # list for instoring 40bit data
        bt = 0        # number of bit data has been detected
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)        
        GPIO.output(channel, GPIO.LOW)    # pull down to lower level to provide starting signal
        time.sleep(0.02)                  # 20ms enables sensor get the starting signal
        GPIO.output(channel, GPIO.HIGH)   # wait for the response from sensor
        GPIO.setup(channel, GPIO.IN)
        while GPIO.input(channel) == GPIO.LOW:
            continue
        while GPIO.input(channel) == GPIO.HIGH: # sensor pull up to high level to start returning data
            continue
        while bt < 40:                    # 40 bit of data
            k = 0
            while GPIO.input(channel) == GPIO.LOW:
                continue
            while GPIO.input(channel) == GPIO.HIGH: # check '0' or '1'
                k += 1                
                if k > 50 :
                    break
            if k < 10:                      # loop used for reflecting high level duration
                data.append(0)                #   26-28us indicate the data is '0' 
            else:
                data.append(1)                # 116-118us indicate the data is '1'        
            bt += 1
        humidity_bit = data[0:8]          
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]
        humidity = 0
        humidity_point = 0
        temperature = 0
        temperature_point = 0
        check = 0
        for i in range(8):                                      # for each 8bit data
            humidity += humidity_bit[i] * 2 ** (7-i)              # integer for temperature
            humidity_point += humidity_point_bit[i] * 2 ** (7-i)  # decimal for temperature
            temperature += temperature_bit[i] * 2 ** (7-i)
            temperature_point += temperature_point_bit[i] * 2 ** (7-i)
            check += check_bit[i] * 2 ** (7-i)                    # sum up all 32bit data
        tmp = humidity + humidity_point + temperature + temperature_point
        if check == tmp:
            return [temperature, humidity]
            break    # if the right temp & humid data is collected, skip the 40 loop
        GPIO.cleanup()
        time.sleep(0.2)   # aviod confliction between two loops
# ----------------------------------------------------------------------------

def smoke():
    # Sensor of gas detection connects to raspberry Pi via GPIO 18 (BCM)

    channel = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    chl = GPIO.wait_for_edge(channel, GPIO.RISING,timeout=500) # add a rising edge trigger detection
    if chl is None:
        return('safe')
    else:
        account_sid = "AC668ad57d6ea31eaa2e55d5ae12e76aea"
        auth_token  = "e6425114fd48bf72867ebfa111a27066"
        client = Client(account_sid, auth_token) 
        tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" Sensor detected dangerous gases!"
        message = client.messages.create(to="+12019939219",
                                 from_="+19148254932",
                                 body= tm)
        return('Sensor detected dangerous gases!')
user = pymongo.MongoClient('localhost',27017)
db = user.test
sens = db.sens
pwd = db.pwd
db.pwd.insert_one({"type":"pwd","pwd":'66666666'})

i = 0
while True:
    hn = human()
    ht = showht()
    sm = smoke()
    sd = sound()
    fe = fire()
    lt = light()
    
    d = time.ctime()
    s1 = {'Datetime':d,'Human':hn,'T&H':ht,'Smoke':sm,'Sound':sd,'Fire':fe,'Light':lt}
    sens.insert_one(s1)
    time.sleep(2)
    i +=1
    print(s1)
    if i>600:
        print(sens.find().count())
        break
