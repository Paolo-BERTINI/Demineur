##############################################################################
##############################################################################
###                       GESTION DES ÉVÉNEMENTS                           ###
##############################################################################
##############################################################################

from evenements.evenements import *

def gestion_events(root, plateau_courant, grille, largeur_case, hauteur_case, DRAPEAU, drapeau_img,
                   QUESTION, question_img, INCONNU, mine_img, inconnu_img, PERDU, perdu_img, game_over):
    # On quitte le programme avec la touche "échap".
    root.bind("<Escape>", lambda event: action_quitter(event, root))

    # On obtient de l'aide avec la touche "suppr".
    root.bind("<Delete>", lambda event: action_aide(event))
    
    # On ouvre la case avec un clic gauche
    grille.bind("<Button-1>", lambda clic: action_clic_decouvre(clic, plateau_courant, largeur_case, hauteur_case,
                                                                plateau_courant, INCONNU, PERDU, grille, DRAPEAU,
                                                                drapeau_img, QUESTION, question_img, mine_img,
                                                                inconnu_img, perdu_img, game_over))

    # On place un drapeau ou un point d'interrogation avec un clic droit
    grille.bind("<Button-3>", lambda clic: action_clic_drapeau_question(clic, largeur_case, hauteur_case, plateau_courant, INCONNU,
                                                                        DRAPEAU, QUESTION, grille, drapeau_img, question_img,
                                                                        mine_img, inconnu_img, PERDU, perdu_img, game_over))
    
    return
