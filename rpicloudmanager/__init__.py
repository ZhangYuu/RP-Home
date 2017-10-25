# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config.from_object('rpicloudmanager.config.Development')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def connect_db():
    # rv = sqlite3.connect(app.config['DATABASE'])
    # rv.row_factory = sqlite3.Row
    # return rv
    return sqlite3.connect(app.config['DATABASE'])


# def init_db():
#     """Initializes the database."""
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#
#
# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
#
#
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()
#
#
# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql', mode='r') as f:
#             ad.cursor().executescript(f.read())
#         db.commit()



import rpicloudmanager.views

if __name__ == '__main__':
    app.run()
