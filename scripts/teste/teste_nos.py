import pandas as pd
import sys
import networkx as nx
import os

G = nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
G.add_path([0, 1, 1, 2])
a = list(G.nodes())
print a

H = nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
H.add_path([0, 1, 1, 2, 3])
b = list(H.nodes())
print b


a.extend(b)

a

sorted(set(a))

dir_base = os.path.abspath(os.getcwd())+""
pd.DataFrame(list(set(a))).to_csv(
    "{}/data/grafos/{}.friends.id_users.list.csv".format(dir_base, "teste"), header=False, index=False)


def func2(x):
    x = [20]


def func():
    x = [10]
    func2(x)
    print x


func()
