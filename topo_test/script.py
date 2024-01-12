import json
import pandas as pd
import os
import configparser





#######utilisation des donnes depuuis le fichier json

with open('Script2/network.json', 'r') as fichier:
    donnees = json.load(fichier)


    
# for element in donnees["data"]:
#     print(element['name'])
# print(donnes["data"])
print(donnees["data"][1]['name'])



fichier_cfg = 'config.cfg'


# if not os.path.exists(fichier_cfg):
#     with open(fichier_cfg, 'w') as fichier:
#         fichier.write("CleSansValeur1\n")
#         fichier.write("CleSansValeur2\n")


with open(fichier_cfg, 'a') as fichier:
    fichier.write("NouvelleCle1\n")
    fichier.write("NouvelleCle2\n")

