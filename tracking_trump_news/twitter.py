import tweepy
import time
import yagmail
import pytz

from datetime import datetime
from collections import deque   

#    --------------------------- EDIT THE BELOW LINE TO PUT YOUR EMAIL --------------------------------
# emailToReceiveNotifications = "originalndd@gmail.com"
emailToReceiveNotifications = "kanybekovdaniel6@gmail.com"
# -----------------------------------------------------------------------------------------------------

# ---------------------------------------- Twitter.com ------------------------------------------------
API_KEY = "oNdtdbLBQm5N6i6fS71tp3mqS"
API_SECRET = "Dnk2E4WepWtsgYSrf6EKdQl6fWDCnJqPs1N8XPNcENnq4"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANu1wwEAAAAASVF9hSfZ2R56ZD4B2oL1Yxs4B1s%3DyscYAs9TAnFf5UFskvnrIBmALK20e4sHISUrD0DPQSj355R2QD"
ACCESS_TOKEN = "1763562898851274754-6ai8gelAWVBS9ThX5wFRxoJHGVRQuW"
ACCESS_TOKEN_SECRET = "lVTX8AKZHn14LwANzscAJUTWiiLP9xwleMS7IYi7FcC3z"
# -----------------------------------------------------------------------------------------------------

client = tweepy.Client(bearer_token=BEARER_TOKEN)
username = "TeamTrump"
user = client.get_user(username=username)
user_id = user.data.id

# For checking duplicates of tweets
tweet_ids = deque(maxlen=10)

# email staffs
emailSender = "ph0150167@gmail.com"
appCode = "ocxg sayq czat pclx"
emailReceiver = emailToReceiveNotifications

def sendGmail(title, body):
    print("sending gmail...")

    with yagmail.SMTP(emailSender, appCode) as yag:
        yag.send(to=emailReceiver, subject=title, contents=str(body))

    print("email sent!")
    return True

# main function
def go():
    try:
        # Fetch latest tweets
        tweets = client.get_users_tweets(user_id, max_results=10)
        
        # Check if there are any tweets
        if tweets.data:
            for tweet in tweets.data:
                if tweet.id not in tweet_ids:  # Only add if tweet is new
                    tweet_ids.append(tweet.id)
                    tweet_url = f"https://twitter.com/{username}/status/{tweet.id}"
                    body = tweet.text

                    print("New tweet added:", tweet.text)
                    sendGmail("New tweet added on Trump page!", f"{body}\n{tweet_url}")
                else:
                    print("Duplicate tweet skipped.")
        else:
            print("No tweets found.")

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)  # Wait before retrying in case of an error


last_notification_time = time.time()
# Infinite loop to run the program 24/7
while True:
    go()
    if time.time() - last_notification_time >= 3600:
        eastern = pytz.timezone("US/Eastern")
        eastern_time = datetime.now(eastern)
        sendGmail("Program Status", f"Trump tracking program is still running at {eastern_time.strftime('%Y-%m-%d %H:%M:%S')} in US Eastern Time.(Twitter.com)")
        last_notification_time = time.time()
    time.sleep(60)