#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##############################################################################
##############################################################################
###                 IMPORT DE MODULES ET FONCTIONS                         ###
##############################################################################
##############################################################################

# On importe la fonction random du module random pour placer les mines de 
# façon aléatoire.
# On importe toute la bibliothèque tkinter pour l'interface graphique.

from evenements.evenements import *
from plateau.grille import dessine_plateau
from plateau.logistique import genere_plateau, dans_plateau, gagne, decouvre_case, compte_mines_solution
from tkinter import *


##############################################################################
##############################################################################
###                         INITIALISATIONS                                ###
##############################################################################
##############################################################################

##############################################################################
### Les 13 états possibles sont modélisés par les entiers de -4 à 8 :        #
### de 0 à 8 : le nombre de mines voisines si la case est découverte,        #
### puis on fixe les 4 autres états avec les valeurs de -1 à -4 :            #
INCONNU = -1                                                                 #
PERDU = -2                                                                   #
DRAPEAU = -3                                                                 #
QUESTION = -4                                                                #
##############################################################################

# Des variables, modifiables par l'utilisateur
largeur = 15                # largeur du plateau, en nombre de cases
hauteur = 15                # hauteur du plateau, en nombre de cases
probabilite_mine = 0.2      # probabilité qu'une case contienne une mine
game_over = False           # détermine si le jeu est fini ou non

# La fenêtre principale se nomme "root" :
largeur_case = 20
hauteur_case = 20
root = Tk()
root.title("DÉMINEUR")
root.resizable(width=False, height=False)
root.geometry(f"{largeur * (largeur_case + 1) + 1}x{hauteur * (hauteur_case + 1) + 1}")
Label(text="Saisir 'a' pour obtenir de l'aide.").pack()
Label(text="Saisir 'q' pour quitter le jeu.").pack()

# Les images utilisées pour les cases spéciales
inconnu_img = PhotoImage(file="images/inconnu.gif")
question_img = PhotoImage(file="images/question.gif")
mine_img = PhotoImage(file="images/mine.gif")
drapeau_img = PhotoImage(file="images/drapeau.gif")
mauvais_drapeau_img = PhotoImage(file="images/mauvais_drapeau.gif")
perdu_img = PhotoImage(file="images/perdu.gif")

# On vérifie que toutes les images ont les mêmes dimensions
assert ( mine_img.height() == perdu_img.height() \
                           == drapeau_img.height() \
                           == mauvais_drapeau_img.height() \
                           == question_img.height() \
                           == inconnu_img.height() ) \
                           , "erreur de dimensions des images"

assert ( mine_img.width() == perdu_img.width() \
                          == drapeau_img.width() \
                          == mauvais_drapeau_img.width() \
                          == question_img.width() \
                          == inconnu_img.width() ) \
                          , "erreur de dimensions des images"

# On récupère les dimensions communes à toutes les images :
largeur_case = mine_img.width()
hauteur_case = mine_img.height()

# "grille" est un objet de type "Canvas" pour pouvoir dessiner dedans 
# "grille" appartient à la fenêtre "root".
grille = Canvas(root , width=largeur*(largeur_case+1)+1 , \
                height=hauteur*(hauteur_case+1)+1, bg="#7f7f7f")
# On place "grille" sur la fenêtre "root" :
grille.pack()



##############################################################################
##############################################################################
###                       GESTION DES ÉVÉNEMENTS                           ###
##############################################################################
##############################################################################

# On va utiliser la méthode bind pour les événements à gérer.
# La syntaxe est la suivante :  bind('evenement', commande)
# 'evenement' doit être un événement (saisie d'une touche, clic de souris, ...)
# commande est une fonction prenant un evenement en argument dans sa définition
# Le paramètre evenement est omis lors de l'appel.

# On quitte le programme avec la touche "échap".
root.bind("<Escape>", lambda event: action_quitter(event, root))

# On affiche la solution pendant une seconde avec la touche "t" pour triche.
root.bind("<Insert>", lambda event: action_afficher_solution(event, plateau_courant, grille, largeur_case, hauteur_case,
                                                             DRAPEAU, drapeau_img, QUESTION, question_img, INCONNU,
                                                             mine_img, inconnu_img, PERDU, perdu_img))

# On obtient de l'aide avec la touche "suppr".
root.bind("<Delete>", lambda event: action_aide(event))
### QUESTION : écrire les deux instructions correspondantes :


# Pour la souris, quelques événements possibles (il en existe d'autres) :
# <Button-1>           : Clic gauche
# <Button-2>           : Clic milieu 
# <Button-3>           : Clic droit
# <Double-Button-1>    : Double clic droit
# <Double-Button-2>    : Double clic gauche

# On ouvre la case avec un clic gauche
grille.bind("<Button-1>", lambda clic: action_clic_decouvre(clic, plateau_courant, largeur_case, hauteur_case,
                                                            plateau_courant, INCONNU, PERDU, grille, DRAPEAU,
                                                            drapeau_img, QUESTION, question_img, mine_img,
                                                            inconnu_img, perdu_img, game_over))


# On place un drapeau ou un point d'interrogation avec un clic droit
### QUESTION : écrire l'instruction correspondante
grille.bind("<Button-3>", lambda clic: action_clic_drapeau_question(clic, largeur_case, hauteur_case, plateau_courant, INCONNU,
                                                                    DRAPEAU, QUESTION, grille, drapeau_img, question_img,
                                                                    mine_img, inconnu_img, PERDU, perdu_img, game_over))



##############################################################################
##############################################################################
###                     LANCEMENT DU PROGRAMME                             ###
##############################################################################
##############################################################################

# On crée le plateau de jeu :
plateau_courant = genere_plateau(largeur, hauteur, probabilite_mine, INCONNU)

# On dessine le plateau de jeu :
dessine_plateau(plateau_courant, grille, largeur_case, hauteur_case,DRAPEAU,drapeau_img,
                QUESTION, question_img, INCONNU, mine_img, inconnu_img, PERDU, perdu_img)

# Affiche la fenêtre et lance la boucle de gestion des événements :
grille.mainloop()
