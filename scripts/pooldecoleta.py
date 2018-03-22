import coleta_timeline


cidade = "london"

dir_cidade = "{}/data/{}".format(dir_base, cidade)


def coleta_do_arquivo(nome_arquivo, cidade):

    arquivo = open(nome_arquivo, 'r')
    for line in arquivo.readlines():
        coleta_timeline(line, cidade)


arquivo.close()
