import requests
import ast
import pandas as pd
import os
import time
import pytz
import yagmail
from datetime import datetime

market_list = [
    "bolsonaro-arrested-in-2024",
    "will-wicked-opening-weekend-gross-more-than-twice-gladiator-2",
    "presidential-election-winner-2024?tid=1730809861381",
    "mrbeast-x-ronaldo-video-views-on-day-1-nov-30",
    "nba-mvp-2024-25",
    "largest-company-eoy",
    "will-icc-withdraw-its-arrest-warrant-against-netanyahu-before-july",
    "another-monkeypox-case-in-us-in-2024",
    "michel-barnier-out-as-prime-minister-of-france-in-2024",
    "scorigami-in-nfl-week-12",
    "michel-barnier-out-as-prime-minister-of-france-in-2024"
]

#    --------------------------- EDIT THE BELOW LINE TO PUT YOUR EMAIL --------------------------------
emailReceivers = ["originalndd@gmail.com", "kanybekovdaniel6@gmail.com"]
#    --------------------------------------------------------------------------------------------------

emailSender = "ph0150167@gmail.com"
appCode = "ocxg sayq czat pclh" # x

def sendGmail(title, body):
    for emailReceiver in emailReceivers[1:]:
        print("sending gmail...")

        with yagmail.SMTP(emailSender, appCode) as yag:
            yag.send(to=emailReceiver, subject=title, contents=str(body))

        print("email sent!")
    return True

def updateDatabase(df, question, yes, no):
    print(f"updating question \"{question}\"")
    for index, row in df.iterrows():
        if row['question'] == question:
            df.at[index, 'yes'] = yes
            df.at[index, 'no'] = no

def checkQuestion(df, question, yes, no, slug):
    questionEventUrl = "https://polymarket.com/event/"+slug
    for x, y in df.iterrows():
        print(y)

        if y['question'] == question:
            print(abs(yes-y['yes'])*100)
            if abs(yes-y['yes'])*100 >= 5:
                print(f"old values: {y['yes']}  {y['no']}")
                print(f"new values: {yes}, {no}")
                updateDatabase(df, question, yes, no)
                sendGmail("Percentage difference of more than or qual to 5% detected", f"Difference found of {abs(yes-y['yes'])*100}% , New market:\n{question} ----> YES:{str(round(yes*100))}%    NO:{str(round(no*100))}%\nOld market:\n{question} ----> YES:{str(round(y['yes']*100))}%    NO:{str(round(y['no']*100))}\n{questionEventUrl}")
                return True
    
    return False

def saveNewData(data):
    df = pd.DataFrame(data)
    df.columns = ['question', 'yes', 'no']

    df.to_csv("database.csv", index=False)

def go(slug):
    try:
        response = requests.get(f"https://gamma-api.polymarket.com/events?slug={slug}") 
        response = response.json()[0]
    except Exception as e:
        print(e)
        return
    
    df = pd.DataFrame()
    
    if os.path.exists("database.csv"):
        df = pd.read_csv("database.csv")
        
    marketHistory = []

    for y in response['markets']:
        try:
            yesInt, noInt = [float(a) for a in ast.literal_eval(y['outcomePrices'])]
            yes, no = str(round(yesInt*100))+"%", str(round(noInt*100))+"%"
        except:
            yes, no = ["ERROR"]*2


        if not checkQuestion(df, y['question'], yesInt, noInt, slug):
            continue

        marketHistory.append([y['question'], yesInt, noInt])
        
    if marketHistory:
        saveNewData(marketHistory)

last_notification_time = time.time()

while True:
    for slug in market_list:
        print(slug)
        go(slug=slug)
        if time.time() - last_notification_time >= 3600:
            eastern = pytz.timezone("US/Eastern")
            eastern_time = datetime.now(eastern)
            sendGmail("Program Status", f"PolyMarket program is still running at {eastern_time.strftime('%Y-%m-%d %H:%M')} in US Eastern Time.")
            last_notification_time = time.time()
        time.sleep(5)