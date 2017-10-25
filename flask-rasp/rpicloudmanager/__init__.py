# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash
from contextlib import closing

app = Flask(__name__)
app.config.from_object('rpicloudmanager.config.Development')
#app.config.from_object('rpicloudmanager.config.Development')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql',mode='r') as f:
      ad.cursor().executescript(f.read())
    db.commit()

import  rpicloudmanager.views

if __name__=='__main__':
  app.run()
