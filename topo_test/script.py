import json
import os
import configparser

#TODO 
#negotiation auto ????
#duplex full ??????


#######utilisation des donnes depuuis le fichier json
with open('topo_test/network.json', 'r') as fichier:
    donnees = json.load(fichier)
# print(donnees["data"][1]['name'])
# for element in donnees["data"]:
#     print(element['name'])
# print(len(donnees["data"]))
print(donnees["data"][0]["protocol"][:1])
#######supprimer le fichier cfg
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
            








def creation_fichier_config(filename, donnees):
    nomrouteur = nom_routeur(filename)
    supprimer_all_lines(filename)
    
    for i in range (len(donnees["data"])):
        if donnees["data"][i]['name'] == nomrouteur:
            numero_json=i

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


        fichier.write("interface Loopback0\n")
        fichier.write(" no ip address\n")
        fichier.write(" ipv6 address ")
        fichier.write(donnees["data"][numero_json]['loopback'])
        fichier.write("\n")
        fichier.write(" ipv6 enable\n")
        if donnees["data"][numero_json]['protocol']== "RIP":
            fichier.write(" ipv6 rip AS")
            fichier.write(donnees["data"][numero_json]['as'])
            fichier.write(" enable\n")

        if donnees["data"][numero_json]['protocol']== "OSPF":
            fichier.write(" ipv6 ospf ")
            fichier.write(donnees["data"][numero_json]['as'])
            fichier.write(" area 0\n")
        for i in range (len(donnees["data"][numero_json]['interfaces'])):
            fichier.write("interface ")
            fichier.write(donnees["data"][numero_json]['interfaces'][i]["name"])
            fichier.write("\n")
            fichier.write(" negotiation auto\n")
            fichier.write(" ipv6 address ")
            fichier.write(donnees["data"][numero_json]['interfaces'][i]["ip"]) 
            fichier.write("\n")
            fichier.write(" ipv6 enable\n")
            fichier.write(" no ip address\n")

            if donnees["data"][numero_json]['protocol']== "RIP":
                fichier.write(" ipv6 rip AS")
                fichier.write(donnees["data"][numero_json]['as'])
                fichier.write(" enable\n")

            if donnees["data"][numero_json]['protocol']== "OSPF":
                fichier.write(" ipv6 ospf ")
                fichier.write(donnees["data"][numero_json]['as'])
                fichier.write(" area 0\n")

        fichier.write("router bgp ")
        fichier.write(donnees["data"][numero_json]['as'])
        fichier.write("\n")
        fichier.write(" bgp router-id ")
        fichier.write(donnees["data"][numero_json]['id'])
        fichier.write("\n")
        fichier.write(" bgp log-neighbor-changes\n")
        fichier.write(" no bgp default ipv4-unicast\n")

        for element in donnees["data"][numero_json]["interfaces"]:
            if (element['neighbor'][1:2]) == donnees["data"][numero_json]["protocol"][:1]:
                fichier.write(" neighbor ")
                for truc in (donnees["data"]):
                    if truc['name'] == element['neighbor']:
                        fichier.write(truc["loopback"].split('/')[0])
                        fichier.write(" remote-as ")
                        fichier.write(truc["as"])
                        fichier.write("\n neighbor ")
                        fichier.write(truc["loopback"].split('/')[0])
                        fichier.write(" update-source Loopback0 ")
                        fichier.write("\n")
            else:
                print("test")
                fichier.write(" neighbor ")
                for truc in (donnees["data"]):
                    
                    if truc['name'] == element['neighbor']:
                        
                        for i in range (len(truc["interfaces"])):
                            print(element["neighbor"])
                            print (truc["interfaces"][i]["neighbor"])
                            if nomrouteur == truc["interfaces"][i]["neighbor"]:
                                print("testtt")
                                fichier.write(truc["interfaces"][i]["ip"].split('/')[0])



                        
                        fichier.write(" remote-as ")
                        fichier.write(truc["as"])
                        fichier.write("\n")
        fichier.write(" address-family ipv4\n")
        fichier.write(" exit-address-family\n")
        fichier.write(" address-family ipv6\n")


        for element in donnees["data"][numero_json]["interfaces"]:
            if (element['neighbor'][1:2]) == donnees["data"][numero_json]["protocol"][:1]:
                fichier.write("  neighbor ")
                for truc in (donnees["data"]):
                    if truc['name'] == element['neighbor']:
                        fichier.write(truc["loopback"].split('/')[0])
                        fichier.write(" activate\n")
                     

                        
            else:
                print("test")
                fichier.write("  neighbor ")
                for truc in (donnees["data"]):
                    
                    if truc['name'] == element['neighbor']:
                        
                        for i in range (len(truc["interfaces"])):
                            print(element["neighbor"])
                            print (truc["interfaces"][i]["neighbor"])
                            if nomrouteur == truc["interfaces"][i]["neighbor"]:
                                print("testtt")
                                fichier.write(truc["interfaces"][i]["ip"].split('/')[0])
                                fichier.write(" activate\n")
        fichier.write(" exit-address-family\n")                    
        fichier.write("ip forward-protocol nd\n")
        fichier.write("no ip http server\n")
        fichier.write("no ip http secure-server\n")
        if donnees["data"][numero_json]['protocol']== "RIP":
            fichier.write("ipv6 router rip AS")
            fichier.write(donnees["data"][numero_json]['as'])
            fichier.write("\n")
            fichier.write(" redistribute connected\n")

        if donnees["data"][numero_json]['protocol']== "OSPF":
            fichier.write("ipv6 router ospf ")
            fichier.write(donnees["data"][numero_json]['as'])
            fichier.write("\n")
            fichier.write(" router-id ")
            fichier.write(donnees["data"][numero_json]['id'])
            fichier.write("\n")
            for element in donnees["data"][numero_json]["interfaces"]:
                if (element['neighbor'][1:2]) == "R":
                    fichier.write(" passive-interface ")
                    fichier.write(element['name'])
                    fichier.write("\n")
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


fichier_cfg = 'tester.cfg'
creation_fichier_config(fichier_cfg, donnees)



    



##########bouts de codes peut etre utiles plus tard

# if not os.path.exists(fichier_cfg):
#     with open(fichier_cfg, 'w') as fichier:
#         fichier.write("CleSansValeur1\n")
#         fichier.write("CleSansValeur2\n")
    



