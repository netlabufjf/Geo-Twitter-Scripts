# Importar modulo do sistema operacional
import os

# dir_base = os.path.abspath(os.getcwd())
caminho_desse_arquivo = os.path.abspath(os.path.dirname(__file__))
dir_base = caminho_desse_arquivo+"/../.."

cidades = [{"cidade": "london", "coletados": 0, "no_geotag": 0, "restritos": 0, "error": 0, "falta_coletar": 0},
           {"cidade": "nyc", "coletados": 0, "no_geotag": 0, "restritos": 0, "error": 0, "falta_coletar": 0},
           {"cidade": "saopaulo", "coletados": 0, "no_geotag": 0, "restritos": 0, "error": 0, "falta_coletar": 0},
           {"cidade": "tokyo", "coletados": 0, "no_geotag": 0, "restritos": 0, "error": 0, "falta_coletar": 0}]


for i, cidade in enumerate(cidades):

    # quantidade de coletados
    cmd = "ls {}/data/{}/user_timeline | wc -l".format(dir_base, cidade["cidade"])
    cidades[i]["coletados"] = int(os.popen(cmd).readline().rstrip())

    # quantidade de no_geotag
    cmd = "wc -l {}/data/{}/nogeotagged.id_users.list.csv | cut -d' ' -f1".format(dir_base, cidade["cidade"])
    cidades[i]["no_geotag"] = int(os.popen(cmd).readline().rstrip())

    # quantidade de processados_erro
    cmd = "wc -l {}/data/{}/processados_erro.id_users.list.csv | cut -d' ' -f1".format(dir_base, cidade["cidade"])
    cidades[i]["error"] = int(os.popen(cmd).readline().rstrip())

    # quantidade de restrict
    cmd = "wc -l {}/data/{}/restrict.id_users.list.csv | cut -d' ' -f1".format(dir_base, cidade["cidade"])
    cidades[i]["restritos"] = int(os.popen(cmd).readline().rstrip())

    # quantidade q falta para coletar
    falta_coletar = 0
    for x in range(0, 15):
        if os.path.isfile("{}/data/{}/{}.id_users.list.csv".format(dir_base, cidade["cidade"], x)):
                cmd = "wc -l {}/data/{}/{}.id_users.list.csv | cut -d' ' -f1".format(dir_base, cidade["cidade"], x)
                falta_coletar = falta_coletar + int(os.popen(cmd).readline().rstrip())

    cidades[i]["falta_coletar"] = falta_coletar

print cidades
