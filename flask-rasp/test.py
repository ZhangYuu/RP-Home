import os
from rpicloudmanager import __init__
from rpicloudmanager import app
import unittest
import tempfile

class RPHomeTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()
        with app.app_context():
            __init__.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    #### ------------ Use Cases -------------
    def test_void_db(self):
        rt = self.app.get('/') # send an HTTP GET request to the application with the root path
        assert b'No entries here so far' in rt.data

    def login(self, usr, psw):
        return self.app.post('/login', data=dict(username=usr, password=psw), follow_redirects=True) # POST to views.login

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login(self, username, password):
        '''fire some requests to the login and logout pages with the required form data (username and password)'''


if __name__ == '__main__':
    unittest.main()