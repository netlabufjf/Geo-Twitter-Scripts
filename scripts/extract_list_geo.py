import gzip
import json
import sys


def extract_list_geo(input_filename):
    #  Extrai o formato link_data:
    with gzip.open(input_filename, "rb") as input_file:
        json_bytes = input_file.read()

        if sys.version_info[0] < 3:
            json_str = json_bytes
        else:
            json_str = json_bytes.decode('utf-8')

        data = json.loads(json_str)

        dados = []

        for tweet in data:
            dados.append([tweet["coordinates"]["coordinates"][0],
                          tweet["coordinates"]["coordinates"][1],
                          tweet["created_at"]])

    return dados
