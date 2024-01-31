import json
import os

import glob

#TODO 
#negotiation auto ????
#duplex full ??????


#######utilisation des donnes depuuis le fichier json
with open('Topology/Small/network.json', 'r') as fichier:
    donnees = json.load(fichier)

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
            


def as_routeur(neighbor):
      for i in range (len(donnees["data"])):
        if donnees["data"][i]['name'] == neighbor:
            return donnees["data"][i]['as']
           




def creation_fichier_config(filename, donnees,numero_json):
    print("start modif for :", filename)
    nomrouteur = nom_routeur(filename)
    
    supprimer_all_lines(filename)
    
    #for i in range (len(donnees["data"])):
        #if donnees["data"][i]['name'] == nomrouteur:
            #numero_json=i

    with open(filename, 'a') as fichier:
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
            if len(donnees["data"][numero_json]['as']) < 3 :
                fichier.write(donnees["data"][numero_json]['as'])
            else :
                fichier.write(donnees["data"][numero_json]['as'][:4])
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

            if donnees["data"][numero_json]['protocol']== "OSPF" and donnees["data"][numero_json]["interfaces"][i]['neighbor'] != 'NETWORK':
                fichier.write(" ipv6 ospf ")
                if len(donnees["data"][numero_json]['as']) < 3 :
                    fichier.write(donnees["data"][numero_json]['as'])
                else :
                    fichier.write(donnees["data"][numero_json]['as'][:4])
                fichier.write(" area 0\n")

        fichier.write("router bgp ")
        fichier.write(donnees["data"][numero_json]['as'])
        fichier.write("\n")
        fichier.write(" bgp router-id ")
        fichier.write(donnees["data"][numero_json]['id'])
        fichier.write("\n")
        fichier.write(" bgp log-neighbor-changes\n")
        fichier.write(" no bgp default ipv4-unicast\n")

        for routeur_data in donnees["data"]:
            if routeur_data["as"]==donnees["data"][numero_json]["as"] and donnees["data"][numero_json]["name"] != routeur_data["name"]:
                fichier.write(" neighbor ")
                fichier.write(routeur_data["loopback"].split('/')[0])
                fichier.write(" remote-as ")
                fichier.write(routeur_data["as"])
                fichier.write("\n neighbor ")
                fichier.write(routeur_data["loopback"].split('/')[0])
                fichier.write(" update-source Loopback0 ")
                fichier.write("\n")
            else:
                for voisins_data in donnees["data"][numero_json]["interfaces"]:
                    if routeur_data['name'] == voisins_data['neighbor']:
                        for i in range (len(routeur_data["interfaces"])):
                            if nomrouteur == routeur_data["interfaces"][i]["neighbor"]:
                                fichier.write(" neighbor ")
                                fichier.write(routeur_data["interfaces"][i]["ip"].split('/')[0])
                        fichier.write(" remote-as ")
                        fichier.write(routeur_data["as"])
                        fichier.write("\n")
                        
        fichier.write(" address-family ipv4\n")
        fichier.write(" exit-address-family\n")
        fichier.write(" address-family ipv6\n")

        
        for routeur_data in donnees["data"]:
            if routeur_data["as"]==donnees["data"][numero_json]["as"] and donnees["data"][numero_json]["name"] != routeur_data["name"]:
                fichier.write("  neighbor ")
                fichier.write(routeur_data["loopback"].split('/')[0])
                fichier.write(" activate\n")
            else:
                for voisins_data in donnees["data"][numero_json]["interfaces"]:
                    if routeur_data['name'] == voisins_data['neighbor']:
                        fichier.write("  neighbor ")
                        for i in range (len(routeur_data["interfaces"])):
                            if nomrouteur == routeur_data["interfaces"][i]["neighbor"]:
                                fichier.write(routeur_data["interfaces"][i]["ip"].split('/')[0])
                                fichier.write(" activate\n")

        # Verification network

        for possible_network in donnees["data"][numero_json]["interfaces"]:
            if possible_network['neighbor'] == 'NETWORK' :
                fichier.write("  network ")
                fichier.write(possible_network["ip"][:possible_network["ip"].rfind(':') + 1])
                fichier.write(possible_network["ip"][possible_network["ip"].rfind(':') + 2:])
                fichier.write("\n")

        for possible_local_pref in donnees["data"][numero_json]["interfaces"]:
            if possible_local_pref['local_pref'] != "None":
                fichier.write("  bgp default local-preference ")
                fichier.write(possible_local_pref['local_pref'])
                fichier.write("\n")
        
        
        fichier.write(" exit-address-family\n")                    
        fichier.write("ip forward-protocol nd\n")
        fichier.write("no ip http server\n")
        fichier.write("no ip http secure-server\n")
        if donnees["data"][numero_json]['protocol']== "RIP":
            fichier.write("ipv6 router rip AS")
            fichier.write(donnees["data"][numero_json]['as'])
            fichier.write("\n")
          # fichier.write(" redistribute connected\n")

        if donnees["data"][numero_json]['protocol']== "OSPF":
            fichier.write("ipv6 router ospf ")
            if len(donnees["data"][numero_json]['as']) < 3 :
                fichier.write(donnees["data"][numero_json]['as'])
            else :
                fichier.write(donnees["data"][numero_json]['as'][:4])
            fichier.write("\n")
            fichier.write(" router-id ")
            fichier.write(donnees["data"][numero_json]['id'])
            fichier.write("\n")
            #fichier.write(" redistribute connected\n")
            for data_voisins in donnees["data"][numero_json]["interfaces"]:
                # print(as_routeur(data_voisins['neighbor']))
                # print(donnees["data"][numero_json]['as'])
                # print("next")
                if (as_routeur(data_voisins['neighbor'])) != donnees["data"][numero_json]['as']:
                    fichier.write(" passive-interface ")
                    fichier.write(data_voisins['name'])
                    fichier.write("\n")
                    
                    
        for neighbor in donnees["data"][numero_json]["interfaces"]:
            if neighbor["ospf_cost"]!="default" and donnees["data"][numero_json]["protocol"]=="OSPF":
                fichier.write("ipv6 router ospf ")
                if len(donnees["data"][numero_json]['as']) < 3 :
                    fichier.write(donnees["data"][numero_json]['as'])
                else :
                    fichier.write(donnees["data"][numero_json]['as'][:4])
                fichier.write("\n")
                fichier.write(" interface ")
                fichier.write(neighbor["name"])
                fichier.write("\n")
                fichier.write("  ip ospf cost ")
                fichier.write(neighbor["ospf_cost"])
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


