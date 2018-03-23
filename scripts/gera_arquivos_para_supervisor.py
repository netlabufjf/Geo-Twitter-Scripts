import glob
import os
# import sys
# parametro 1 - caminho para o /etc/supervisor/conf.d
# caminho = sys.argv[1]
caminho = "/etc/supervisor/conf.d"

cidades = ["london", "saopaulo", "tokyo", "nyc"]

contador_chave = 0

dir_base = os.path.abspath(os.path.dirname(__file__))

for cidade in cidades:
    dir_cidade = "{}/data/{}".format(dir_base+"/..", cidade)
    if os.path.exists(dir_cidade):
        for file in glob.glob("{}/[0-9]*.id_users.list.csv".format(dir_cidade)):
            print file
            print os.path.basename(file)
            print '{}/{}.{}'.format(caminho, cidade, os.path.basename(file).replace("csv", "conf"), contador_chave)
            contador_chave += 1
            arq_principal = open('{}/{}.{}'.format(caminho, cidade, os.path.basename(file).replace("csv", "conf")), 'a')
            arq_principal.write("[program:{}.{}]\n".format(cidade, os.path.basename(file).replace("csv", "")))
            arq_principal.write("command=python {}/coleta_timeline_uma_chave_por_thread.py {} {} {}\n".format(dir_base,
                                cidade, file, contador_chave))
            arq_principal.write("autostart=true\n")
            arq_principal.write("autorestart=true\n")
            arq_principal.write("stderr_logfile=/hd/novacoleta/Geo-Twitter-Scripts/logs/coleta.err.log\n")
            arq_principal.write("stdout_logfile=/hd/novacoleta/Geo-Twitter-Scripts/logs/coleta.out.log\n")
            arq_principal.close()
