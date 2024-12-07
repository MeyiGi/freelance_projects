import requests
import yagmail
import pytz
import datetime
import time

from collections import deque
from bs4 import BeautifulSoup


# ------------------------------ EDIT THE BELOW LINE TO PUT YOUR EMAIL --------------------------------
emailReceivers = ["originalndd@gmail.com", "kanybekovdaniel777@gmail.com"]
# -----------------------------------------------------------------------------------------------------

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

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


def go():
    response = requests.get("https://rumble.com/c/DonaldTrump", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    href = soup.select_one(".videostream:nth-child(1) a").get("href")
    text = soup.select_one(".videostream:nth-child(1) a h3").text.strip()
    link = "https://rumble.com" + href

    if link in queue:
        return
    
    queue.append(link)

    sendGmail("(rumble.com)New post added on Trump page!", f"{text}\n{link}")


last_notification_time = time.time()

while True:
    go()
    if time.time() - last_notification_time >= 3600:
        eastern = pytz.timezone("US/Eastern")
        eastern_time = datetime.now(eastern)
        sendGmail("Program Status", f"rumble Trump tracking program is still running at {eastern_time.strftime('%Y-%m-%d %H:%M:%S')} in US Eastern Time.")
        last_notification_time = time.time()
    time.sleep(60 * 5)