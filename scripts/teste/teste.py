

import os

dir_base = os.path.abspath(os.getcwd())+""

dir_cidade = "{}/data/{}".format(dir_base, "london")


import glob
for file in glob.glob("{}/[0-9]*.id_users.list.csv".format(dir_cidade)):
    print file
