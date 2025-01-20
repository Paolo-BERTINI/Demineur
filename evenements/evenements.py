##############################################################################
##############################################################################
###                 FONCTIONS QUI RÉAGISSENT À UN ÉVÉNEMENT                ###
##############################################################################
##############################################################################

from plateau.logistique import dans_plateau, decouvre_case, gagne, compte_mines_solution
from plateau.grille import dessine_plateau
from tkinter import messagebox

# Géstion clic droit
def action_clic_decouvre(clic, plateau, largeur_case, hauteur_case, plateau_courant, INCONNU, PERDU, grille, DRAPEAU,
                         drapeau_img, QUESTION, question_img, mine_img, inconnu_img, perdu_img, game_over)->None:
    """
    Fonction appelée quand on fait un clic-1 (gauche) sur la fenêtre
    découvre la case sur laquelle on a cliqué
    et redessine le plateau.
    La fonction prend en argument l'événement clic.
    C'est une procédure.
    """
    
    if game_over == True:
        return
    
    # clic.x et clic.y contiennent les coordonnées, en pixels,
    # de la souris au moment du clic (à l'intérieur de la fenêtre)
    x = clic.x // (largeur_case+1)  # x et y contiennent les
    y = clic.y // (hauteur_case+1)  # coordonnées de la case

    if not dans_plateau(plateau_courant, x, y):
        return

    if plateau_courant[x][y]["etat"] != INCONNU:
        return

    if decouvre_case(plateau_courant, x, y, INCONNU, PERDU):
        dessine_plateau(plateau_courant, grille, largeur_case, hauteur_case, DRAPEAU, drapeau_img, QUESTION,
                        question_img, INCONNU, mine_img, inconnu_img, PERDU, perdu_img, solution=True)
        game_over = True
        return

    dessine_plateau(plateau_courant, grille, largeur_case, hauteur_case, DRAPEAU, drapeau_img,
                    QUESTION, question_img, INCONNU, mine_img, inconnu_img, PERDU, perdu_img)
    if gagne(plateau_courant, DRAPEAU, INCONNU):
        print("Félicitations, vous avez gagné !")
        game_over = True
    return


# Géstion clic gauche
def action_clic_drapeau_question(clic, largeur_case, hauteur_case, plateau_courant, INCONNU, DRAPEAU, QUESTION, grille,
                                 drapeau_img, question_img, mine_img, inconnu_img, PERDU, perdu_img, game_over)->None:
    """
    Fonction appelée quand on fait un clic-3 (droit) sur la fenêtre
    place un drapeau sur la case sur laquelle on a cliqué
    et redessine le plateau.
    S'il y a déjà un drapeau, on place un point d'interrogtion.
    S'il y a déjà un point d'interrogation, on l'enlève.
    La fonction prend en argument l'événement clic.
    C'est une procédure.
    """
    if game_over == True:
        return
    
    x = clic.x // (largeur_case+1)  # x et y contiennent les
    y = clic.y // (hauteur_case+1)  # coordonnées de la case

    if not dans_plateau(plateau_courant, x, y):
        return

    etat = plateau_courant[x][y]["etat"]

    if etat == INCONNU:
        plateau_courant[x][y]["etat"] = DRAPEAU
    elif etat == DRAPEAU:
        plateau_courant[x][y]["etat"] = QUESTION
    elif etat == QUESTION:
        plateau_courant[x][y]["etat"] = INCONNU

    dessine_plateau(plateau_courant, grille, largeur_case, hauteur_case, DRAPEAU, drapeau_img,
                    QUESTION, question_img, INCONNU, mine_img, inconnu_img, PERDU, perdu_img)
    return

# Géstion boutton échap
def action_quitter(evt, root)->None:
    """
    Permet de quitter le jeux.
    La fonction prend en argument l'événement evt.
    C'est une procédure.
    """
    root.destroy()
    return

# Géstion boutton suppr/info
def action_aide(evt) -> None:
    """
    Permet d'afficher les règles du jeu.
    La fonction prend en argument l'événement evt.
    C'est une procédure.
    """
    messagebox.showinfo("Info", 
                        "Clic gauche pour ouvrir.\nClic droit pour drapeau ou \"?\".")
    return
