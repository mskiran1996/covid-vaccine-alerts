import requests
import json, os
import datetime, time
from os.path import join, dirname
from dotenv import load_dotenv
from fake_useragent import UserAgent

load_dotenv(join(dirname(__file__), '.env'))

"""
# search for @PushitBot on Telegram to get token
# Contents of .env file

PINCODES=533001, 533002, 533003, 533005
MIN_AGE_LIMIT=46
TOKEN=<telegram-token>
INTERVAL=60
"""

EMOJIS = {
    "center_id" : "🆔",
    "name" : "🏥",
    "state_name" : "🗾",
    "district_name" : "🏘️",
    "block_name" : "📍",
    "pincode" : "🔢",
    "from" : "🕐",
    "to" : "🕒",
    "lat" : "🗺️",
    "long" : "🗺️",
    "fee_type" : "💰",
    "session_id" : "🚀",
    "date" : "📅",
    "available_capacity" : "🏺",
    "fee" : "💰",
    "min_age_limit" : "👾",
    "vaccine" : "💉",
    "slots" : "🎰"
}

PINCODES = [p.strip() for p in os.environ.get("PINCODES").split(",")]
MIN_AGE = int(os.environ.get("MIN_AGE_LIMIT"))
TOKEN = os.environ.get("TOKEN")
DATES = lambda r: [(datetime.datetime.today() + datetime.timedelta(days=d)).strftime("%d-%m-%Y") for d in range(0, r)]
INTERVAL = int(os.environ.get("INTERVAL"))
UA = UserAgent()

def get_sessions(pincode, date):
    try:
        # request cowin portal API for available sessions
        res = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pincode, date), headers={'User-Agent':str(UA.random)})
        if res.status_code == 403:
            print("[{}][ERROR] 403 Cowin portal is blocking your IP address".format(datetime.datetime.now()))
        return json.loads(res.text).get("sessions") if res.ok else []
    except Exception as e:
        print(e)
        return []    


def push(string):
    # push data to telegram bot
    requests.get("https://tgbots.skmobi.com/pushit/{}?msg={}".format(TOKEN, string))


def emojify(d):
    try:
        # remove unnecessary data
        for k in ["session_id", "lat", "long", "fee_type"]:
            d.pop(k)
    except: pass
    
    # parse dict to readable message
    string = ""
    for (k,v) in d.items():
        if k == "slots":
            v = ", ".join(v).replace("-", " - ")
        string += "{} {} = {}\n".format(EMOJIS.get(k), k.replace("_", " ").title(), v)
    return string

# Event Loop
while True:
    for pincode in PINCODES:
        # check for next 2 days
        for date in DATES(2):
            print("[{}][INFO] fetching data for date: {}, PINCODE: {}".format(datetime.datetime.now(), date, pincode))
            # fetch data from cowin portal
            sessions = get_sessions(pincode, date)
            
            # parse session details
            for s in sessions:
                try:
                    if MIN_AGE >= s.get("min_age_limit"):
                        message = emojify(s)
                        print(message)
                        # send message to telegram
                        push(message)
                except Exception as e:
                    print(e)
    print("[{}][INFO] sleeping for {} seconds".format(datetime.datetime.now(), INTERVAL))
    time.sleep(INTERVAL)
