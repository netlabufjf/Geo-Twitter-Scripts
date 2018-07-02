import gzip
import json
import matplotlib.pyplot as plt
import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
import os
import pandas as pd
import sys


# caminho_desse_arquivo = os.path.abspath(os.path.dirname(__file__))
# dir_base = caminho_desse_arquivo+"/../.."

caminho_desse_arquivo = "/home/rooke/Projetos/mestrado/Geo-Twitter-Scripts/scripts/teste"

input_filename = '{}/1000028444.json.gz'.format(caminho_desse_arquivo)


def extract_list_geo(input_filename):
    #  Extrai o formato link_data:
    with gzip.open(input_filename, "rb") as input_file:
        json_bytes = input_file.read()

        if sys.version_info[0] < 3:
            json_str = json_bytes
        else:
            json_str = json_bytes.decode('utf-8')

        data = json.loads(json_str)

        dados = []

        for tweet in data:
            dados.append([tweet["coordinates"]["coordinates"][0],
                          tweet["coordinates"]["coordinates"][1],
                          tweet["created_at"]])

    return dados


print(extract_list_geo(input_filename))
