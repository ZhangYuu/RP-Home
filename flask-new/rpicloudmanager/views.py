# all the imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from rpicloudmanager import app
import re
#import RPi.GPIO as GPIO

@app.route('/')
def index():
  return render_template('login.html')

@app.route('/show_index')
def show_index():
  return render_template('home.html')

@app.route('/skip/<int:num>',methods=['POST'])
def skip(num):
  if request.method == 'POST':
   if num==1:
    return render_template('TH.html')
   if num==2:
    return render_template('video.html')
   if num==3:
    return render_template('GPIO.html')
   else:
    return render_template('home.html')

@app.route("/login",methods=["POST","GET"])
def login():
  error = None
  print request.form['password']
  if request.method == 'POST':
    if request.form['password']!='123456':
      error = 'sorry'
      return render_template(url_for('home.html'))
    else:
      return render_template('home.html')
  return render_template('login.html',error=error)


@app.route('/gpio/<int:id>',methods=['POST'])
def gpio_led(id):
  if request.method == 'POST':
    #GPIO.setmode(GPIO.BCM)
    if id<100:
      #GPIO.setup(id,GPIO.OUT)
      #GPIO.setmode(GPIO.BCM)
      #GPIO.setup(id,GPIO.OUT)
      #GPIO.output(id,False)
      print id, "is being set up"
    else:
      #GPIO.setup(id-100,GPIO.OUT)
      #GPIO.output(id-100,True)
      print "id is being opened/closed"
  return render_template('GPIO.html')
  #return redirect(url_for('show_index'))

@app.route('/getT/',methods=['POST'])
def showt():
	t=34
	x=59
	return render_template('TH.html',var=t,va=x)
