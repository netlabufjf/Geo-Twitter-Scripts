import tweepy
import socket
import threading
hostname = socket.gethostname()

import os
#dir_base = os.path.abspath(os.path.dirname(__file__))
dir_base = os.path.abspath(os.getcwd())

import sys
# https://github.com/sixohsix/twitter
sys.path = ["{}/libs/twitter".format(dir_base)]+sys.path

#import twitter

import logging
logging.basicConfig(filename="{}/logs/collect_users_timelines.{}.log".format(dir_base, hostname), filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")

import time
import json
import gzip
import pandas as pd

#Graph library
import networkx as nx

#import keys from keys.py
#from keys import consumer_key, consumer_secret, access_token, access_token_secret
execfile("{}/scripts/keys.py".format(dir_base))

# Go to http://dev.twitter.com and create an app (apps.twitter.com).
# The consumer key and secret will be generated for you after
#consumer_key = ""
#consumer_secret = ""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
#access_token = ""
#access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

# https://www.mapdevelopers.com/geocode_bounding_box.php
# https://stackoverflow.com/questions/30758203/tweepy-location-on-twitter-api-filter-always-throws-406-error

#def get_twitter_timeline(user_id):

user_id = 999332724

output_filename = "{}/data/user_timeline/{}.json.gz".format(dir_base, user_id)

# Skip user if it was already collected
if os.path.exists(output_filename):
    logging.info("[User {} - Skipped".format(user_id))
# Collect all tweets of the user
else:
    logging.info("User {} - Starting".format(user_id))

    user_timeline = []

    #try:
    c = tweepy.Cursor(api.user_timeline, id = user_id, trim_user=True, exclude_replies=False, include_rts=True, count=200)

    c

    for page in c.pages():
        geotagged_tweets = [tweet._json for tweet in page if tweet.geo]
        user_timeline.extend(geotagged_tweets)

    # API error
    except tweepy.RateLimitError:
        rates = api.rate_limit_status()
        rate_limit_reset = rates["resources"]["statuses"]["/statuses/user_timeline"]["reset"]
        to_sleep = max(rate_limit_reset - int(time.time()), 0)
        logging.warning("User {} - Rate limit exceeded, sleeping {} seconds".format(user_id, to_sleep+1))
        time.sleep(to_sleep+1)
    except tweepy.TweepError, error:
        logging.warning("User {} - API error code: {} - Message: {}".format(user_id, error.message[0]['code'],error.message[0]['message']))
    except:
        e = sys.exc_info()[0]
        logging.warning("User {} - Sys Error: {}".format(user_id, e))


    # Output result only if there was no error
    if user_timeline is not None and len(user_timeline) > 0:
        with gzip.open(output_filename, "w") as outfile:
            outfile.write(bytes(json.dumps(user_timeline), "UTF-8"))
        logging.info("User {} - Finished ({} tweets)".format(user_id, len(user_timeline)))
    else:
        logging.info("User {} - Terminated".format(user_id))
