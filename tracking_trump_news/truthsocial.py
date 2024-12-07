# just ignore it
# import os
# os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/home/ubuntu/.cache/ms-playwright"

from playwright.sync_api import Playwright, sync_playwright
from collections import deque
from datetime import datetime

import yagmail
import time
import pytz

# ------------------------------ EDIT THE BELOW LINE TO PUT YOUR EMAIL --------------------------------
emailReceivers = ["originalndd@gmail.com", "kanybekovdaniel777@gmail.com"]
# -----------------------------------------------------------------------------------------------------
queue = deque([], maxlen=3)

# email staffs
emailSender = "ph0150167@gmail.com"
appCode = "ocxg sayq czat pclx"

def sendGmail(title, body):
    for emailReceiver in emailReceivers:
        print("sending gmail...")

        with yagmail.SMTP(emailSender, appCode) as yag:
            yag.send(to=emailReceiver, subject=title, contents=str(body))

        print("email sent!")
    return True

# function for checking post valid
def isValid(link, text: str):
    youtu = text.find("youtu.be")
    foxnews = text.find("foxnews.com")
    
    # copy paste link post
    if youtu != -1 and youtu < 10:
        return False
    
    if foxnews != -1 and foxnews < 10:
        return False

    # checking for duplicate
    return link not in queue

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    page = context.new_page()
    page.goto("https://truthsocial.com/@realDonaldTrump")

    # clicking first post
    page.locator("div[data-index='0']").click()

    # extracting link and text
    link = page.url
    text = page.locator("p p").text_content()
    print(link)

    if not isValid(link, text):
        print("yes")
        return

    # appending link to queue for check duplicates
    queue.append(link)
    sendGmail("(truthsocial.com)New post added on Trump page!", f"{text}\n{link}")

    # ---------------------
    context.close()
    browser.close()


last_notification_time = time.time()
while True:
    # main function
    with sync_playwright() as playwright:
        run(playwright)

    # status code sender
    if time.time() - last_notification_time >= 3600:
        eastern = pytz.timezone("US/Eastern")
        eastern_time = datetime.now(eastern)
        sendGmail("Program Status", f"truthsocial Trump tracking program is still running at {eastern_time.strftime('%Y-%m-%d %H:%M:%S')} in US Eastern Time.")
        last_notification_time = time.time()
    time.sleep(60 * 15)