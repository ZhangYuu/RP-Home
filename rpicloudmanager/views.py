# all the imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from rpicloudmanager import app
import re
from functools import wraps

# import RPi.GPIO as GPIO


def login_required(f):
    # @wraps(f)
    def decorated_function(*args, **kwargs):
        # if g.user is None:
        if 'username' not in session:
            print 'fail'
            # return redirect(url_for('/login', next=request.url))
            return render_template('login_new.html')
        return f(*args, **kwargs)
    return decorated_function


# @app.route('/login', methods=['GET', 'POST'])
# def index():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         session['username'] = 'LOL'
#         return redirect('/')


@app.route('/')
@login_required
def show_index():
    return render_template('index.html')


@app.route('/skip/<int:num>', methods=['GET', 'POST'])
def skip(num):
    if request.method == 'GET':
        if num == 1:
            return render_template('TH_new.html')
        if num == 2:
            return render_template('video_new.html')
        if num == 3:
            return render_template('GPIO_new.html')
        else:
            return render_template('index.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == "POST":
        if session.get('username', None):
            del session['username']
    return redirect('/')


# @app.route('/th', methods=['GET', 'POST'])
# def th():
#     if request.method == "GET":
#         return render_template('TH_new.html')
#     else:
#         return render_template('TH_new.html')


@app.route('/video', methods=['GET', 'POST'])
def video():
    if request.method == "GET":
        return render_template('video_new.html')
    else:
        return render_template('video_new.html')


@app.route('/gpio', methods=['GET', 'POST'])
def gpio():
    if request.method == "GET":
        return render_template('GPIO_new.html')
    else:
        return render_template('GPIO_new.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    error = None

    if request.method == 'GET':
        return render_template('login_new.html')
    if request.method == 'POST':

        print request.form['password']
        if request.form['password'] != '123456':
            error = 'sorry, your password is not correct'
            return render_template('login_new.html', error=error)
        else:
            session['username'] = 'User'
            return redirect('/')
    return render_template('login_new.html', error=error)


@app.route('/human/', methods=['POST'])
def human():
    hum = 'No one at home'
    while True:
        return render_template('TH_new.html', v=hum)


@app.route('/gpio/<int:id>', methods=['POST'])
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
            print "id is being opened/closed"
    return render_template('GPIO_new.html')
    # return redirect(url_for('show_index'))


@app.route('/th/', methods=['GET'])
def show_th():
    t = 35
    h = 59
    return render_template('TH_new.html', temperature=t, humidity=h)


@app.route('/alert/', methods=['GET', 'POST'])
def alert():
    return render_template('alert_info.html')
