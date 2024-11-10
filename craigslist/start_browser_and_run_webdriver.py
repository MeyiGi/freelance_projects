"""
Description: 
Used to start the profile browser, then connected to the browser with webdriver and try google search.
Note: To use this interface, you need to start the MoreLogin client and successfully log in.

Documentation:
https://docs.morelogin.com/l/en/interface-documentation/browser-profile#1_start_browser_profile
"""

# pip install requests pycryptodome Crypto
from base_morelogin.base_func import requestHeader, postRequest

# pip install selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

import sys
import random
import asyncio
import traceback,time

# From profile list page, click on the API button, and copy API ID and API Key to below.
APPID = '1603184696627727'
SECRETKEY = '2a546deb503d4952abf0bd973d8d1e49'
BASEURL = 'http://127.0.0.1:40000'

async def main():
    try:
        profiles = read_txt()
        random_num = random.randint(0, len(profiles) - 1)

        # browser's order num, you can get it from profile list page: Numerical order 
        uniqueId = profiles[random_num].split(": P-")[1]
        # browser profile id, please check API-demo: list_browser_profiles.py
        envId = profiles[random_num].split(": P-")[0]
        debugUrl = await startEnv(envId, uniqueId, APPID, SECRETKEY, BASEURL)
        print(debugUrl)
        
        driver = createWebDriver(debugUrl)
        operationEnv(driver)
    except:
        errorMessage = traceback.format_exc()
        print('run-error: ' + errorMessage)
        print(uniqueId)
        print(envId)

def read_txt(filename="profiles.txt"):
    with open(filename, "r") as file:
        return [item.strip() for item in file.readlines()]

# create webdriver with exist browser
def createWebDriver(debugUrl):
    opts = webdriver.ChromeOptions()
    opts.set_capability('browserVersion', '129')
    opts.add_experimental_option('debuggerAddress', debugUrl)
    driver = webdriver.Chrome(options=opts)
    return driver

# start a browser profile, and return debug-url
# if browser already opened, the browser will auto bring to front
async def startEnv(envId, uniqueId, appId, secretKey, baseUrl):
    requestPath = baseUrl + '/api/env/start'  
    # Send the envId(profile ID) or the uniqueId(profile order number). 
    # If both are sent, the profile ID takes precedence. 
    data = { 
        'envId': envId,
        'uniqueId': uniqueId
    }
    headers = requestHeader(appId, secretKey)
    response = postRequest(requestPath, data, headers).json()

    if response['code'] != 0:
        print(response['msg'])
        print('please check envId')
        sys.exit()

    port = response['data']['debugPort']
    print('env open result:', response['data'])
    return '127.0.0.1:' + port

# open page and operation
def operationEnv(driver):
    # new tab, and open google for search
    driver.switch_to.new_window('tab')
    driver.get('https://www.google.com')

    # wait for page loaded
    wait = WebDriverWait(driver, 10)

    # find input element and fill word
    element = driver.find_element('css selector', '[name="q"]')
    element.send_keys("MoreLogin")
    element.send_keys(Keys.RETURN)
    print('search executed')

    driver.close()

if __name__ == '__main__':
    asyncio.run(main())