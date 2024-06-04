import argparse
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from search import getRoute

#import function from search.py and use it to return a route after passing start and end page

def main(args):
    getRoute(args.start, args.end)



#use selenium to follow that route
#basic selenium setup for searching google:

# service = Service(executable_path='chromedriver.exe')
# driver = webdriver.Chrome(service=service)

# driver.get("https://google.com")

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
# )

# input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
# input_element.clear()
# input_element.send_keys("blahblah" + Keys.ENTER)

# time.sleep(5)
# driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find shortest route between two Wikipedia pages (english pages only)')
    parser.add_argument('start', help="the start page title")
    parser.add_argument('end', help="the end page title")
    args = parser.parse_args()
    main(args)