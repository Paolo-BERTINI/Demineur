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

from tkinter import *

def dessine_case(plateau:list, x:int, y:int, grille, largeur_case, hauteur_case, DRAPEAU, drapeau_img, QUESTION, question_img, INCONNU, mine_img, inconnu_img, PERDU, perdu_img, solution=False)->None:
    """
    Dessine la case "(x,y)" sur le plateau en fonction de son état
    Si "solution" vaut True, dessine aussi l'éventuelle mine 
    même si la case est fermée.
    C'est une procédure.
    """
    x1 = x * (largeur_case + 1) + 2
    y1 = y * (hauteur_case + 1) + 2
    x2 = (x + 1) * (largeur_case + 1 )
    y2 = (y + 1) * (hauteur_case + 1)
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
        x1 = x1 + largeur_case // 2
        y1 = y1 + hauteur_case // 2
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


def dessine_plateau(plateau:list, grille, largeur_case, hauteur_case, DRAPEAU, drapeau_img, QUESTION, question_img, INCONNU, mine_img, inconnu_img, PERDU, perdu_img, solution=False)->None:
    """
    Dessine toues les cases du plateau selon leur état en appelant la fonction 
    dessine_case sur chaque case du plateau.
    Si "solution" vaut True, les cases fermées contenant des mines 
    seront dessinées.
    C'est une procédure.
    """
    grille.delete(ALL)
    for x in range(len(plateau)):
        for y in range(len(plateau[0])):
            dessine_case(plateau, x, y, grille, largeur_case, hauteur_case, DRAPEAU, drapeau_img, QUESTION, question_img, INCONNU, mine_img, inconnu_img, PERDU, perdu_img, solution)
    return None
