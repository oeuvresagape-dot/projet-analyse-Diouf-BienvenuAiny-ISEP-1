# Rapport d'Analyse des Journaux du Pare-Feu

**Auteur :** [Votre Nom et Prénom]  
**Rôle :** Technicien(ne) Sécurité  
**Date :** [Date du jour]  
**Projet :** Analyse des logs réseau (Niveau L3)

---

## 1. Résumé Exécutif

Au cours de la semaine écoulée, le pare-feu de l'entreprise a enregistré un ensemble de connexions impliquant divers équipements du réseau (PC, serveurs, caméras IoT et capteurs IoT). L'analyse globale des journaux après nettoyage révèle une activité réseau caractérisée par un trafic principalement légitime (majorité de requêtes HTTP/HTTPS et DNS), mais également perturbée par des anomalies ciblées. Une proportion significative de paquets a été bloquée par les règles du pare-feu, soulignant des tentatives d'accès non autorisées. Enfin, l'examen détaillé des métriques a permis de mettre en évidence deux comportements fortement suspects attribuables à des équipements spécifiques du réseau.

---

## 2. Analyse des Comportements Suspects et Preuves

### 🔍 Comportement Suspect 1 : Tentative de Reconnaissance (Scan de Ports)
* **Description :** Une adresse IP interne a contacté un nombre anormalement élevé de ports de destination distincts sur une très courte période. Ce comportement est typique d'une phase de reconnaissance (port scanning) visant à identifier des services vulnérables ou ouverts sur le réseau.
* **Preuves et Chiffres Clés :**
  * **Adresse IP source incriminée (`ip_scanner`) :** Identifiée dans le fichier `resultats.json`.
  * **Indicateur :** Cette IP a interrogé un grand nombre de ports distincts (comparé à la moyenne des autres équipements qui n'en sollicitent que 2 à 4).
  * **Support Visuel :** Le graphique `figures/top_ports.png` montre une dispersion anormale des requêtes vers des ports non standards (ex. Telnet port 23, MQTT port 1883) initiées par cet hôte.

### 🔍 Comportement Suspect 2 : Exfiltration de Données ou Compromission d'un Équipement
* **Description :** Une adresse IP appartenant au réseau a émis un volume disproportionné de données (`bytes_sent`) par rapport au fonctionnement normal des machines de sa catégorie. Ce pic de trafic sortant/interne indique une possible exfiltration de données confidentielles ou un appareil compromis utilisé comme relais.
* **Preuves et Chiffres Clés :**
  * **Adresse IP source incriminée (`ip_exfiltration`) :** Identifiée dans le fichier `resultats.json`.
  * **Indicateur :** Le volume total d'octets envoyés par cette IP dépasse largement la médiane globale observée sur l'ensemble des équipements.
  * **Support Visuel :** Le graphique `figures/bytes_par_appareil.png` illustre une dissymétrie majeure dans la répartition des octets transmis, mettant en évidence un volume anormalement élevé concentré sur cet équipement.

---

## 3. Recommandations de Sécurité Concrètes

Afin de neutraliser les menaces identifiées et d'améliorer la posture de sécurité globale de l'entreprise, les trois mesures suivantes doivent être appliquées à court terme :

1. **Isolation et Segmentation du Réseau IoT (VLAN dédié) :**
   * *Action :* Isoler l'ensemble des caméras et capteurs IoT (`camera_IoT`, `capteur_IoT`) dans un VLAN strict, séparé des postes de travail (`PC`) et des serveurs.
   * *Objectif :* Limiter le déplacement latéral en cas de compromission d'un objet connecté vulnérable.

2. **Mise en Place de Règles de Pare-Feu Strictes et Fermeture des Protocoles Incurisés :**
   * *Action :* Bloquer définitivement les flux utilisant des protocoles non chiffrés et obsolètes tels que **Telnet (port 23)** au profit de SSH (port 22). Restreindre l'accès au protocole **MQTT (port 1883)** uniquement aux courtiers (brokers) autorisés.
   * *Objectif :* Réduire la surface d'attaque et prévenir l'interception d'identifiants en clair.

3. **Mise en Place d'une Règle de Bannissement Automatique (IDS/IPS ou Fail2ban) :**
   * *Action :* Configurer le pare-feu pour bloquer automatiquement toute adresse IP effectuant plus de $N$ tentatives de connexion sur des ports distincts en moins de 60 secondes (détection de balayage de ports).
   * *Objectif :* Contrer immédiatement les tentatives de reconnaissance réseau avant qu'une vulnérabilité ne soit exploitée.
