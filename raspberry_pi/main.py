import json
import os
import time
import urllib.request, json
import datetime
import tweepy
from mastodon import Mastodon
import random
import time
testmode = True
if testmode != True:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    print("Mode: operational")
else:
    print("Mode: test")


def textselect(min, max):
    number = random.randint(0, 1)

    if number == 0:
        return 0
    else:
        return random.randint(min, max)


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
print("dir path is", dir_path)

# starting by configuring the bot
file_configure_path = dir_path + os.sep + "config.json"
with open(file_configure_path, 'r') as f:
    data_config = json.load(f)

path = data_config["path"]


TWITTER_CONSUMER_KEY = data_config["twitter_api"]["consumer_key"]
TWITTER_CONSUMER_SECRET = data_config["twitter_api"]["consumer_secret"]
TWITTER_ACCESS_KEY = data_config["twitter_api"]["token"]
TWITTER_ACCESS_SECRET = data_config["twitter_api"]["token_secret"]

twitter_auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
twitter_auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(twitter_auth)


MASTODON_ACCESS_TOKEN = data_config["mastodon_api"]["access_token"]
MASTODON_API_BASE_URL = data_config["mastodon_api"]["api_base_url"]




state = 1
state_b4 = 1


while True:

    if testmode != True:
        if GPIO.input(12) == GPIO.HIGH:
            #print("button was pushed:")
        
            state = 1
        
    
        if GPIO.input(12) == GPIO.LOW:
            #print("button was not pushed:")
            state = 0
    else:
        # just toggles the states for test mode!
        if state == 0:
            state = 1
        else:
            state = 0


    time_now = time.time()
    
    file_status_path = dir_path + os.sep + "status.json"
    
    if state == 1 and state_b4 == 0:
        
        if os.path.exists(file_status_path) == True:
            with open(file_status_path, 'r') as f:
                    data_status = json.load(f)
        
        number = len(data_status["opening_text"])
        number = textselect(0, number - 1)


        time_opening = datetime.datetime.fromtimestamp(int(time_now)).strftime('%Y-%m-%d %H:%M:%S')
        texts = data_status["opening_text"][number]["text"]

        if TWITTER_ACCESS_KEY != "fill in your data!":
            if texts.get("twitter") != None:
                text = texts["twitter"] + " [OPEN:" + time_opening + "]"

            else:
                text = texts["universal"] + " [OPEN:" + time_opening + "]"


            print("twitter text:", text)

            if testmode != True:
                try:
                    twitter_api.update_status(text)
                    # same text as before cannot be posted!
                except:
                    print(time_now, "did not tweet opening status")



        if MASTODON_ACCESS_TOKEN != "fill in your data!":

            if texts.get("mastodon") != None:
                text = texts["mastodon"] + " [OPEN:" + time_opening + "]"

            else:
                text = texts["universal"] + " [OPEN:" + time_opening + "]"


            print("mastodon text:", text)

            if testmode != True:
                try:
                    mastodon = Mastodon(
                        access_token=MASTODON_ACCESS_TOKEN,
                        api_base_url=MASTODON_API_BASE_URL
                    )
                    mastodon.toot(text)
                except:
                    print(time_now, "did not toot closing status", time_closing)



    if state == 0 and state_b4 == 1:
        #print("closed")
        
        if os.path.exists(file_status_path) == True:
            with open(file_status_path, 'r') as f:
                    data_status = json.load(f)
        
        number = len(data_status["closing_text"])
        number = textselect(0, number - 1)


        time_closing = datetime.datetime.fromtimestamp(int( time_now )).strftime('%Y-%m-%d %H:%M:%S')
        texts = data_status["closing_text"][number]["text"]

        if MASTODON_ACCESS_TOKEN != "fill in your data!":
            if texts.get("twitter") != None:
                text = texts["twitter"] + " [CLOSED:" + time_closing + "]"

            else:
                text = texts["universal"] + " [CLOSED:" + time_closing + "]"

                    
            print("twitter text:", text)

            if testmode != True:
                try:
                    twitter_api.update_status(text)
                    # same text as before cannot be posted!
                except:
                    print(time_now, "did not tweet closing status")



        if MASTODON_ACCESS_TOKEN != "fill in your data!":
            if texts.get("mastodon") != None:
                text = texts["mastodon"] + " [CLOSED:" + time_closing + "]"

            else:
                text = texts["universal"] + " [CLOSED:" + time_closing + "]"


            print("mastodon text:", text)

            if testmode != True:
                try:
                    mastodon = Mastodon(
                        access_token=MASTODON_ACCESS_TOKEN,
                        api_base_url=MASTODON_API_BASE_URL
                    )
                    mastodon.toot(text)
                except:
                    print(time_now, "did not toot closing status", time_closing)


    state_b4 = state
    
    time.sleep(10)