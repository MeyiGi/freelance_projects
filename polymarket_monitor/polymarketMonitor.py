import requests
from bs4 import BeautifulSoup as bs
import ast
import pandas as pd
from email.message import EmailMessage
import ssl
import os
import smtplib
import time
from datetime import datetime
import pytz
import yagmail


#    --------------------------- EDIT THE BELOW LINE TO PUT YOUR EMAIL --------------------------------
emailReceivers = ["originalndd@gmail.com", "kanybekovdaniel6@gmail.com"]
#    --------------------------------------------------------------------------------------------------
#  for example, it will ignore the updates that contain both trump and kamala (if there is only one it will let it pass), both furry and trend, and cricket. BUT if there is the word "next" in those updates, it will bypass the checks and deliver the update. So something like "trump beats kamala" will not pass but "trump will beat kamala in the next elections" will pass!
#excluders = ["trump AND kamala", "furry AND trend", "cricket"]
#includers = ["next"]

excluders = ["cricket", "Poker", "Solana", "Bitcoin", "Ethereum", "reach $", "above $", "tweet AND times"]
includers = ["bitcoin"]

#    --------------------------------------------------------------------------------------------------
eventLimit = 10  # max is 100
#    --------------------------------------------------------------------------------------------------


emailSender = "ph0150167@gmail.com"
appCode = "ocxg sayq czat pclx" # x

def sendGmail(title, body):
    try:
        for emailReceiver in emailReceivers[1:]:
            print("sending gmail...")

            with yagmail.SMTP(emailSender, appCode) as yag:
                yag.send(to=emailReceiver, subject=title, contents=str(body))

            print("email sent!")
        return True
    except Exception:
        time.sleep(120)

def checkQuestion(df, question, yes, no, slug):
    questionExisted = False

    questionEventUrl = "https://polymarket.com/event/"+slug
    print(slug)
    for x, y in df.iterrows():
        
        if y['question'] == question:
            questionExisted = True
            if abs(yes-y['yes'])*100 >= 5:
                print(f"old values: {y['yes']}  {y['no']}")
                print(f"new values: {yes}, {no}")
                updateDatabase(df, question, yes, no)
                # sendGmail("Percentage difference of more than or qual to 5% detected", f"Difference found of {abs(yes-y['yes'])*100}% , New market:\n{question} ----> YES:{str(round(yes*100))}%    NO:{str(round(no*100))}%\nOld market:\n{question} ----> YES:{str(round(y['yes']*100))}%    NO:{str(round(y['no']*100))}\n{questionEventUrl}")
                
    if not questionExisted:
        sendGmail("New market added on polymarket!", f'''{question}\tYES:{str(round(yes*100))}%    NO:{str(round(no*100))}%\n{questionEventUrl}''')
        return False
        
    return True
            
def updateDatabase(df, question, yes, no):
    print(f"updating question \"{question}\"")
    for index, row in df.iterrows():
        if row['question'] == question:
            df.at[index, 'yes'] = yes
            df.at[index, 'no'] = no
            
            


def saveNewData(data):
    df = pd.DataFrame(data)
    df.columns = ['question', 'yes', 'no']

    df.to_csv("database.csv", index=False)


def allowQuestion(question):
    for excluder in excluders:
        for includer in includers:
            if all(word in question for word in includer.split("AND")):
                return True
            if all(word.replace(" ", "") in question for word in excluder.split("AND")):
                return False
    return True

def go():
    try:
        response = requests.get(f"https://gamma-api.polymarket.com/events?limit={eventLimit}&active=true&archived=false&closed=false&order=startDate&ascending=false&offset=20&exclude_tag_id=100639") 
        #response = requests.get("https://gamma-api.polymarket.com/events?limit={eventLimit}&active=true&archived=false&closed=false&order=startDate&ascending=false&offset=20&exclude_tag_id=100639", verify=False)
        #?start_date_min=2024-10-05
        response = response.json()
    except Exception as e:
        print(e)
        return
    
    df = pd.DataFrame()
    
    if os.path.exists("database.csv"):
        df = pd.read_csv("database.csv")
        
    marketHistory = []
    for x in response:
        try:
            slug = x['slug']
            for y in (x['markets']):
                try:
                    yesInt, noInt = [float(a) for a in ast.literal_eval(y['outcomePrices'])]
                    yes, no = str(round(yesInt*100))+"%", str(round(noInt*100))+"%"
                except:
                    yes, no = ["ERROR"]*2

                if not allowQuestion(y['question']): continue


                if checkQuestion(df, y['question'], yesInt, noInt, slug):
                    continue

                marketHistory.append([y['question'], yesInt, noInt])
        except Exception as e:
            continue
        
    if marketHistory:
        saveNewData(marketHistory)

last_notification_time = time.time()

while True:
    go()
    if time.time() - last_notification_time >= 3600:
        print("yes")
        eastern = pytz.timezone("US/Eastern")
        eastern_time = datetime.now(eastern)
        sendGmail("Program Status", f"PolyMarket program is still running at {eastern_time.strftime('%Y-%m-%d %H:%M')} in US Eastern Time.")
        last_notification_time = time.time()
    time.sleep(5)