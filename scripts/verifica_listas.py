import os


def in_lista_perfil_restrito(id_user, cidade):

    dir_base = os.path.abspath(os.path.dirname(__file__))+"/.."

    dir_cidade = "{}/data/{}".format(dir_base, cidade)

    if not os.path.exists(dir_cidade):
        os.makedirs(dir_cidade)

    existe = False

    try:
        arquivo = open("{}/restrict.id_users.list.csv".format(dir_cidade), "r")
        for line in arquivo.readlines():
            if line.rstrip() == id_user:
                existe = True
                break
        arquivo.close()
    except IOError:
        pass

    return existe


def in_lista_nogeotagged(id_user, cidade):

    dir_base = os.path.abspath(os.path.dirname(__file__))+"/.."

    dir_cidade = "{}/data/{}".format(dir_base, cidade)

    if not os.path.exists(dir_cidade):
        os.makedirs(dir_cidade)

    existe = False

    try:
        arquivo = open("{}/nogeotagged.id_users.list.csv".format(dir_cidade), "r")
        for line in arquivo.readlines():
            if line.rstrip() == id_user:
                existe = True
                break
        arquivo.close()
    except IOError:
        pass

    return existe