def afficher_premieres_lignes(chemin_fichier, nombre_lignes=5):
    try:
        with open(chemin_fichier, 'r') as fichier:
            for i in range(nombre_lignes):
                ligne = fichier.readline()
                if not ligne:
                    break  # Arrêter si nous atteignons la fin du fichier
                print(ligne.strip())
    except FileNotFoundError:
        print(f"Le fichier '{chemin_fichier}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


liste_chemins=[]
j=0
chemin = "GNS3/Small/project-files/dynamips/"
for files in os.listdir(chemin):
    suite = "/configs/"
    fin = "*startup*.cfg"
    dossier = chemin + files + suite 
    
    
    if os.path.exists(dossier):
         
        dossier = dossier + fin
        for elmt in glob.glob(dossier):
            if os.path.exists(elmt):
               
                
                chemin_corrige = elmt.replace('\\', '/')
                
                
                liste_chemins.append(chemin_corrige)





for fichier_routeurs in liste_chemins:
    nomrouteur = nom_routeur(fichier_routeurs)
    for i in range (len(donnees["data"])):
        if donnees["data"][i]['name'] == nomrouteur:
            numero_json=i
            creation_fichier_config(fichier_routeurs, donnees,numero_json)



# Ajouter ces lignes pour vérifier le nombre de noms de routeurs et de fichiers de configuration

