# Please visit http://selenium-python.readthedocs.org/en/latest/index.html for detailed installation and instructions
# Getting started: http://docs.seleniumhq.org/docs/03_webdriver.jsp
# API details: https://github.com/SeleniumHQ/selenium#selenium

# Requests is the easiest way to make RESTful API calls in Python. You can install it by following the instructions here:
# http://docs.python-requests.org/en/master/user/install/

import unittest
from selenium import webdriver
import requests

class TodoAppTest(unittest.TestCase):
    def setUp(self):

        # Put your username and authey below
        # You can find your authkey at crossbrowsertesting.com/account
        self.username = "user@email.com"
        self.authkey  = "12345"

        self.api_session = requests.Session()
        self.api_session.auth = (self.username,self.authkey)

        self.test_result = None

        caps = {}

        caps['name'] = 'Todo App Example'
        caps['build'] = '1.0'
        caps['browserName'] = 'Chrome'
        caps['version'] = '53'
        caps['platform'] = 'Windows 10'
        caps['screenResolution'] = '1366x768'
        caps['record_video'] = 'true'
        caps['record_network'] = 'false'

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
            self.driver.get('http://crossbrowsertesting.github.io/todo-app.html')

            # maximize the window - DESKTOPS ONLY
            #print('Maximizing window')
            self.driver.maximize_window()

            # if the checkboxes work, I should be able to click on them
            print('Clicking Checkbox')
            self.driver.find_element_by_name('todo-4').click()
            print('Clicking Checkbox')
            self.driver.find_element_by_name('todo-5').click()

            # if I clicked on them, their class name should now be 'done-true'
            elems = self.driver.find_elements_by_class_name('done-true')
            self.assertEqual(2, len(elems))
            # if my form element works, I should be able to enter text and add it to my list.
            print('Entering Text')
            self.driver.find_element_by_id('todotext').send_keys('Run your first Selenium Test')
            self.driver.find_element_by_id('addbutton').click()

            # if I entered the text, the following element should contain that text
            span_text = self.driver.find_element_by_xpath('/html/body/div/div/div/ul/li[6]/span').text
            self.assertEqual('Run your first Selenium Test', span_text)

            # if my archive link works, my checked elements should be archived
            print('Archiving old todos')
            self.driver.find_element_by_link_text('archive').click()

            elems = self.driver.find_elements_by_class_name('done-false')
            self.assertEqual(4, len(elems))

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
