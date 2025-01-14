#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##############################################################################
##############################################################################
#####                                                                    #####
#####                       LE JEU DU DÉMINEUR                           #####
#####                                                                    #####
##############################################################################
##############################################################################


##############################################################################
#                                                                            #
#                         Paradygme choisie :                                #
#                    la programmation fonctionnelle                          #
#                                                                            #
##############################################################################


##############################################################################                                                                           #
#  Vous devez lire l'intégralité du code avant de commencer à le compléter,  #
#                ainsi que les commentaires et les explications.             #
##############################################################################

##############################################################################
#            Le code est séparé en plusieurs parties :                       # 
#                                                                            #
#                   - IMPORT DE MODULES ET FONCTIONS                         #
#                   - EXPLICATIONS                                           #
#                   - FONCTIONS POUR LE PLATEAU DE JEU                       #
#                   - FONCTIONS d'AFFICHAGE SUR LA GRILLE                    #
#                   - FONCTIONS QUI RÉAGISSENT À UN ÉVÉNEMENT                #
#                   - INITIALISATIONS                                        #
#                   - GESTION DES ÉVÉNEMENTS                                 #
#                   - LANCEMENT DU PROGRAMME                                 #
#                   - AMÉLIORATIONS                                          #
##############################################################################



##############################################################################
##############################################################################
###                 IMPORT DE MODULES ET FONCTIONS                         ###
##############################################################################
##############################################################################

# On importe la fonction random du module random pour placer les mines de 
# façon aléatoire.
# On importe toute la bibliothèque tkinter pour l'interface graphique.
from plateau.logistique import genere_plateau, dans_plateau, gagne, decouvre_case, compte_mines_solution
from tkinter import *



##############################################################################
##############################################################################
###                             EXPLICATIONS                               ###
##############################################################################
##############################################################################


### Plateau de jeu
### Le plateau est simplement représenté par une matrice (un tableau de
### tableaux).
### La case de coordonnées "(i,j)" est un dictionnaire à deux champs :
###   - "mine" qui est un booléen et qui indique si la case contient une mine
###   - "etat" qui indique l'état de la case :
###        - INCONNU quand le joueur n'a pas découvert la case
###        - un entier entre 0 et 8 qui indique le nombre de mines voisines,
###          quand le joueur a découvert la case
###        - DRAPEAU quand le joueur a mis un drapeau sur la case
###        - QUESTION quand le joueur n'est pas sûr.
###        - PERDU quand il s'agit d'une case avec une mine, sur laquelle le
###          joueur a cliqué.

##############################################################################
### Les 13 états possibles sont modélisés par les entiers de -4 à 8 :        #
### de 0 à 8 : le nombre de mines voisines si la case est découverte,        #
### puis on fixe les 4 autres états avec les valeurs de -1 à -4 :            #
INCONNU = -1                                                                 #
PERDU = -2                                                                   #
DRAPEAU = -3                                                                 #
QUESTION = -4                                                                #
##############################################################################

game_over = False




##############################################################################
##############################################################################
###                FONCTIONS d'AFFICHAGE SUR LA GRILLE                     ###
##############################################################################
##############################################################################
    
### La fonction "dessine_case" utilise une constante globale (définie plus
### bas) "grille" qui représente la grille des cases du jeu.
### Cette grille est la représentation graphique du "plateau" de jeu.
### "grille" est un objet de type "Canvas" et a des méthodes de dessin
### comme "create_rectangle" et autres.


