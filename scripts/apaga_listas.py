import subprocess


def remove_line(padrao, arquivo):
    subprocess.call(
        ["sed -i '/{}/d' {}".format(padrao, arquivo)], shell=True)
