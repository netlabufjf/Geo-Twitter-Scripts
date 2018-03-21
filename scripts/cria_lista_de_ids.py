"""
Created on Tue Feb 27 21:28:27 2018

@author: rooke
"""

import sys
import networkx as nx
import os
import pandas as pd

cidade = sys.argv[1]


def cria_lista_de_ids(cidade_param):
    graph_friends = nx.DiGraph()

    dir_base = os.path.abspath(os.getcwd())+"/.."
    graph_friends_output = "{}/data/grafos/{}.graph_user.friends.adjlist".format(
        dir_base, cidade_param)

    if os.path.exists(graph_friends_output):
        graph_friends = nx.read_adjlist(graph_friends_output, create_using=nx.DiGraph())

    graph_followers = nx.DiGraph()

    graph_followers_output = "{}/data/grafos/{}.graph_user.followers.adjlist".format(
        dir_base, cidade_param)

    if os.path.exists(graph_followers_output):
        graph_followers = nx.read_adjlist(graph_followers_output, create_using=nx.DiGraph())

    graph = nx.compose(graph_friends, graph_followers)

    pd.DataFrame(list(graph.nodes())).to_csv(
        "{}/data/grafos/{}.complete.id_users.list.csv".format(dir_base, cidade_param), header=False, index=False)

    del graph
    del graph_friends
    del graph_followers


cria_lista_de_ids(cidade)
