"""
    Sao passados 2 parametros para esse arquivo
    o primeiro e a cidade e o segundo e a quantidade pela qual se quer dividir o arquivo
"""

import os
import sys

cidade = sys.argv[1]
qtd = int(sys.argv[2])


def divide_arquivo(cidade_param, quantidade):

    dir_base = os.path.abspath(os.getcwd())+"/.."

    dir_cidade = "{}/data/{}".format(dir_base, cidade_param)

    if not os.path.exists(dir_cidade):
        os.makedirs(dir_cidade)

    contador = 0

    arquivos = []

    for i in range(0, quantidade):
        arquivos.append(open("{}/{}.id_users.list.csv".format(dir_cidade, i), "a"))

    arq_principal = open(
        '{}/data/grafos/{}.complete.id_users.list.csv'.format(dir_base, cidade_param), 'r')

    for line in arq_principal.readlines():
        # o valor de contador roda entre 0, 1, 2 ... quantidade
        contador = contador % quantidade
        arquivos[contador].write(line)
        contador += 1

    arq_principal.close()

    for i in range(0, quantidade):
        arquivos[i].close()


divide_arquivo(cidade, qtd)
