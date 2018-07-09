from extract_list_geo import extract_list_geo
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
cidade_param = sys.argv[1]

# cidade_param = "london"

caminho_desse_arquivo = os.path.abspath(os.path.dirname(__file__))
dir_base = caminho_desse_arquivo+"/../.."

output_filename = '{}/data/{}/graph_complete.node_link_data.json.gz'.format(dir_base, cidade_param)

grafo = None


def add_lista(nome_lista, id_user, cidade):

    caminho_desse_arquivo = os.path.abspath(os.path.dirname(__file__))
    dir_base = caminho_desse_arquivo+"/../.."

    dir_cidade = "{}/data/{}".format(dir_base, cidade)

    if not os.path.exists(dir_cidade):
        os.makedirs(dir_cidade)

    arquivo = open("{}/{}.id_users.list.csv".format(dir_cidade, nome_lista), "a")
    arquivo.write(str(id_user)+"\n")
    arquivo.close()


#  Grava o formato link_data:
with gzip.open(output_filename, "rb") as input_file:
    json_bytes = input_file.read()

    if sys.version_info[0] < 3:
        json_str = json_bytes
    else:
        json_str = json_bytes.decode('utf-8')

    data = json.loads(json_str)

    grafo = json_graph.node_link_graph(data)

# df = pd.DataFrame()
lista_count_tweets = []

for no in grafo:
    arquivo_no = '{}/data/{}/user_timeline/{}.json.gz'.format(dir_base, cidade_param, no)

    try:
        lista_count_tweets.append(len(extract_list_geo(arquivo_no)))
    except Exception:
        add_lista("count_tweets_error", no, cidade_param)

    # df = df.append({'lat': dados_do_no[0],
    #                'lon': dados_do_no[1],
    #                'date': dados_do_no[2]}, ignore_index=True)


# Plot CDF

df = pd.DataFrame.from_dict({'num_tweets': lista_count_tweets})

x = df.sort_values(by='num_tweets')['num_tweets'].values

###################################
#    Receita de Bolo para ECDFs  ##
#    CookBook from ECDFs         ##
###################################

# Dont touch in Y
# Nao mexa no Y
y = np.arange(1.0, len(x)+1) / len(x)

# Configurando a saida em imagem
# fig = plt.figure()

# Ingrediente 2 - Customize suas linhas
# Ingredient 2 - Custom your lines
plt.plot(x, y, marker='.', linestyle='none')

# Ingredient 3 - Define your label axis
# Ingrediente 3 - Defina os rotulos dos eixos
plt.xlabel("Numero de Tweets")
plt.ylabel("ECDF")
plt.margins(0.02)

# Ingredient 5 - Define your pattern from x(or y) axis
# Ingrediente 5 - Defina o padrao dos numeros eixo x(ou y)


def major_formatter(a, pos):
    return "%.f" % (a)


ax = plt.axes()

# Ingredient 6 - Define how many elements show in y axis
# Ingrediente 6 - Defina Quantos elementos aparecerao no eixo y
ax.yaxis.set_major_locator(plt.MaxNLocator(9))

# Ingredient 7 - Define how many elements show in x axis
# Ingrediente 7 - Defina Quantos elementos aparecerao no eixo x
ax.xaxis.set_major_locator(plt.MaxNLocator(11))

# Ingredient 8 - Add the Ingredient 5 in x axis
# Ingrediente 8 - Adiciona o Ingrediente 5 no eixo x
ax.xaxis.set_major_formatter(plt.FuncFormatter(major_formatter))

# Plot
plt.legend()

fig = ax.get_figure()

arquivo_saida = '{}/data/{}/CDF_num_tweets.png'.format(dir_base, cidade_param)

fig.savefig(arquivo_saida)
