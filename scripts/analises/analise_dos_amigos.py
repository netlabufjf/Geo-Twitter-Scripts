import gzip
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import numpy as np
import os
import pandas as pd
import sys

# pega a cidade que sera gerado os graficos
# cidade_param = sys.argv[1]

cidade_param = "london"

caminho_desse_arquivo = os.path.abspath(os.path.dirname(__file__))
dir_base = caminho_desse_arquivo+"/../.."

output_filename = '{}/data/{}/graph_complete.node_link_data.json.gz'.format(dir_base, cidade_param)

grafo = None

#  Grava o formato link_data:
with gzip.open(output_filename, "rb") as input_file:
    json_bytes = input_file.read()

    if sys.version_info[0] < 3:
        json_str = json_bytes
    else:
        json_str = json_bytes.decode('utf-8')

    data = json.loads(json_str)

    grafo = json_graph.node_link_graph(data)

list_degree_in_out = []

print("passou")


if grafo is not None:
    i = 0
    for no in grafo:
        print "no:"+no
        print grafo.edges(no)
        quem_ele_segue = grafo.edges(no)
        for seguido in quem_ele_segue:
            print seguido
        i = i + 1
        if i > 10:
            break
