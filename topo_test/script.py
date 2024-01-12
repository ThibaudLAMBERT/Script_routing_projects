import json
import os
import configparser





#######utilisation des donnes depuuis le fichier json

with open('topo_test/network.json', 'r') as fichier:
    donnees = json.load(fichier)


    
# for element in donnees["data"]:
#     print(element['name'])
# print(donnes["data"])
print(donnees["data"][1]['name'])



filename = 'config.cfg'
with open(filename, 'w') as file:
    pass

fichier_cfg = 'config.cfg'


# if not os.path.exists(fichier_cfg):
#     with open(fichier_cfg, 'w') as fichier:
#         fichier.write("CleSansValeur1\n")
#         fichier.write("CleSansValeur2\n")


with open(fichier_cfg, 'a') as fichier:
   
    fichier.write("control-plane\n")
    fichier.write("line con 0\n")
    fichier.write(" exec-timeout 0 0\n")
    fichier.write(" privilege level 15\n")
    fichier.write(" logging synchronous\n")
    fichier.write(" stopbits 1\n")
    fichier.write("line aux 0\n")
    fichier.write(" exec-timeout 0 0\n")
    fichier.write(" privilege level 15\n")
    fichier.write(" logging synchronous\n")
    fichier.write(" stopbits 1\n")
    fichier.write("line vty 0 4\n")
    fichier.write(" login\n")
    fichier.write("!\n")
    fichier.write("!\n")
    fichier.write("end\n")

