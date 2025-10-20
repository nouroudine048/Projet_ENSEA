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
