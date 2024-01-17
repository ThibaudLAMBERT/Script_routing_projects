import json
import os

import glob

#TODO 
#negotiation auto ????
#duplex full ??????


#######utilisation des donnes depuuis le fichier json
with open('topo_sujet/network.json', 'r') as fichier:
    donnees = json.load(fichier)
# print(donnees["data"][1]['name'])
# for element in donnees["data"]:
#     print(element['name'])
# print(len(donnees["data"]))
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
            if (as_routeur(element['neighbor'])) == donnees["data"][numero_json]["as"]:
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
                
                fichier.write(" neighbor ")
                for truc in (donnees["data"]):
                    
                    if truc['name'] == element['neighbor']:
                        
                        for i in range (len(truc["interfaces"])):
                           
                            if nomrouteur == truc["interfaces"][i]["neighbor"]:
                                
                                fichier.write(truc["interfaces"][i]["ip"].split('/')[0])



                        
                        fichier.write(" remote-as ")
                        fichier.write(truc["as"])
                        fichier.write("\n")
        fichier.write(" address-family ipv4\n")
        fichier.write(" exit-address-family\n")
        fichier.write(" address-family ipv6\n")


        for element in donnees["data"][numero_json]["interfaces"]:
            if (as_routeur(element['neighbor'])) == donnees["data"][numero_json]["as"]:
                fichier.write("  neighbor ")
                for truc in (donnees["data"]):
                    if truc['name'] == element['neighbor']:
                        fichier.write(truc["loopback"].split('/')[0])
                        fichier.write(" activate\n")
                     

                        
            else:
                
                fichier.write("  neighbor ")
                for truc in (donnees["data"]):
                    
                    if truc['name'] == element['neighbor']:
                        
                        for i in range (len(truc["interfaces"])):
                            
                            if nomrouteur == truc["interfaces"][i]["neighbor"]:
                                
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
chemin = "gns3_automatique2/project-files/dynamips/"
for element in os.listdir(chemin):
    suite = "/configs/"
    fin = "*startup*.cfg"
    dossier = chemin + element + suite 
    
    
    if os.path.exists(dossier):
         
        dossier = dossier + fin
        for elmt in glob.glob(dossier):
            if os.path.exists(elmt):
               
                
                chemin_corrige = elmt.replace('\\', '/')
                
                
                liste_chemins.append(chemin_corrige)
# print(liste_chemins)



#là, on appelle à la main la fonction, et ca fonctionne bien tout va bien                
fichier_cfg = 'gns3_files/project-files/dynamips/ad27bb0b-dedf-408c-9304-e543a19c4627/configs/i1_startup-config.cfg'
#creation_fichier_config(fichier_cfg, donnees)
#print(liste_chemins)
#print(donnees)
#print(nuumero_json)
#quand je fais une boucle, qui semble vraiment etre la meme chose qu'au dessus, juste pour tous les chemins un par un
#eh bah ca marche plus, et j'ai des erreurs dans ma fonction creation_fichier_config, peut etre un probleme de types

for fichier_routeurs in liste_chemins:
    nomrouteur = nom_routeur(fichier_routeurs)
    for i in range (len(donnees["data"])):
        if donnees["data"][i]['name'] == nomrouteur:
            numero_json=i
            creation_fichier_config(fichier_routeurs, donnees,numero_json)

#ducoup c'est la j'ai mis le numero_json à cet endroit plutôt qu'à l'intérieur de la fonction creation_fichier_config 
#et j'ai passé numero_json en paramètre de la fonction 

# Ajouter ces lignes pour vérifier le nombre de noms de routeurs et de fichiers de configuration





