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
    print db.collection_names()
    return redirect('/login')


@app.route('/show_index')
@login_required
def show_index():
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

