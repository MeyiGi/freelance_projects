from apify_client import ApifyClient
from datetime import datetime
from collections import deque
import yagmail
import time
import pytz



# ------------------------------- Configurations -------------------------------
client = ApifyClient("apify_api_iJJSoiVM5g7p88ske7DLTOPoakqsvv4lGtc6")

# inputs to apify
run_input = {
    "directUrls": ["https://www.instagram.com/realdonaldtrump/"],
    "resultsType": "posts",
    "resultsLimit": 1,
    "searchType": "hashtag",
    "searchLimit": 1,
    "addParentData": False,
}
# email stuff
emailReceivers = ["originalndd@gmail.com", "kanybekovdaniel777@gmail.com"]
emailSender = "ph0150167@gmail.com"
appCode = "ocxg sayq czat pclx"
# -------------------------------------------------------------------------------

post_ids = deque(maxlen=3)

def sendGmail(title, body):    
    for emailReceiver in emailReceivers[1:]:
        print(f"sending gmail to {emailReceiver}")

        with yagmail.SMTP(emailSender, appCode) as yag:
            yag.send(to=emailReceiver, subject=title, contents=str(body))
        
        print("email sent!")

    return True


def go():
    # Run the Actor and wait for it to finish
    run = client.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if item["id"] in post_ids:
            continue

        print(item)
        
        title = "New Trump instagram post added!"
        body = item["caption"] + "\n" + item["url"]

        sendGmail(title=title, body=body)

        post_ids.append(item["id"])


last_notification_time = time.time()
# Infinite for 24/7 work
while True:
    go()
    time.sleep(1350)

    if time.time() - last_notification_time > 3600:
        eastern = pytz.timezone("US/Eastern")
        eastern_time = datetime.now(eastern)
        sendGmail("Program Status", f"instagram Trump tracking program is still running at {eastern_time.strftime('%Y-%m-%d %H:%M:%S')} in US Eastern Time.")
        last_notification_time = time.time()