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

import threading
from concurrent.futures import ThreadPoolExecutor

lock = threading.Lock()

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

chaves = pd.read_csv("{}/scripts/keys_twitter.csv".format(dir_base))

consumer_key_list = chaves.consumer_key.tolist()
consumer_secret_list = chaves.consumer_secret.tolist()
acess_token_list = chaves.acess_token.tolist()
access_token_secret_list = chaves.access_token_secret.tolist()



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

def para_ou_pega_nova_chave(param_api):
    global consumer_key_list
    global consumer_secret_list
    global acess_token_list
    global access_token_secret_list
    global lock

    trava = False
    api = param_api

    lock.acquire()

    # antes de tenta adquirir nova chave
    # verifica se nao tem mais chaves disponiveis e solta o sleep
    if(len(consumer_key_list) == 0 and
        len(consumer_secret_list) == 0 and
        len(acess_token_list) == 0 and
        len(access_token_secret_list) == 0):

        trava = True
    else:

        # adiciona a chave esgotada no final da fila
        consumer_key_list.append(param_api.auth.consumer_key)
        consumer_secret_list.append(param_api.auth.consumer_secret)
        acess_token_list.append(param_api.auth.access_token)
        access_token_secret_list.append(param_api.auth.access_token_secret)

        # recupera a chave do topo da fila
        auth = tweepy.OAuthHandler(consumer_key_list.pop(), consumer_secret_list.pop())
        auth.set_access_token(acess_token_list.pop(), access_token_secret_list.pop())
        api = tweepy.API(auth, compression=True)

    lock.release()

    if(trava):
        time.sleep(15 * 60)

    return api


# https://www.mapdevelopers.com/geocode_bounding_box.php
# https://stackoverflow.com/questions/30758203/tweepy-location-on-twitter-api-filter-always-throws-406-error

    def limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                # troca a chave
                time.sleep(15 * 60)

    def get_twitter_timeline(user_id):
        # https://twitter.com/intent/user?user_id=145635516
        # 999332724
        user_id = 145635516

        # In this example, the handler is time.sleep(15 * 60),
        # but you can of course handle it in any way you want.


        for follower in limit_handled(tweepy.Cursor(api.followers).items()):
            if follower.friends_count < 300:
                print(follower.screen_name)



        num_pagina = 0

        while True:
            try:
                # tenta recuperar a pagina, se nao conseguir 2 coisas podem acontecer
                # 1 - excedeu o limite de paginas
                # 2 - excedeu o limite de requisicoes a cada 15 min
                page = tweepy.Cursor(api.user_timeline, id = user_id, trim_user=True, exclude_replies=False, include_rts=True, count=200, page=num_pagina ).pages().next()

                num_pagina += 1

                geotagged_tweets = [tweet._json for tweet in page if tweet.geo]
                user_timeline.extend(geotagged_tweets)

            # Se excedeu o numero de requisicoes
            except tweepy.RateLimitError:
                # troca a chave
                api = para_ou_pega_nova_chave(api)
            except tweepy.TweepError as e:
                # se for erro de permissao e 401 - registra e nao faz nada
                # se for erro de que nao tem mais paginas para retornar - termina o while

        pages.next()
        pages.index

        cursor.

        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                # troca a chave
                time.sleep(15 * 60)

        for page in c.pages():
            geotagged_tweets = [tweet._json for tweet in page if tweet.geo]
            user_timeline.extend(geotagged_tweets)









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
    for page in c.pages():
        geotagged_tweets = [tweet._json for tweet in page if tweet.geo]
        user_timeline.extend(geotagged_tweets)

    user_timeline

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

    bytes(json.dumps(user_timeline), 'utf-8')

    # Output result only if there was no error
    if user_timeline is not None and len(user_timeline) > 0:
        with gzip.open(output_filename, "w") as outfile:
            outfile.write(bytes(, "UTF-8"))
        logging.info("User {} - Finished ({} tweets)".format(user_id, len(user_timeline)))
    else:
        logging.info("User {} - Terminated".format(user_id))
