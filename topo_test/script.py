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




# if not os.path.exists(fichier_cfg):
#     with open(fichier_cfg, 'w') as fichier:
#         fichier.write("CleSansValeur1\n")
#         fichier.write("CleSansValeur2\n")

###############debut ecriture



fichier_cfg = 'config.cfg'
with open(fichier_cfg, 'a') as fichier:
 

    fichier.write("version 15.2\n")
    fichier.write("service timestamps debug datetime msec\n")
    fichier.write("service timestamps log datetime msec\n")
    fichier.write("hostname RR1\n")
    fichier.write("boot-start-marker\n")
    fichier.write("boot-end-marker\n")
    fichier.write("no aaa new-model\n")
    fichier.write("no ip icmp rate-limit unreachable\n")
    fichier.write("ip cef\n")
    fichier.write("no ip domain lookup\n")
    fichier.write("ipv6 unicast-routing\n")
    fichier.write("ipv6 cef\n")
    fichier.write("multilink bundle-name authenticated\n")
    fichier.write("ip tcp synwait-time 5\n")








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

