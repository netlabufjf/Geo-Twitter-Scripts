import os


def add_lista_perfil_restrito(id_user, cidade):

    dir_base = os.path.abspath(os.getcwd())+""

    dir_cidade = "{}/data/{}".format(dir_base, cidade)

    if not os.path.exists(dir_cidade):
        os.makedirs(dir_cidade)

    print(dir_cidade)

    arquivo = open("{}/restrict.id_users.list.csv".format(dir_cidade), "a")
    arquivo.write(str(id_user)+"\n")
    arquivo.close()