def dessine_case(plateau:list, x:int, y:int, solution=False)->None:
    """
    Dessine la case "(x,y)" sur le plateau en fonction de son état
    Si "solution" vaut True, dessine aussi l'éventuelle mine 
    même si la case est fermée.
    C'est une procédure.
    """
    x1 = x*(largeur_case+1)+2
    y1 = y*(hauteur_case+1)+2
    x2 = (x+1)*(largeur_case+1)
    y2 = (y+1)*(hauteur_case+1)
    etat = plateau[x][y]["etat"]
    if etat == 0:
        grille.create_rectangle(x1, y1, x2, y2, \
                                outline='#c0c0c0', fill='#c0c0c0')
    elif 0 < etat < 9:
        couleurs = ["blue", "green", "red", \
                    "darkblue", "maroon", "light sea green", "black", "gray"]
        chiffre_couleur = couleurs[etat - 1]
        grille.create_rectangle(x1, y1, x2, y2, \
                                outline='#c0c0c0', fill='#c0c0c0')
        x1 = x1 + largeur_case//2
        y1 = y1 + hauteur_case//2
        grille.create_text(x1, y1, justify=CENTER, text=str(etat), \
                           fill=chiffre_couleur, font=("Arial", 10, "bold"))
    elif etat == DRAPEAU:
        grille.create_image(x1, y1, image=drapeau_img, anchor=NW)
    elif etat == QUESTION:
        grille.create_image(x1, y1, image=question_img, anchor=NW)
    elif etat == INCONNU:
        if plateau[x][y]["mine"] and solution:
            grille.create_image(x1, y1, image=mine_img, anchor=NW)
        else:
            grille.create_image(x1, y1, image=inconnu_img, anchor=NW)
    elif etat == PERDU:
        grille.create_image(x1, y1, image=perdu_img, anchor=NW)
    else:
        assert False , "On ne passera jamais par là !"
    return None


def dessine_plateau(plateau:list, solution=False)->None:
    """
    Dessine toues les cases du plateau selon leur état en appelant la fonction 
    dessine_case sur chaque case du plateau.
    Si "solution" vaut True, les cases fermées contenant des mines 
    seront dessinées.
    C'est une procédure.
    """
    l = len(plateau)
    h = len(plateau[0])
    grille.delete(ALL)
    for x in range(l):
        for y in range(h):
            dessine_case(plateau, x, y, solution)
    return None



##############################################################################
##############################################################################
###                 FONCTIONS QUI RÉAGISSENT À UN ÉVÉNEMENT                ###
##############################################################################
##############################################################################
    
### Dans ces fonctions,
###    - "plateau" est une variable globale qui contient le plateau courant,
###    - "grille" est une constante globale qui contient la fenêtre.
    
### Ces variables étant de type construit, elles sont forcément globales.

### QUESTION : compléter le code de la fonction suivante
def action_clic_decouvre(clic, plateau)->None:
    """
    Fonction appelée quand on fait un clic-1 (gauche) sur la fenêtre
    découvre la case sur laquelle on a cliqué
    et redessine le plateau.
    La fonction prend en argument l'événement clic.
    C'est une procédure.
    """
    global game_over
    
    if game_over == True:
        return None
    
    # clic.x et clic.y contiennent les coordonnées, en pixels,
    # de la souris au moment du clic (à l'intérieur de la fenêtre)
    x = clic.x // (largeur_case+1)  # x et y contiennent les
    y = clic.y // (hauteur_case+1)  # coordonnées de la case

    if not dans_plateau(plateau_courant, x, y):
        return None

    if plateau_courant[x][y]["etat"] != INCONNU:
        return None

    if decouvre_case(plateau_courant, x, y, INCONNU, PERDU):
        dessine_plateau(plateau_courant, solution=True)
        game_over = True
        return None

    dessine_plateau(plateau_courant)
    if gagne(plateau_courant, DRAPEAU, INCONNU):
        print("Félicitations, vous avez gagné !")
        game_over = True
    return None



### QUESTION : compléter le code de la fonction suivante
def action_clic_drapeau_question(clic)->None:
    """
    Fonction appelée quand on fait un clic-3 (droit) sur la fenêtre
    place un drapeau sur la case sur laquelle on a cliqué
    et redessine le plateau.
    S'il y a déjà un drapeau, on place un point d'interrogtion.
    S'il y a déjà un point d'interrogation, on l'enlève.
    La fonction prend en argument l'événement clic.
    C'est une procédure.
    """
    global game_over
    if game_over == True:
        return None
    
    x = clic.x // (largeur_case+1)  # x et y contiennent les
    y = clic.y // (hauteur_case+1)  # coordonnées de la case

    if not dans_plateau(plateau_courant, x, y):
        return None

    etat = plateau_courant[x][y]["etat"]

    if etat == INCONNU:
        plateau_courant[x][y]["etat"] = DRAPEAU
    elif etat == DRAPEAU:
        plateau_courant[x][y]["etat"] = QUESTION
    elif etat == QUESTION:
        plateau_courant[x][y]["etat"] = INCONNU

    dessine_plateau(plateau_courant)
    return None



