import time
import random
from collections import defaultdict

#------------------------------------
''' Function "all.showht" test sample data: temperature: 26 *C, humidity: 55 % '''
TEST_DATA = [   0,0,1,1,0,1,1,1,
                0,1,0,1,0,0,0,1,
                0,0,0,1,1,0,1,0,
                0,0,1,0,1,0,0,0,
                1,1,0,0,1,0,1,0 # check
            ]
#------------------------------------

class GPIOEmulator:
    BCM = 'GPIO.BCM'
    IN = 'GPIO.IN'
    OUT = 'GPIO.OUT'
    LOW = 'GPIO.LOW'
    HIGH = 'GPIO.HIGH'

    # several randomly generated numbers for emulating hardware listening events
    EMU_NUM_1 = random.randint(0, 5)
    EMU_NUM_2 = random.randint(5, 10)

    def __init__(self):
        self.channel = defaultdict(lambda:defaultdict(int))
        self.sig_in = 0
        self.sig_in_prev = 0
        self.data_idx = 0
        self.is_out_of_loop40 = True

    def setmode(self, mode):
        print "GPIO mode is set to:", mode
        assert(GPIOEmulator.BCM == mode)

    def setup(self, chnl, IO):
        self.channel[chnl]['IO'] = IO
        assert(self.channel[chnl]['IO'] in [GPIOEmulator.IN, GPIOEmulator.OUT])

    def output(self, chnl, SIG):
        self.channel[chnl]['SIG'] = SIG
        assert(self.channel[chnl]['SIG'] in [GPIOEmulator.LOW, GPIOEmulator.HIGH])    

    def input(self, chnl):
        time.sleep(0.002) # emulates hardware latency: 2 ms

        global TEST_DATA

        if self.sig_in < GPIOEmulator.EMU_NUM_1:
            self.channel[chnl]['SIG'] = GPIOEmulator.LOW
            self.sig_in += 1
            return GPIOEmulator.LOW
        elif self.sig_in < GPIOEmulator.EMU_NUM_2:
            self.channel[chnl]['SIG'] = GPIOEmulator.HIGH
            self.sig_in += 1
            return GPIOEmulator.HIGH
        elif self.is_out_of_loop40:
            self.sig_in = 10
        
        if self.is_out_of_loop40:
            self.is_out_of_loop40 = False
            return GPIOEmulator.LOW # to enter '< 40' loop

        if 10 == self.sig_in:
            self.sig_in_prev = self.sig_in
            if 1 == TEST_DATA[self.data_idx]: # append(1)
                self.sig_in = random.randint(self.sig_in_prev + 11, self.sig_in_prev + 50)
            else: # append(0)
                self.sig_in = random.randint(self.sig_in_prev + 2, self.sig_in_prev + 10)
            self.data_idx += 1
        
        if len(TEST_DATA) == self.data_idx:
            return 'N/A' # to break whatever loop

        if self.sig_in_prev < self.sig_in:
            self.channel[chnl]['SIG'] = GPIOEmulator.HIGH
            self.sig_in_prev += 1
            return GPIOEmulator.HIGH
        else: # break and go next bit
            self.channel[chnl]['SIG'] = GPIOEmulator.LOW
            self.sig_in = 10
            return GPIOEmulator.LOW

    def cleanup(self):
        self.channel[chnl]['IO'] = 'N/A'
        self.channel[chnl]['SIG'] = 'N/A'


#-----------------------------------------
#-----------------------------------------
''' Target code to test (from all.py) : '''
#-----------------------------------------
#-----------------------------------------

GPIO = GPIOEmulator() # fake GPIO device

channel = 17
bits = []
j = 0

# Device init phase part:
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
GPIO.output(channel, GPIO.LOW)
time.sleep(0.02)
GPIO.output(channel, GPIO.HIGH)
GPIO.setup(channel, GPIO.IN)
while GPIO.input(channel) == GPIO.LOW:
    continue
while GPIO.input(channel) == GPIO.HIGH:
    continue

# T&H calculation part
while j < 40:
    k = 0
    while GPIO.input(channel) == GPIO.LOW:
        continue
    while GPIO.input(channel) == GPIO.HIGH:
        k += 1
        if k > 50:
            break
    if k < 10:
        bits.append(0)
    else:
        bits.append(1)
    j += 1

#-----------------------------------------
#-----------------------------------------

print "Channel =", channel

print TEST_DATA
print bits

assert(TEST_DATA == bits) # ensure identicalness
print "Test OK: Emulated result is identical to the testing data."

data = bits # just an alias

#-----------------------------------------
#-----------------------------------------
''' Target code to test (from all.py) : '''
#-----------------------------------------
#-----------------------------------------

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
for i in range(8):
    humidity += humidity_bit[i] * 2 ** (7-i)
    humidity_point += humidity_point_bit[i] * 2 ** (7-i)
    temperature += temperature_bit[i] * 2 ** (7-i)
    temperature_point += temperature_point_bit[i] * 2 ** (7-i)
    check += check_bit[i] * 2 ** (7-i)
tmp = humidity + humidity_point + temperature + temperature_point

#-----------------------------------------
#-----------------------------------------

assert(check == tmp) # ensure the identicalness
print "Test OK: Data bits are verified to be valid."

if check == tmp:
    #print "check =", tmp
    print "Temperature:", temperature, "*C; Humidity:", humidity, "%"
else:
    print "Check bits and calculated results did not match!"

