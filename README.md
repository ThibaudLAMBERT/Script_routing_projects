# Projet GNS3

## Comment le lancer

1) Cloner le github sur votre machine :

``` bash
git clone https://github.com/ThibaudLAMBERT/Script_routing_projects.git
```

2) Deplacez vous dans le dossier :

``` bash
cd Script_routing_projects
```

## Description des dossiers


### GNS3

Ce dossier contient les différentes topologies utilisées utilisés lors du projet :

- Small : première topologie réalisé. Elle nous a d'abord permis de réaliser uen configuration simple.

- Sujet : ce dossier contient la topologie du sujet

- Various : topologiz plus complexe avec 4 AS. Cette topologie a été réalisé pour tester notre script sur un réseau plus complexe.

### Topology

Ce dossier contient les différents scripts qui nous ont permis d'automatiser la configuration, il contient pour chaque dossier :

- un script de génération d'un fichier d'intention (json) : json_creator.py
- le fichier d'intention : network.json
  
Ce dossier  contient aussi le script qui génère les configurations à partir du json et qui les mets dans les fichiers configs adaptés : script.py


### Fichier d'intention et configuration

Voici notre fichier d'intention pour la topologie du sujet : https://github.com/ThibaudLAMBERT/Script_routing_projects/blob/main/Topology/Sujet/network.json

Voici une configuration pour un routeur :
