# all the imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from rpicloudmanager import app
import re
from flask.ext.pymongo import PyMongo
import pymongo
#import RPi.GPIO as GPIO
user = pymongo.MongoClient("localhost", 27017)
db = user.test
sensors=db.sens
pwd = db.pwd
MacNum='66666666'

@app.route('/')
def index():
  print db.collection_names()
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
    if request.form['password']!=db.pwd.find_one()["pwd"]:
      error = 'sorry'
      return render_template('login.html',error=error)
    else:
      return render_template('home.html')
  return render_template('login.html',error=error)

@app.route("/change_pwd",methods=["POST","GET"])
def change_pwd():
  error = None
  print request.form['MAC_NUM']
  print request.form['new_pwd']
  if request.method == 'POST':
    if request.form['MAC_NUM']==MacNum:
      db.pwd.update({"type":"pwd"},{"type":"pwd","pwd":request.form['new_pwd']})
      error = 'success'
      return render_template('login.html',error1=error)
    else:
      error = 'wrong mac number'
      return render_template('login.html',error1=error)
  return render_template('login.html',error1=error)

@app.route('/human/',methods=['POST'])
def human():
  hum='No one at home'
  while True:
    return render_template('TH.html',v=hum)

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
	#y=sensors.find_one()['S1']#.count()
	cnt=sensors.find().count()-1
  	csr=sensors.find().skip(cnt)
  	for i in csr:
    		time=i['Datetime']
        sound=i['Sound']
        t=i['T&H'][0]
        h=i['T&H'][1]
        fire=i['Fire']
        light=i['Light']
        human=i['Human']
        smoke=i['Smoke']
	return render_template('TH.html',temperature=t,humidity=h,time=time,sound=sound,fire=fire,light=light,human=human,smoke=smoke)
