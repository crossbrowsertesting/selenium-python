from threading import Thread
from selenium import webdriver
import time

USERNAME = "mikeh"
API_KEY = ""


def get_browser(caps):
    return webdriver.Remote(
            desired_capabilities=caps,
            command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub" % (USERNAME, API_KEY)
        )

browsers = [
  {"os_api_name": "Win7x64-C2", "browser_api_name": "IE10", "name": "Python Parallel"},
  {"os_api_name": "Win8.1", "browser_api_name": "Chrome43x64", "name": "Python Parallel"},
]
browsers_waiting = []


def get_browser_and_wait(browser_data):
    print "starting %s\n" % browser_data["browser_api_name"]
    browser = get_browser(browser_data)
    browser.get("http://crossbrowsertesting.com")
    browsers_waiting.append({"data": browser_data, "driver": browser})
    print "%s ready" % browser_data["browser_api_name"]
    while len(browsers_waiting) < len(browsers):
        print "working on %s.... please wait" % browser_data["browser_api_name"]
        browser.get("http://crossbrowsertesting.com")
        time.sleep(3)

threads = []
for i, browser in enumerate(browsers):
    thread = Thread(target=get_browser_and_wait, args=[browser])
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()

print "all browsers ready"
for i, b in enumerate(browsers_waiting):
    print "browser %s's title: %s" % (b["data"]["name"], b["driver"].title)
    b["driver"].quit()
