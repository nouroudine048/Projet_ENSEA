# Projet_ENSEA
# Sujet de Projet: Conception d’un robot à navigation autonome

## Description du Projet :
L’objectif principal est de contrôler un robot pour se déplacer dans un espace clos, tel qu’un un entrepôt. La consigne à laquelle il doit répondre est simple : aller d’un point de départ A à un point d’arrivée B en évitant les obstacles. 
Ce projet adresse des applications logistiques multiples et concrètes, telles que le rangement de produits en entrepôts d'usine.
 Pour ce faire, le robot sera équipé principalement d’un Lidar qui fournira toutes les données utiles à la construction de la carte de son environnement et sa localisation. De plus, on s’appuiera sur la puissance du Framework ROS2, spécialisé dans le développement robotique, pour exploiter l’ensemble des données issues des différents capteurs et piloter le rebot en conséquence. Le développement peut se faire dans différents langages : C, C++ et/ou Python.

## Ressources matérielles 
Le prototype à réaliser en impression 3D doit intégrer les éléments suivants :
- **Capteurs** : Dans un premier temps, on intègre seulement un Lidar 2D. On ajoutera par la suite, si le temps le permet, une IMU et une caméra (pour optimiser la précision de la localisation)
- **Deux moteurs pas à pas (avec encodeurs)**
- **Système numérique** : Raspberry PI-5 pour le pilotage et STM32/Arduino pour le contrôle des moteurs.
- **Bloc d’alimentation du système avec une batterie adéquate**

  # Realisation du projet

  ## Cahier de charge
  **1. Architecture Technique**
**1.1. Architecture Matérielle (Hardware)**

- Châssis : Prototype réalisé en impression 3D.
- Calculateur Principal (Cerveau) : Raspberry Pi 5.
- Contrôleur Bas Niveau : Carte STM32 accompagné d'un MD25 pour l'asservissement des moteurs.
- Capteur Principal : Un Lidar 2D.
- Actionneurs : Deux moteurs pas-à-pas avec encodeurs, contrôlés par des drivers.
- Alimentation : Batterie LiPo/Li-Ion avec circuits de régulation de puissance pour le Raspberry Pi, les moteurs et le Lidar.

**1.2. Architecture Logicielle (Software)**

- Système d'Exploitation :
- Middleware : ROS 2 Humble Hawksbill.
- Langages de Développement : Python et/ou C++.
- Bibliothèques Clés ROS2 :
          - nav2 : Pour la navigation, la planification (Nav2 Planner) et le contrôle (Nav2 Controller).
          - slam_toolbox : Pour la cartographie SLAM.
          - ros2_control : Pour une gestion abstraite et matérielle des actionneurs et capteurs.

  **2. Objectifs Non-Fonctionnels (ONF)**

- ONF1 : Autonomie : La batterie doit permettre au moins 1 heure d'opération continue.
- ONF2 : Robustesse : Le robot doit fonctionner de manière stable sans intervention humaine pendant son cycle de mission.
- ONF3 : Modularité : L'architecture logicielle basée sur ROS2 doit permettre l'ajout facile de nouveaux capteurs (IMU, caméra) à l'avenir.
- ONF4 : Précision : La localisation et la navigation doivent être suffisamment précises pour évoluer dans des couloirs d'entrepôt simulés.

**3. Objectifs Fonctionnels (OF)**

-**OF1 : Contrôle des Moteurs**
Le système doit contrôler avec précision la vitesse et la direction des deux moteurs pas-à-pas (avec encodeurs) pour assurer les déplacements.

-**OF2 : Cartographie et Localisation**
Le robot doit être capable de construire une carte 2D de son environnement (SLAM - Simultaneous Localization and Mapping) en utilisant les données du Lidar.
Il doit pouvoir se localiser en temps réel sur cette carte.

-**OF3 : Planification de Trajet**
Sur une carte préexistante ou construite, le robot doit calculer un trajet optimal entre un point de départ A et un point d'arrivée B défini par l'utilisateur.

-**OF4 : Navigation et Évitement d'Obstacles**
Le robot doit suivre le trajet planifié.
Il doit détecter et éviter les obstacles statiques et dynamiques non présents sur la carte en modifiant sa trajectoire localement.

-**OF5 : Interface Utilisateur**
Fournir un moyen simple de définir les points A et B (ex: via un terminal ou une interface graphique simple).
