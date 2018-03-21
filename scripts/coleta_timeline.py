import cria_lista_perfil_restrito as pr
import tweepy
import socket
import threading
import os
import sys
import logging
import time
import json
import gzip
import pandas as pd
# import networkx as nx
# import threading
# from concurrent.futures import ThreadPoolExecutor

hostname = socket.gethostname()

# dir_base = os.path.abspath(os.path.dirname(__file__))
dir_base = os.path.abspath(os.getcwd())

sys.path = ["{}/libs/twitter".format(dir_base)]+sys.path

logging.basicConfig(filename="{}/logs/collect_users_timelines.{}.log".format(dir_base, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")

lock = threading.Lock()

chaves = pd.read_csv("{}/scripts/keys_twitter.csv".format(dir_base))

consumer_key_list = chaves.consumer_key.tolist()
consumer_secret_list = chaves.consumer_secret.tolist()
acess_token_list = chaves.acess_token.tolist()
access_token_secret_list = chaves.access_token_secret.tolist()


def para_ou_pega_nova_chave(param_api=None):
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
        if(param_api is not None):

            logging.info("Leave api key - {}".format(param_api.auth.consumer_key))

            # adiciona a chave esgotada no final da fila
            consumer_key_list.append(param_api.auth.consumer_key)
            consumer_secret_list.append(param_api.auth.consumer_secret)
            acess_token_list.append(param_api.auth.access_token)
            access_token_secret_list.append(param_api.auth.access_token_secret)

        # recupera a chave do topo da fila
        auth = tweepy.OAuthHandler(consumer_key_list.pop(), consumer_secret_list.pop())
        auth.set_access_token(acess_token_list.pop(), access_token_secret_list.pop())
        api = tweepy.API(auth, compression=True)

        logging.info("Change api key to - {}".format(api.auth.consumer_key))

    lock.release()

    if(trava):
        # time.sleep(15 * 60)
        # espera 15 segundos e tenta novamente
        time.sleep(15)

    return api


def get_twitter_timeline(user_id, cidade):
    # https://twitter.com/intent/user?user_id=145635516

    api = para_ou_pega_nova_chave()

    dir_cidade = "{}/data/{}/user_timeline".format(dir_base, cidade)

    if not os.path.exists(dir_cidade):
        os.makedirs(dir_cidade)

    output_filename = "{}/{}.json.gz".format(dir_cidade, user_id)

    # Skip user if it was already collected
    if os.path.exists(output_filename):
        logging.info("User {} - Skipped".format(user_id))
        return

    # Senao existe usuario coletado...
    logging.info("User {} - Starting".format(user_id))

    num_pagina = 0
    user_timeline = []

    while True:
        try:
            # tenta recuperar a pagina, se nao conseguir 2 coisas podem acontecer
            # 1 - excedeu o limite de paginas
            # 2 - excedeu o limite de requisicoes a cada 15 min
            page = tweepy.Cursor(api.user_timeline, id=user_id, trim_user=True,
                                 exclude_replies=False, include_rts=True, count=200, page=num_pagina).pages().next()

            num_pagina += 1

            geotagged_tweets = [tweet._json for tweet in page if tweet.geo]
            user_timeline.extend(geotagged_tweets)

        except StopIteration:
            # se for erro de que nao tem mais paginas para retornar - termina o while
            break
        except tweepy.TweepError as e:
            # Se excedeu o numero de requisicoes
            if e.response.status_code == 429:
                # troca a chave
                api = para_ou_pega_nova_chave(api)
            else:
                if e.response.status_code == 401:
                    pr.add_lista_perfil_restrito(user_id, cidade)
                # Se o erro for outro, registra e sai do loop
                logging.warning("User {} - Error Status: {} - Reason: {} - Error: {}".format(
                    user_id, e.response.status_code, e.response.reason, e.response.text))
                break

    # Se foram coletados tweets geolocalizados...
    if user_timeline is not None and len(user_timeline) > 0:
        with gzip.open(output_filename, "w") as outfile:
            try:
                # se python 2.7
                if sys.version_info[0] < 3:
                    dump = str(json.dumps(user_timeline))
                else:
                    dump = bytes(json.dumps(user_timeline), "UTF-8")
                outfile.write(dump)
            except Exception:
                logging.warning(
                    "User {} - Erro ao gerar bytes para escrita no json".format(user_id))
        logging.info("User {} - Finished ({} tweets)".format(user_id, len(user_timeline)))
    else:
        logging.info("User {} - Terminated".format(user_id))


get_twitter_timeline(145635516, "london")

t_1 = threading.Thread(target=get_twitter_timeline, args=(145635516, "london"))
t_1.start()

t_2 = threading.Thread(target=get_twitter_timeline, args=(999332724, "london"))
t_2.start()
