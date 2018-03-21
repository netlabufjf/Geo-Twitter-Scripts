"""
Created on Tue Feb 27 21:28:27 2018

@author: rooke
"""
import pandas as pd
import sys
import networkx as nx
import os

cidade = sys.argv[1]

"""
def cria_lista_de_ids(cidade_param):
    graph_friends = nx.DiGraph()

    dir_base = os.path.abspath(os.getcwd())+"/.."
    graph_friends_output = "{}/data/grafos/{}.graph_user.friends.adjlist".format(
        dir_base, cidade_param)

    if os.path.exists(graph_friends_output):
        graph_friends = nx.read_adjlist(graph_friends_output, create_using=nx.DiGraph())

    pd.DataFrame([graph_friends.nodes()]).sort_values(0).to_csv(
        "{}/data/grafos/{}.friends.id_users.list.csv".format(dir_base, cidade_param), header=False, index=False)

    del graph_friends

    graph_followers = nx.DiGraph()

    graph_followers_output = "{}/data/grafos/{}.graph_user.followers.adjlist".format(
        dir_base, cidade_param)

    if os.path.exists(graph_followers_output):
        graph_followers = nx.read_adjlist(graph_followers_output, create_using=nx.DiGraph())

    pd.DataFrame([graph_followers.nodes()]).sort_values(0).to_csv(
        "{}/data/grafos/{}.followers.id_users.list.csv".format(dir_base, cidade_param), header=False, index=False)

    del graph_followers

    arq_followers = open(
        '{}/data/grafos/{}.complete.id_users.list.csv'.format(dir_base, cidade_param), 'r')
"""


def cria_lista_de_ids(cidade_param):
    graph_friends = nx.DiGraph()

    dir_base = os.path.abspath(os.getcwd())+"/.."
    graph_friends_output = "{}/data/grafos/{}.graph_user.friends.adjlist".format(
        dir_base, cidade_param)

    if os.path.exists(graph_friends_output):
        graph_friends = nx.read_adjlist(graph_friends_output, create_using=nx.DiGraph())

    list_friends = list(graph_friends.nodes())

    del graph_friends

    graph_followers = nx.DiGraph()

    graph_followers_output = "{}/data/grafos/{}.graph_user.followers.adjlist".format(
        dir_base, cidade_param)

    if os.path.exists(graph_followers_output):
        graph_followers = nx.read_adjlist(graph_followers_output, create_using=nx.DiGraph())

    list_followers = list(graph_followers.nodes())

    del graph_followers

    list_friends.extend(list_followers)

    del list_followers

    lista_completa = list(set(list_friends))

    del list_friends

    pd.DataFrame(lista_completa).to_csv(
        "{}/data/grafos/{}.complete.id_users.list.csv".format(dir_base, cidade_param), header=False, index=False)


cria_lista_de_ids(cidade)
