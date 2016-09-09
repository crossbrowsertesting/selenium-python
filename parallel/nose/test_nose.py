#!/usr/bin/env python

import unittest
from selenium import webdriver

USERNAME = "mikeh"
API_KEY = ""


class SeleniumCBT(unittest.TestCase):
    def setUp(self):
        caps = {}

        caps['name'] = 'Python Nose Parallel'
        caps['build'] = '1.0'
        caps['browser_api_name'] = 'Chrome43x64'
        caps['os_api_name'] = 'Win8.1'
        caps['screen_resolution'] = '1024x768'

        # start the remote browser on our server
        self.driver = webdriver.Remote(
            desired_capabilities=caps,
            command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub" % (USERNAME, API_KEY)
        )

        self.driver.implicitly_wait(20)

    def test_CBT(self):

        # load the page url
        print('Loading Url')
        self.driver.get('http://crossbrowsertesting.github.io/selenium_example_page.html')

        # check the title
        print('Checking title')
        self.assertTrue("Selenium Test Example Page" in self.driver.title)

    def tearDown(self):
        print("Done with session %s" % self.driver.session_id)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
