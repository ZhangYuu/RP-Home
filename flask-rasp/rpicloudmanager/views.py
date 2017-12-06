# all the imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from functools import wraps
from contextlib import closing
from rpicloudmanager import app
import re
from flask.ext.pymongo import PyMongo
import pymongo
import time, json

# import RPi.GPIO as GPIO
user = pymongo.MongoClient("localhost", 27017)
db = user.test
sensors = db.sens
pwd = db.pwd
prof = db.prof
MacNum = '66666666'

@app.route('/create_newdata')
def create_data():
    s1 = {'Datetime': time.ctime(), 'Human': 'No one at home',
          'T&H': [97, 10], 'Smoke': 'Sensor detected dangerous gases!', 'Sound': 'No sound',
          'Fire': 'No fire', 'Light': 'Detecting light'}
    sensors.insert_one(s1)
    return render_template('login.html')


# check whether the user has logged in or not      By Zhi
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if g.user is None:
        if 'username' not in session:
            print 'No user now.'
            # return redirect(url_for('/login', next=request.url))
            return render_template('login_rp.html')
        return f(*args, **kwargs)

    return decorated_function



@app.route('/')
def index():
<<<<<<< HEAD
    return render_template('login.html')
=======
    print db.collection_names()
    return redirect('/login')
>>>>>>> upstream/master


@app.route('/show_index')
@login_required
def show_index():
<<<<<<< HEAD
    return render_template('home.html')


@app.route('/skip/<int:num>', methods=['POST'])
def skip(num):
    if request.method == 'POST':
        if num == 1:
            return render_template('TH.html')
        if num == 2:
            return render_template('video.html')
        if num == 3:
            return render_template('GPIO.html')
        else:
            return render_template('home.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    print request.form['password']
    if request.method == 'POST':
        if request.form['password'] != '123456':
            error = 'sorry'
            return render_template('login.html', error=error)
        else:
            return render_template('home.html')
    '''return render_template('login.html',error=error)'''


@app.route('/gpio/<int:id>', methods=['POST'])
def gpio_led(id):
    if request.method == 'POST':
        GPIO.setmode(GPIO.BCM)
        if id < 100:
            GPIO.setup(id, GPIO.OUT)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(id, GPIO.OUT)
            GPIO.output(id, False)
            print id, "is being set up"
        else:
            GPIO.setup(id - 100, GPIO.OUT)
            GPIO.output(id - 100, True)
            print "id is being opened/closed"
    return render_template('GPIO.html')
    # return redirect(url_for('show_index'))


@app.route('/human/', methods=['POST'])
def human():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)
    while True:
        if GPIO.input(18) == True:
            return render_template('TH.html', v='Human')
        else:
            return render_template('TH.html', v='Noman')


@app.route('/getT/', methods=['POST'])
def showt():
    import RPi.GPIO as GPIO
    import time
    channel = 17
    data = []
    j = 0
    GPIO.setmode(GPIO.BCM)
    # time.sleep(1)
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.LOW)
    time.sleep(0.02)
    GPIO.output(channel, GPIO.HIGH)
    GPIO.setup(channel, GPIO.IN)
    while GPIO.input(channel) == GPIO.LOW:
        continue
    while GPIO.input(channel) == GPIO.HIGH:
        continue
    while j < 40:
        k = 0
        while GPIO.input(channel) == GPIO.LOW:
            continue
        while GPIO.input(channel) == GPIO.HIGH:
            k += 1
            if k > 100:
                break
        if k < 8:
            data.append(0)
        else:
            data.append(1)
        j += 1
    print "sensor is working."
    print data
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
        humidity += humidity_bit[i] * 2 ** (7 - i)
        humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
        temperature += temperature_bit[i] * 2 ** (7 - i)
        temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
        check += check_bit[i] * 2 ** (7 - i)
    tmp = humidity + humidity_point + temperature + temperature_point
    if check == tmp:
        return render_template('TH.html', var=temperature, va=humidity)
        print "temperature :", temperature, "*C, humidity :", humidity, "%"
    else:
        return render_template('TH.html', var=temperature, va=humidity)
        print "wrong"
        print "temperature :", temperature, "*C, humidity :", humidity, "% check :", check, ", tmp :", tmp
    GPIO.cleanup()


'''
	t=34
	x=59
	return render_template('TH.html',var=t,va=x)
'''
=======
    return render_template('index.html')


