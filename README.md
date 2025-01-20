# Démineur

## Introduction
Ce projet est une implémentation du jeu classique **Démineur**, codé en Python. Il permet aux utilisateurs de jouer à une version graphique de ce jeu de stratégie populaire. Le projet est conçu pour être facilement exécuté sur une machine locale.

## Prérequis
- Python 3.8 ou supérieur
- Les bibliothèques Python suivantes :
  - `tkinter` (pour l'interface graphique)
  - `os` et d'autres modules standards.

## Utilisation
Au lancement, une interface graphique apparaîtra pour vous permettre de jouer.

### Commandes disponibles
- Cliquez sur une case pour dévoiler son contenu.
- Marquez une case suspectée de contenir une mine en effectuant un clic droit.
- Appuyez sur le bouton **échap** pour quitter le jeu et fermer la fenêtre de jeu.
- Appuyez sur le bouton **SUPPR** pour avoir des informations sur le jeu de jeu.

## Structure du projet

- `main.py` : Point d'entrée principal du programme.
- `evenements/` : Contient la gestion des différents événements du jeu.
- `plateau/` : Gère la logique du plateau et les opérations principales.
- `images/` : Ressources graphiques utilisées dans l'interface.
- `README.md` : Documentation du projet.
