import gzip
import json
import matplotlib.pyplot as plt
import networkx as nx
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


# Plot CDF

df = pd.DataFrame(np.random.randint(0, 100, size=(100, 1)), columns=['degree'])

x = df.sort_values(by='degree')['degree'].values

###################################
#    Receita de Bolo para ECDFs  ##
#    CookBook from ECDFs         ##
###################################

# Dont touch in Y
# Nao mexa no Y
y = np.arange(1.0, len(x)+1) / len(x)

# Configurando a saida em imagem
fig = plt.figure()

# Ingrediente 2 - Customize suas linhas
# Ingredient 2 - Custom your lines
plt.plot(x, y, marker='.', linestyle='none')

# Ingredient 3 - Define your label axis
# Ingrediente 3 - Defina os rotulos dos eixos
plt.xlabel("Gral de Saida")
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

fig.savefig('/home/rooke/Projetos/mestrado/Geo-Twitter-Scripts/scripts/teste/CDF_out_degree.png')
