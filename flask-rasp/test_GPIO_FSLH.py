import time
import random
from collections import defaultdict

''' test emulator for fire(12), sound(16), light(25), human(23) '''
class GPIOEmulator:
    TYPE_FIRE = 12
    TYPE_SOUND = 16
    TYPE_LIGHT = 25
    TYPE_HUMAN = 23

    BCM = 'GPIO.BCM'
    IN = 'GPIO.IN'
    OUT = 'GPIO.OUT'
    LOW = 'GPIO.LOW'
    HIGH = 'GPIO.HIGH'
    EXPECTED_MSG = {TYPE_FIRE:['Yes', 'No'], TYPE_SOUND:['Yes', 'No'], TYPE_LIGHT:['Detecting light', 'No light'], TYPE_HUMAN:['Someone is in your home! CALL 911 ?', 'No one at home']}

    def __init__(self, sensor_type):
        self.channel = defaultdict(lambda:defaultdict(int))
        self.type = sensor_type
        self.msg = ''

    def setmode(self, mode):
        print "GPIO mode is set to:", mode
        assert(GPIOEmulator.BCM == mode)

    def setup(self, chnl, IO):
        self.channel[chnl]['IO'] = IO
        assert(self.channel[chnl]['IO'] in [GPIOEmulator.IN, GPIOEmulator.OUT]) 

    def input(self, chnl):
        time.sleep(0.001) # emulates hardware latency
        
        assert (chnl == self.type) and (chnl in self.channel.keys()), "Test ERROR: The channel is invalid!: {}".format(chnl)
        sig = random.randint(0,1) # emulate fire/sound/light/human event: 0(low/False) or 1(high/True)
        self.msg = GPIOEmulator.EXPECTED_MSG[chnl][sig] if GPIOEmulator.TYPE_HUMAN != chnl else GPIOEmulator.EXPECTED_MSG[chnl][1-sig]
        return sig if GPIOEmulator.TYPE_HUMAN != chnl else bool(sig)

    def expected_msg(self):
        return self.msg


#------------------------------------------------
''' sample test (fire detection): '''

GPIO = GPIOEmulator(GPIOEmulator.TYPE_FIRE)

# fire detection code:
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN)
if (GPIO.input(12)) == 0:  # low level means detecting fire
    assert('Yes' == GPIO.expected_msg())
    print "Test OK: Fire(=12) detected"
    #return ('Yes')
else:
    assert('No' == GPIO.expected_msg())
    print "Test OK: Fire(=12) not detected"
    #return ('No')