def action_afficher_solution(evt)->None:
    """
    Permet d'afficher la solution pendant 1 seconde.
    La fonction prend en argument l'événement evt.
    C'est une procédure.
    """
    import copy
    from time import sleep
    # On copie le plateau courant sans le modifier
    p = copy.deepcopy(plateau_courant)
    compte_mines_solution(p)
    # On dessine le plateau avec les solutions
    dessine_plateau(p, True)
    grille.update_idletasks()
    sleep(1)
    # On dessine à nouveau le plateau courant
    dessine_plateau(plateau_courant)
    return None


def action_quitter(evt)->None:
    """
    Permet de quitter le jeux.
    La fonction prend en argument l'événement evt.
    C'est une procédure.
    """
    root.destroy()
    return None


def action_aide(evt)->None:
    """
    Permet d'afficher les régles du jeu.
    La fonction prend en argument l'événement evt.
    C'est une procédure.
    """
    messagebox.showinfo("Aide", \
    "Clic gauche pour ouvrir.\nClic droit pour drapeau ou ?.")
    return None



##############################################################################
##############################################################################
###                         INITIALISATIONS                                ###
##############################################################################
##############################################################################
    
##############################################################################
###       Initialisation de la fenêtre graphique et d'autres variables     ###

# Des variables, modifiables par l'utilisateur
largeur = 15                # largeur du plateau, en nombre de cases
hauteur = 15                # hauteur du plateau, en nombre de cases
probabilite_mine = 0.2     # probabilité qu'une case contienne une mine


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

# On quitte le programme avec la touche "q".
root.bind("q", action_quitter)

# On affiche la solution pendant une seconde avec la touche "t" pour triche.
# On obtient de l'aide avec la touche "a".
### QUESTION : écrire les deux instructions correspondantes :


# Pour la souris, quelques événements possibles (il en existe d'autres) :
# <Button-1>           : Clic gauche
# <Button-2>           : Clic milieu 
# <Button-3>           : Clic droit
# <Double-Button-1>    : Double clic droit
# <Double-Button-2>    : Double clic gauche

# On ouvre la case avec un clic gauche
grille.bind("<Button-1>", lambda event: action_clic_decouvre(event, plateau_courant))


# On place un drapeau ou un point d'interrogation avec un clic droit
### QUESTION : écrire l'instruction correspondante
grille.bind("<Button-3>", action_clic_drapeau_question)



##############################################################################
##############################################################################
###                     LANCEMENT DU PROGRAMME                             ###
##############################################################################
##############################################################################

# On crée le plateau de jeu :
plateau_courant = genere_plateau(largeur, hauteur, probabilite_mine, INCONNU)

# On dessine le plateau de jeu :
dessine_plateau(plateau_courant)

# Affiche la fenêtre et lance la boucle de gestion des événements :
grille.mainloop()


##############################################################################
##############################################################################
###                             AMÉLIORATIONS                              ###
##############################################################################
##############################################################################

###  Montrer la solution lorsque la partie est perdue.

###  Proposer au joueur de choisir les dimensions de la grille.

###  Utiliser l'image mauvais_drapeau_img dans la fonction dessine_case en mode
###  solution lorsqu'un drapeau était mal placé.

###  Faire en sorte que la première case cliquée ne soit jamais une mine.

###  Ajouter un compteur de drapeaux.

###  Ajouter un compteur de mines.

###  Ajouter un chronomètre.

###  Mémoriser les meilleurs scores dans un fichier.



###############################    FIN    ####################################