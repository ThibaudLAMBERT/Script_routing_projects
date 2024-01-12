import json
import os
import configparser





#######utilisation des donnes depuuis le fichier json

with open('topo_test/network.json', 'r') as fichier:
    donnees = json.load(fichier)
#print(donnees["data"][1]['name'])


#######"supprimer le fichier cfg"


def supprimer_all_lines(filename):

    with open(filename, 'w') as file:
        pass




#########recupere nom
#quand les fichiers conf sont vides, ils n'ont que le nom du routeur
#ce programme return le nom du routeur avec le fichier config vide

def nom_routeur(nom_fichier):

    with open(nom_fichier, 'r') as file:
        for numero_ligne, ligne in enumerate(file, start=1):
            if 'hostname' in ligne:
                return(ligne.strip()[9:])
            

###############debut ecriture



fichier_cfg = 'tester.cfg'


def creation_fichier_config(filename):
    nomrouteur = nom_routeur(filename)
    supprimer_all_lines(filename)
    with open(fichier_cfg, 'a') as fichier:
    

        fichier.write("version 15.2\n")
        fichier.write("service timestamps debug datetime msec\n")
        fichier.write("service timestamps log datetime msec\n")
        fichier.write("hostname ")
        fichier.write(nomrouteur)
        fichier.write("\n")
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

##############milieu ecriture

creation_fichier_config(fichier_cfg)


############fin ecriture

# with open(fichier_cfg, 'a') as fichier:
   
#     fichier.write("control-plane\n")
#     fichier.write("line con 0\n")
#     fichier.write(" exec-timeout 0 0\n")
#     fichier.write(" privilege level 15\n")
#     fichier.write(" logging synchronous\n")
#     fichier.write(" stopbits 1\n")
#     fichier.write("line aux 0\n")
#     fichier.write(" exec-timeout 0 0\n")
#     fichier.write(" privilege level 15\n")
#     fichier.write(" logging synchronous\n")
#     fichier.write(" stopbits 1\n")
#     fichier.write("line vty 0 4\n")
#     fichier.write(" login\n")
#     fichier.write("!\n")
#     fichier.write("!\n")
#     fichier.write("end\n")



##########bouts de codes peut etre utiles plus tard

# if not os.path.exists(fichier_cfg):
#     with open(fichier_cfg, 'w') as fichier:
#         fichier.write("CleSansValeur1\n")
#         fichier.write("CleSansValeur2\n")
    



# for element in donnees["data"]:
#     print(element['name'])
# print(donnes["data"])