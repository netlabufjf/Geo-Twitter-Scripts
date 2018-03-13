import pandas as pd
import os
# dir_base = os.path.abspath(os.path.dirname(__file__))
dir_base = os.path.abspath(os.getcwd())

df = pd.read_csv("{}/scripts/keys_twitter.csv".format(dir_base))

consumer_key_list = df.consumer_key.tolist()
consumer_secret_list = df.consumer_secret.tolist()
acess_token_list = df.acess_token.tolist()
access_token_secret_list = df.access_token_secret.tolist()

import threading
from concurrent.futures import ThreadPoolExecutor

lock = threading.Lock()


def funcao_para_thread():
    global df
    global lock

    lock.acquire()

    # adquire as chaves

    lock.release()
