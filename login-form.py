# Please visit http://selenium-python.readthedocs.org/ for detailed installation and instructions
# Getting started: http://docs.seleniumhq.org/docs/03_webdriver.jsp
# API details: https://github.com/SeleniumHQ/selenium#selenium

# Requests is the easiest way to make RESTful API calls in Python. You can install it by following the instructions here:
# http://docs.python-requests.org/en/master/user/install/

import unittest
from selenium import webdriver
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class LoginForm(unittest.TestCase):
    def setUp(self):

        # Put your username and authey below
        # You can find your authkey at crossbrowsertesting.com/account
        self.username = "user@email.com"
        self.authkey  = "12345"

        self.api_session = requests.Session()
        self.api_session.auth = (self.username,self.authkey)

        self.test_result = None

        caps = {}

        caps['name'] = 'Login Form Example'
        caps['build'] = '1.0'
        caps['browser_api_name'] = 'Chrome53'
        caps['os_api_name'] = 'Win10'
        caps['screen_resolution'] = '1024x768'
        caps['record_video'] = 'true'
        caps['record_network'] = 'true'

        # start the remote browser on our server
        self.driver = webdriver.Remote(
            desired_capabilities=caps,
            command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(self.username,self.authkey)
        )

        self.driver.implicitly_wait(20)

    def test_CBT(self):
        # We wrap this all in a try/except so we can set pass/fail at the end
        try:
            # load the page url
            print('Loading Url')
            self.driver.get('http://crossbrowsertesting.github.io/login-form.html')

            # maximize the window - DESKTOPS ONLY
            #print('Maximizing window')
            self.driver.maximize_window()

            # we'll start the login process by entering our username
            print('Entering username')
            self.driver.find_element_by_name('username').send_keys('tester@crossbrowsertesting.com')
            
            # then by entering our password
            print('Entering password')
            self.driver.find_element_by_name('password').send_keys('test123')
            
            # now we'll click the login button
            print('Logging in')
            self.driver.find_element_by_css_selector('body > div > div > div > div > form > div.form-actions > button').click()
            
            # if we've passed the login, we should see the welcome text

            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id=\"logged-in-message\"]/h2'))
            )

            welcomeText = elem.text
            self.assertEqual("Welcome tester@crossbrowsertesting.com", welcomeText)

            print("Taking snapshot")
            snapshot_hash = self.api_session.post('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots').json()['hash']

            # if we are still in the try block after all of our assertions that
            # means our test has had no failures, so we set the status to "pass"
            self.test_result = 'pass'

        except AssertionError as e:
            # log the error message, and set the score to "during tearDown()".
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots/' + snapshot_hash,
                data={'description':"AssertionError: " + str(e)})
            self.test_result = 'fail'
            raise

    def tearDown(self):
        print("Done with session %s" % self.driver.session_id)
        self.driver.quit()
        # Here we make the api call to set the test's score.
        # Pass it it passes, fail if an assertion fails, unset if the test didn't finish
        if self.test_result is not None:
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id,
                data={'action':'set_score', 'score':self.test_result})


if __name__ == '__main__':
    unittest.main()