@app.route('/skip/<int:num>', methods=['GET', 'POST'])
@login_required
def skip(num):
    # if request.method == 'get':
    if num == 1:
        # return render_template('TH_new.html')
        return redirect('/getT')
    if num == 2:
        return render_template('video_new.html')
    if num == 3:
        return render_template('GPIO_new.html')
    else:
        return render_template('index.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'username' in session:
        return redirect('/show_index')
    error = None
    #  print request.form['password']
    if request.method == 'POST':
        if request.form['password'] != db.pwd.find_one()["pwd"]:
            error = 'Please input the correct password!'
            return render_template('login_rp.html', error=error)
        else:
            session['username'] = 'User'
        return render_template('index.html')
    return render_template('login_rp.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == "POST":
        if session.get('username', None):
            del session['username']
    return redirect('/')


@app.route("/change_pwd", methods=["POST", "GET"])
def change_pwd():
    error = None
    #  print request.form['MAC_NUM']
    # 'MAC_NUM' has been changed to 'current_pwd'
    #  print request.form['new_pwd']
    if request.method == 'POST':
        #    if request.form['current_pwd']==MacNum:
        if request.form['current_pwd'] == db.pwd.find_one()["pwd"]:
            db.pwd.update({"type": "pwd"}, {"type": "pwd", "pwd": request.form['new_pwd']})
            error = 'success'
            return render_template('login_rp.html', error1=error)
        else:
            #      error = 'wrong mac number'
            error = 'wrong password'
            return render_template('login_rp.html', error1=error)
    return render_template('change_pwd.html')


@app.route('/human/', methods=['POST'])
@login_required
def human():
    hum = 'No one at home'
    while True:
        return render_template('TH_new.html', v=hum)


@app.route('/alert_check', methods=['GET', 'POST'])
@login_required
def check():
    cnt = sensors.find().count() - 2
    csr = sensors.find().skip(cnt)
    for i in csr:
        time1 = i['Datetime']
        sound1 = i['Sound']
        t1 = i['T&H'][0]
        h1 = i['T&H'][1]
        fire1 = i['Fire']
        light1 = i['Light']
        human1 = i['Human']
        smoke1 = i['Smoke']
        break

    cnt = sensors.find().count() - 1
    csr = sensors.find().skip(cnt)
    for i in csr:
        time2 = i['Datetime']
        sound2 = i['Sound']
        t2 = i['T&H'][0]
        h2 = i['T&H'][1]
        fire2 = i['Fire']
        light2 = i['Light']
        human2 = i['Human']
        smoke2 = i['Smoke']

    status = "same"
    print smoke1
    if t2 > 90:
        status = "Dangerous! Temperature is too high!"
    if sound1 != sound2 and "Detecting sound" in sound2:
        status = "Dangerous!" + sound2
    if fire1 != fire2 and "Detecting fire" in fire2:
        status = "Dangerous!" + fire2
    if human1 != human2 and "Someone" in human2:
        status = "Dangerous!" + human2
    if smoke1 != smoke2 and "Sensor" in smoke2:
        status = "Dangerous!" + smoke2

    data = {
        'status': status
    }
    print status
    return jsonify(data)


@app.route('/gpio/<int:id>', methods=['POST'])
@login_required
def gpio_led(id):
    if request.method == 'POST':
        # GPIO.setmode(GPIO.BCM)
        if id < 100:
            # GPIO.setup(id,GPIO.OUT)
            # GPIO.setmode(GPIO.BCM)
            # GPIO.setup(id,GPIO.OUT)
            # GPIO.output(id,False)
            print id, "is being set up"
        else:
            # GPIO.setup(id-100,GPIO.OUT)
            # GPIO.output(id-100,True)
            print id, "is being opened/closed"
    return render_template('GPIO_new.html')
    # return redirect(url_for('show_index'))


@app.route('/getT/', methods=['GET', 'POST'])
@login_required
def showt():
    # y=sensors.find_one()['S1']#.count()
    cnt = sensors.find().count() - 1
    csr = sensors.find().skip(cnt)
    for i in csr:
        time = i['Datetime']
        sound = i['Sound']
        t = i['T&H'][0]
        h = i['T&H'][1]
        fire = i['Fire']
        light = i['Light']
        human = i['Human']
        smoke = i['Smoke']

    if "No" in fire:
        fire_degree = 1
    else:
        fire_degree = 100
    if "dangerous" in smoke:
        smoke_degree = 90
    else:
        smoke_degree = 3
    if "No" in sound:
        sound_degree = 1
    else:
        sound_degree = 80

    return render_template('TH_new.html', temperature=t, humidity=h, time=time, sound=sound, fire=fire, light=light,
                           human=human, smoke=smoke,
                           smoke_degree=smoke_degree, fire_degree=fire_degree, sound_degree=sound_degree)


@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == "GET":
        user_prof = prof.find_one()
        return render_template('alert_info.html', user_prof=user_prof)
    else:
        email = request.form['email']
        phone1 = request.form['phone1']
        phone2 = request.form['phone2']
        user_prof = {"type": "prof","email": email, "phone1": phone1, "phone2": phone2}
        print prof.find_one()
        if prof.find_one():
            print "find"
            prof.update({"type": "prof"}, user_prof)
        else:
            print "insert"
            prof.insert_one(user_prof)
        return redirect('/profile')

>>>>>>> upstream/master
