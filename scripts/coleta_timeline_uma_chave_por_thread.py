# from concurrent.futures import ThreadPoolExecutor
import apaga_listas as apagalistas
import cria_listas as crialistas
import gzip
import json
import logging
import os
import pandas as pd
import socket
import sys
import tweepy
import verifica_listas as verificalistas
# import networkx as nx
# import threading

cidade = sys.argv[1]
lista_de_ids = sys.argv[2]
id_key = int(sys.argv[3])


hostname = socket.gethostname()

dir_base = os.path.abspath(os.path.dirname(__file__))+"/.."

# print dir_base
# dir_base = os.path.abspath(os.getcwd())

# sys.path = ["{}/libs/twitter".format(dir_base)]+sys.path

logging.basicConfig(filename="{}/logs/collect_users_timelines.{}.log".format(dir_base, hostname),
                    filemode="a", level=logging.INFO, format="[ %(asctime)s ] [%(levelname)s] %(message)s")

chaves = pd.read_csv("{}/data/keys_twitter.csv".format(dir_base))

# recupera a chave do topo da fila
auth = tweepy.OAuthHandler(chaves.consumer_key[id_key], chaves.consumer_secret[id_key])
auth.set_access_token(chaves.acess_token[id_key], chaves.access_token_secret[id_key])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

logging.info("Use api key - {}".format(api.auth.consumer_key))


def get_twitter_timeline(user_id, cidade):
    # https://twitter.com/intent/user?user_id=145635516

    global api

    dir_cidade = "{}/data/{}".format(dir_base, cidade)
    dir_cidade_timelines = "{}/data/{}/user_timeline".format(dir_base, cidade)

    if not os.path.exists(dir_cidade_timelines):
        os.makedirs(dir_cidade_timelines)

    output_filename = "{}/{}.json.gz".format(dir_cidade_timelines, user_id)

    # Skip user if it was already collected
    if os.path.exists(output_filename):
        logging.info("[{}] User {} - Skipped".format(cidade, user_id))
        return

    # Skip user if it was already in nogeotagged list
    if verificalistas.in_lista_nogeotagged(user_id, cidade):
        logging.info("[{}] User {} - Skipped - in nogeotagged".format(cidade, user_id))
        return

    # Skip user if it was already in restrict list
    if verificalistas.in_lista_perfil_restrito(user_id, cidade):
        logging.info("[{}] User {} - Skipped - in restrict list".format(cidade, user_id))
        return

    # Skip user if it was already but crashed
    if verificalistas.in_lista_processados(user_id, cidade):
        logging.info("[{}] User {} - Skipped - in processados list".format(cidade, user_id))
        return

    # Senao existe usuario coletado...
    logging.info("[{}] User {} - Starting".format(cidade, user_id))

    # Add na lista de processados
    crialistas.add_lista_processados_com_erro(user_id, cidade)

    user_timeline = []

    coletou = False
    while not coletou:
        try:
            # tenta recuperar a pagina, se nao conseguir 2 coisas podem acontecer
            # 1 - excedeu o limite de paginas
            # 2 - excedeu o limite de requisicoes a cada 15 min
            c = tweepy.Cursor(api.user_timeline, id=user_id, trim_user=True,
                              exclude_replies=False, include_rts=True, count=200)
            for page in c.pages():
                geotagged_tweets = [tweet._json for tweet in page if tweet.geo]
                user_timeline.extend(geotagged_tweets)

            coletou = True

            apagalistas.remove_line(
                user_id, "{}/processados_erro.id_users.list.csv".format(dir_cidade))

        except tweepy.TweepError as e:

            if e.response is not None:
                if e.response.status_code is not None:

                    # Se excedeu o numero de requisicoes
                    if e.response.status_code == 429:
                        user_timeline = []
                        logging.warning("[{}] User {} - Error Status: {} - Reason: {} - Error: {}".format(
                            cidade, user_id, e.response.status_code, e.response.reason, e.response.text))
                        logging.warning(
                            "[{}] User {} - Coletando novamente".format(cidade, user_id))
                    else:
                        if e.response.status_code == 401:
                            crialistas.add_lista_perfil_restrito(user_id, cidade)
                        # Se o erro for outro, registra e sai do loop
                        logging.warning("[{}] User {} - Error Status: {} - Reason: {} - Error: {}".format(
                            cidade, user_id, e.response.status_code, e.response.reason, e.response.text))

                        coletou = True

                        apagalistas.remove_line(
                            user_id, "{}/processados_erro.id_users.list.csv".format(dir_cidade))

        except Exception as e:
            # Se o erro for outro, registra e sai do loop
            logging.warning("[{}] User {} - Erro Desconhecido: {} - Reason: {} - Error: {}".format(
                cidade, user_id, e.message))
            coletou = True

            apagalistas.remove_line(
                user_id, "{}/processados_erro.id_users.list.csv".format(dir_cidade))

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
        logging.info("[{}] User {} - Finished ({} tweets)".format(cidade,
                                                                  user_id, len(user_timeline)))
    else:
        crialistas.add_lista_nogeotagged(user_id, cidade)
        logging.info("[{}] User {} - Terminated - no geotagged tweets".format(cidade, user_id))


def coleta_do_arquivo(nome_arquivo, cidade):

    while 1:
        # open in read / write mode
        with open(nome_arquivo, 'r+') as arquivo:
            linha = arquivo.readline()
            if not linha:
                break
            # read the first line and use
            get_twitter_timeline(linha.rstrip(), cidade)
            # read the rest
            data = arquivo.read()
            # set the cursor to the top of the file
            arquivo.seek(0)
            # write the data back
            arquivo.write(data)
            # set the file size to the current size
            arquivo.truncate()
            arquivo.close()


coleta_do_arquivo(lista_de_ids, cidade)
