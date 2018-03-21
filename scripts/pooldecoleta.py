import coleta_timeline


cidade = "london"

dir_cidade = "{}/data/{}".format(dir_base, cidade)


def coleta_do_arquivo(nome_arquivo):

    arquivo = open(nome_arquivo, 'r')
    for line in arquivo.readlines():
        coleta_timeline(line)


t_followers = threading.Thread(target=collect_users_followers,args=(status.user.id, ))
            t_followers.start()

dir_cidade = "{}/data/{}".format(dir_base, cidade)
