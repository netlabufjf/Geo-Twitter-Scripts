import gzip
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from networkx.readwrite import json_graph
import numpy as np
import os
import pandas as pd
import sys

# pega a cidade que sera gerado os graficos
cidade_param = sys.argv[1]
in_out = sys.argv[2]

# cidade_param = "london"

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
    for no in grafo:
        if in_out == "in":
            list_degree_in_out.append(grafo.in_degree(no))
        else:
            list_degree_in_out.append(grafo.out_degree(no))

    # Plot CDF

    df = pd.DataFrame.from_dict({'degree': list_degree_in_out})

    x = df.sort_values(by='degree')['degree'].values

    ###################################
    #   Receita de Bolo para ECDFs   ##
    #   CookBook from ECDFs          ##
    ###################################

    # Dont touch in Y
    # Nao mexa no Y
    y = np.arange(1.0, len(x)+1) / len(x)

    # Ingrediente 2 - Customize suas linhas
    # Ingredient 2 - Custom your lines
    plt.plot(x, y, marker='.', linestyle='none')

    # Ingredient 3 - Define your label axis
    # Ingrediente 3 - Defina os rotulos dos eixos
    plt.xlabel("Duracao em Horas")
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

    plt.legend()

    ####################################################
    #   Receita para dar um Zoom no recheio do Bolo   ##
    #   Recipe to make zoom inside the cake           ##
    ####################################################

    # Ingredient 1 - Select the range from zoom in x
    # Ingrediente 1 - Seleciona o intervalo do zoom no x
    x1 = 0.0
    x2 = 500

    # Ingredient 2 - Select the range from zoom in y
    # Ingrediente 2 - Seleciona o intervalo do zoom no y
    y1 = 0.98
    y2 = 1

    # Ingredient 3 - Define zoom (parameter 2) and define the location (loc):
    # Ingrediente 3 - Defina o tamanho do zoom na plotagem (parametro 2) e defina a localizacao do zoom (loc):
    # loc
    axins = zoomed_inset_axes(ax, 10, loc=4)

    # Ingrediente 4 - Add the Ingredient 4 from cookbook
    # Ingrediente 4 - Adicione o Ingrediente 4 da Receita de Bolo
    axins.plot(x, y, marker='.', linestyle='none')

    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)

    # Ingredient 5 - Define how many elements show in x axis from zoom
    # Ingrediente 5 - Defina Quantos elementos aparecerao no eixo x do zoom
    axins.xaxis.set_major_locator(plt.MaxNLocator(4))

    # Ingredient 6 - Define how many elements show in y axis from zoom
    # Ingrediente 6 - Defina Quantos elementos aparecerao no eixo y do zoom
    axins.yaxis.set_major_locator(plt.MaxNLocator(5))

    axins.xaxis.set_major_formatter(plt.FuncFormatter(major_formatter))

    # plt.yticks(visible=False)

    # Ingredient 7 - Define the location 1 and 2 from zoom lines
    # Ingrediente 7 - Defina a localizacao 1 e 2 das linhas do zoom
    mark_inset(ax, axins, loc1=1, loc2=2, fc="none", ec="0.8")
    plt.draw()

    fig = ax.get_figure()

    arquivo_saida = '{}/data/{}/CDF_out_degree_zoom.png'.format(dir_base, cidade_param)
    if in_out == "in":
        arquivo_saida = '{}/data/{}/CDF_in_degree_zoom.png'.format(dir_base, cidade_param)

    fig.savefig(arquivo_saida)
