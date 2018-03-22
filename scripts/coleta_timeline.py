# from concurrent.futures import ThreadPoolExecutor
import cria_listas as crialistas
import glob
import gzip
import json
import logging
import os
import pandas as pd
import socket
import sys
import threading
import time
import tweepy
# import networkx as nx
# import threading

hostname = socket.gethostname()

dir_base = os.path.abspath(os.path.dirname(__file__))+"/.."
# dir_base = os.path.abspath(os.getcwd())

# sys.path = ["{}/libs/twitter".format(dir_base)]+sys.path

logging.basicConfig(filename="{}/logs/collect_users_timelines.{}.log".format(dir_base, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")

lock = threading.Lock()

chaves = pd.read_csv("{}/data/keys_twitter.csv".format(dir_base))

consumer_key_list = chaves.consumer_key.tolist()
consumer_secret_list = chaves.consumer_secret.tolist()
acess_token_list = chaves.acess_token.tolist()
access_token_secret_list = chaves.access_token_secret.tolist()


def libera_chave(param_api):
    global consumer_key_list
    global consumer_secret_list
    global acess_token_list
    global access_token_secret_list
    global lock

    lock.acquire()

    logging.info("Leave api key - {}".format(param_api.auth.consumer_key))

    # adiciona a chave no final da fila
    consumer_key_list.append(param_api.auth.consumer_key)
    consumer_secret_list.append(param_api.auth.consumer_secret)
    acess_token_list.append(param_api.auth.access_token)
    access_token_secret_list.append(param_api.auth.access_token_secret)

    lock.release()


def pega_nova_chave():
    global consumer_key_list
    global consumer_secret_list
    global acess_token_list
    global access_token_secret_list
    global lock

    while True:
        # verifico se a lista nao esta vazia
        if(len(consumer_key_list) == 0 and
                len(consumer_secret_list) == 0 and
                len(acess_token_list) == 0 and
                len(access_token_secret_list) == 0):

            time.sleep(2)
        else:
            lock.acquire()

            passou_pelo_lock = True

            # garante dentro do lock que nao esta vazio
            if(len(consumer_key_list) > 0 and
                    len(consumer_secret_list) > 0 and
                    len(acess_token_list) > 0 and
                    len(access_token_secret_list) > 0):

                # recupera a chave do topo da fila
                auth = tweepy.OAuthHandler(consumer_key_list.pop(), consumer_secret_list.pop())
                auth.set_access_token(acess_token_list.pop(), access_token_secret_list.pop())
                api = tweepy.API(auth, compression=True)

                logging.info("Change api key to - {}".format(api.auth.consumer_key))

            lock.release()

            if passou_pelo_lock:
                    return api


def coloca_chave_de_castigo(api_param):
    logging.info("Sleeped api key for 15min- {}".format(api_param.auth.consumer_key))
    time.sleep(15*60)
    libera_chave(api_param)


def get_twitter_timeline(user_id, cidade):
    # https://twitter.com/intent/user?user_id=145635516

    api = pega_nova_chave()

    dir_cidade = "{}/data/{}/user_timeline".format(dir_base, cidade)

    if not os.path.exists(dir_cidade):
        os.makedirs(dir_cidade)

    output_filename = "{}/{}.json.gz".format(dir_cidade, user_id)

    # Skip user if it was already collected
    if os.path.exists(output_filename):
        logging.info("[{}] User {} - Skipped".format(cidade, user_id))
        return

    # Senao existe usuario coletado...
    logging.info("[{}] User {} - Starting".format(cidade, user_id))

    # pagina 1 e pagina 0 sao a mesma pagina
    num_pagina = 1
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
                # coloca chave de castigo
                t = threading.Thread(target=coloca_chave_de_castigo, args=(api,))
                t.start()
                # troca a chave
                api = pega_nova_chave()
            else:
                if e.response.status_code == 401:
                    crialistas.add_lista_perfil_restrito(user_id, cidade)
                # Se o erro for outro, registra e sai do loop
                logging.warning("[{}] User {} - Error Status: {} - Reason: {} - Error: {}".format(
                    cidade, user_id, e.response.status_code, e.response.reason, e.response.text))
                break

    libera_chave(api)

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
                    "[{}] User {} - Erro ao gerar bytes para escrita no json".format(cidade, user_id))
        logging.info("[{}] User {} - Finished ({} tweets)".format(cidade, user_id, len(user_timeline)))
    else:
        crialistas.add_lista_nogeotagged(user_id, cidade)
        logging.info("[{}] User {} - Terminated - no geotagged tweets".format(cidade, user_id))


def coleta_do_arquivo(nome_arquivo, cidade):

    arquivo = open(nome_arquivo, 'r')
    for line in arquivo.readlines():
        get_twitter_timeline(line.rstrip(), cidade)

    arquivo.close()


cidades = ["london", "saopaulo", "tokyo", "nyc"]


# with ThreadPoolExecutor(max_workers=20) as workers:
#     for cidade in cidades:
#         dir_cidade = "{}/data/{}".format(dir_base, cidade)
#        if os.path.exists(dir_cidade):
#             for file in glob.glob("{}/[0-9]*.id_users.list.csv".format(dir_cidade)):
#                 print file
#                 workers.submit(coleta_do_arquivo, file, cidade)


threads_poll = []

for cidade in cidades:
    dir_cidade = "{}/data/{}".format(dir_base, cidade)
    if os.path.exists(dir_cidade):
        for file in glob.glob("{}/[0-9]*.id_users.list.csv".format(dir_cidade)):
            print file
            t = threading.Thread(target=coleta_do_arquivo, args=(file, cidade))
            t.start()
            threads_poll.append(t)


# get_twitter_timeline(114359580, "london")

# workers.submit(get_twitter_timeline, 145635516, "london")
# workers.submit(get_twitter_timeline, 999332724, "london")

# t_1 = threading.Thread(target=get_twitter_timeline, args=(145635516, "london"))
# t_1.start()

# t_2 = threading.Thread(target=get_twitter_timeline, args=(999332724, "london"))
# t_2.start()
