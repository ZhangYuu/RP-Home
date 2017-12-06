import os
import rpicloudmanager
from rpicloudmanager import app
import unittest
import tempfile

class RPHomeTestCase(unittest.TestCase):
    ''' General RP-Home test suits
    '''
    # runned first every time test begins
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp() # create temporary empty database file
        app.testing = True
        self.app = app.test_client() # flask app client for test
        with app.app_context():
            rpicloudmanager.init_db()

    # runned last every time test ends
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE']) # disconnect with db

    ###### ------------ Use Cases ------------- ######

    def test_void_db(self):
        ''' test empty database '''
        rt = self.app.get('/') # send an HTTP GET request to the application with the root path
        assert b'No entries here so far' in rt.data

    def login(self, usr, psw):
        ''' login test's trigger function '''
        # POST to views.login
        return self.app.post('/login'
                , data={'username':usr, 'password':psw}
                , follow_redirects=True
            )

    def logout(self):
        ''' logout test's trigger function '''
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        '''Login test: fire some requests to the login page with the required form data (username and password)
           Logout test: fire some requests to the logout page
        '''
        # normal login:
        resp = self.login('admin', '123456')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'logged in' in resp.data)

        # normal logout; needed before testing the following wrong-case logins
        resp = self.logout()
        self.assertEqual(resp.status_code, 200) # 200: request succeeded
        self.assertTrue(b'logged out' in resp.data)

        # login with wrong user name:
        resp = self.login('ADmin', '123456')
        self.assertTrue(b'sorry' in resp.data)

        # login with wrong password:
        resp = self.login('admin', '12345678')
        self.assertTrue(b'sorry' in resp.data)


if __name__ == '__main__':
    unittest.main()