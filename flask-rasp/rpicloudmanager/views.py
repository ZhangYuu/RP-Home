# all the imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from rpicloudmanager import app
import re
import RPi.GPIO as GPIO


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


@app.route('/')
@login_required
def index():
  return render_template('index.html')

# @app.route('/show_index')
# def show_index():
#   return render_template('index.html')


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


@app.route('/skip/<int:num>',methods=['POST', "GET"])
def skip(num):
  if request.method == 'POST':
   if num==1:
    return render_template('TH_new.html')
   if num==2:
    return render_template('video_new.html')
   if num==3:
    return render_template('GPIO_new.html')
   else:
    return render_template('index.html')


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



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == "POST":
        if session.get('username', None):
            del session['username']
    return redirect('/')


@app.route('/gpio/<int:id>',methods=['POST'])
def gpio_led(id):
  if request.method == 'POST':
    GPIO.setmode(GPIO.BCM)
    if id<100:
      GPIO.setup(id,GPIO.OUT)
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(id,GPIO.OUT)
      GPIO.output(id,False)
      print id, "is being set up"
    else:
      GPIO.setup(id-100,GPIO.OUT)
      GPIO.output(id-100,True)
      print "id is being opened/closed"
  return render_template('GPIO_new.html')
  #return redirect(url_for('show_index'))

@app.route('/human/',methods=['GET', 'POST'])
def human():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(23, GPIO.IN)
  while True:
    if GPIO.input(23)==True:
      return render_template('TH_new.html',v='Someone is in your home! Call 911?')
    else:
      return render_template('TH_new.html',v='Nothing detected.')

@app.route('/th/',methods=['GET', 'POST'])
def showt():
  for n in range(40):
    import RPi.GPIO as GPIO
    import time
    channel =17
    data = []
    j = 0
    GPIO.setmode(GPIO.BCM)
  #time.sleep(1)
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
        if k > 50 :
           break
      if k < 10:
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
      humidity += humidity_bit[i] * 2 ** (7-i)
      humidity_point += humidity_point_bit[i] * 2 ** (7-i)
      temperature += temperature_bit[i] * 2 ** (7-i)
      temperature_point += temperature_point_bit[i] * 2 ** (7-i)
      check += check_bit[i] * 2 ** (7-i)
    tmp = humidity + humidity_point + temperature + temperature_point
    if check == tmp:
      return render_template('TH_new.html',temperature=temperature,humidity=humidity)
      print "temperature :", temperature, "*C, humidity :", humidity, "%"
      break
    GPIO.cleanup()
    time.sleep(0.2)


@app.route('/alert/', methods=['GET', 'POST'])
def alert():
    return render_template('alert_info.html')
