# Projet 1 - Analyse des journaux d'un pare-feu (Réseaux / Sécurité / IoT)

## 👤 Informations
* **Nom :**  DIOUF
* **Prénom :** Bienvenu Ainy
* **Niveau :** L2
* **Filière / Groupe :** RSIOTP6

---

## 📌 Présentation du Projet
Ce projet consiste à analyser un jeu de données de journaux (logs) de connexions réseau sur une période d'une semaine (`data/logs_reseau.csv`). 

L'objectif est d'effectuer un nettoyage des données, d'extraire des métriques clés de sécurité, de générer des visualisations graphiques et d'identifier des comportements malveillants ou suspects sur le réseau (ex. scan de ports, exfiltration de données) afin de formuler des recommandations de sécurité adaptées.

---

## 📁 Structure du Dépôt
Le dépôt respecte la structure minimale requise pour l'évaluation :

```text
projet-analyse-NOM-Prenom/
├── README.md               # Présentation du projet et instructions
├── requirements.txt        # Dépendances Python requises
├── analyse.py              # Script principal d'analyse et de nettoyage
├── rapport.md              # Rapport d'analyse et recommandations
├── resultats.json          # Métriques clés calculées (généré automatiquement)
├── data/
│   └── logs_reseau.csv     # Fichier de données brut
└── figures/                # Graphiques générés par le script
    ├── top_ports.png
    ├── activite_temporelle.png
    ├── bytes_par_appareil.png
    └── repartition_actions.png
