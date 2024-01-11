import json
import pandas as pd



with open('Script2/network.json', 'r') as fichier:
    donnees = json.load(fichier)




# for element in donnees["data"]:
#     print(element['name'])
# print(donnes["data"])
print(donnees["data"][1]['name'])




# Créer un DataFrame avec des données de configuration
data = {
    'Section': ['Section1', 'Section1', 'Section2', 'Section2'],
    'Option': ['Option1', 'Option2', 'Option3', 'Option4'],
    'Value': ['valeur1', 'valeur2', 'valeur3', 'valeur4']
}

df = pd.DataFrame(data)

# Convertir le DataFrame en une chaîne de caractères sans délimiteur
config_string = df.to_string(index=False, header=False)

# Écrire la chaîne dans un fichier .cfg
with open('Script2/config.cfg', 'w') as fichier_cfg:
    fichier_cfg.write(config_string)