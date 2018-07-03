import gzip
import json
import networkx as nx
from networkx.readwrite import json_graph
import os
import sys

cidade_param = sys.argv[1]
# cidade_param = "saopaulo"

caminho_desse_arquivo = os.path.abspath(os.path.dirname(__file__))
dir_base = caminho_desse_arquivo+"/../.."

# dir_base = "/home/rooke/Projetos/Geo-Twitter-Scripts/scripts/analises/../.."

print(dir_base)

# Ideias
# Pega todos os ids de usuarios do grafo e subtrai deles todos os usuarios coletados
# Desse modo teremos ao final todos os ids de usuarios que nao servem para a analise
# Pega a estrutura do grafo e remove todos os nos que nao servem


# Pega todos os ids do grafo
arq_lista_completa = open(
    '{}/data/grafos/{}.complete.id_users.list.csv'.format(dir_base, cidade_param), 'r')

lista_completa = []
for i, line in enumerate(arq_lista_completa.readlines()):
    lista_completa.append(line.rstrip())
arq_lista_completa.close()

# gera lista de ids coletados
# cd user_timeline
# ls -1 | ls -1 | sed -e 's/\.json.gz$//' > ../coletados.id_users.list.csv

# Pega todos os ids dos coletados
arq_lista_coleta = open(
    '{}/data/{}/coletados.id_users.list.csv'.format(dir_base, cidade_param), 'r')

lista_coleta = []
for i, line in enumerate(arq_lista_coleta.readlines()):
    lista_coleta.append(line.rstrip())
arq_lista_coleta.close()

# Pega todos os ids que nao serviram para a coleta
diferenca = list(set(lista_completa) - set(lista_coleta))

# Pega o grafo com todo mundo, para isso...
# Pega o grafo de amigos
graph_friends = nx.DiGraph()

graph_friends_output = "{}/data/grafos/{}.graph_user.friends.adjlist".format(dir_base, cidade_param)

if os.path.exists(graph_friends_output):
    graph_friends = nx.read_adjlist(graph_friends_output, create_using=nx.DiGraph())

# Pega o grafo de seguidores
graph_followers = nx.DiGraph()

graph_followers_output = "{}/data/grafos/{}.graph_user.followers.adjlist".format(
    dir_base, cidade_param)

if os.path.exists(graph_followers_output):
    graph_followers = nx.read_adjlist(graph_followers_output, create_using=nx.DiGraph())

# Junta o grafo de amigos e de seguidores
graph_complete = nx.compose(graph_friends, graph_followers)

del graph_followers
del graph_friends

# Percorre todos que nao servem removendo do grafo
for id in diferenca:
    if graph_complete.has_node(id):
        graph_complete.remove_node(id)
    else:
        print("Grafo nao tem o no: "+id)


# Grava grafo processado
# https://networkx.github.io/documentation/stable/reference/readwrite/generated/
# networkx.readwrite.json_graph.node_link_data.html#networkx.readwrite.json_graph.node_link_data

link_data_format = json_graph.node_link_data(graph_complete)

output_filename = '{}/data/{}/graph_complete.node_link_data.json.gz'.format(dir_base, cidade_param)

# Grava o formato link_data:
with gzip.open(output_filename, "w") as outfile:
    try:
        # se python 2.7
        if sys.version_info[0] < 3:
            dump = str(json.dumps(link_data_format))
        else:
            dump = bytes(json.dumps(link_data_format), "UTF-8")
        outfile.write(dump)
    except Exception:
        print("Erro ao gerar bytes para escrita no json cidade: {}".format(cidade_param))
