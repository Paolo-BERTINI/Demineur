##############################################################################
##############################################################################
###                     FONCTIONS POUR LE PLATEAU DE JEU                   ###
##############################################################################
##############################################################################



from random import random

def genere_plateau(largeur:int, hauteur:int, probabilite_mine:float, INCONNU:int)->list:
    """
    Renvoie un plateau de jeu de taille largeur et hauteur données en argument
    Chaque case contenant une mine avec la probabilité donnée en argument
    """
    plateau = []
    for i in range(hauteur):
        ligne = []
        for j in range(largeur):
            mine_present = random() < probabilite_mine
            case = {"mine": mine_present, "etat": INCONNU}
            ligne.append(case)
        plateau.append(ligne)
    return plateau

def dans_plateau(plateau:list, x:int, y:int)->bool:
    """
    Teste si la case de coordonnées (x,y) est sur le plateau.
    Renvoie le booléen correspondant.
    """
    return 0 <= x < len(plateau) and 0 <= y < len(plateau[0]) 

def cases_voisines(plateau:list, x:int, y:int)->list:
    """
    Renvoie la liste des coordonnées (tableaux de 2 entiers) des cases
    voisines de la case "(x,y)"
    Ne se préoccupe pas de savoir si la case "(x,y)" est dans le plateau
    """
    lst = []
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i, j) != (x, y):
                lst.append((i, j))
    return lst

def compte_mines_voisines(plateau:list, x:int, y:int)->int:
    """
    Renvoie le nombre de mines voisines de la case "(x,y)" sur le plateau
    """
    mines_voisines = 0
    for i, j in cases_voisines(plateau, x, y):
        if dans_plateau(plateau, i, j) and plateau[i][j]["mine"]:
            mines_voisines += 1
    return mines_voisines

def composante_connexe(plateau:list, x:int, y:int, INCONNU:int)->None:
    """
    Met le plateau à jour en ouvrant façon récursive
    toutes les cases vides voisines de la case "(x,y)".
    Une case vide est une case sans mine n'ayant aucun voisin avec une mine
    La fonction s'arrêtera sur les cases contenant un entier entre 1 et 8
    Attention, c'est une procédure (renvoie None) récursive (cas de base ?)
    """
    if dans_plateau(plateau, x, y) and plateau[x][y]["etat"] == INCONNU:
        plateau[x][y]["etat"] = compte_mines_voisines(plateau, x, y)
        if plateau[x][y]["etat"] == 0:
            for i, j in cases_voisines(plateau, x, y):
                composante_connexe(plateau, i, j, INCONNU)

def perdu(plateau:list, PERDU:int)->bool:
    """
    Renvoie True lorsque que le plateau contient 
    une case découverte avec une mine, 
    c-à-d une case dont l'état est PERDU
    """
    global game_over
    for ligne in plateau:
        for case in ligne:
            if case["etat"] == PERDU:
                game_over = True
                return True
    return False

def gagne(plateau: list, DRAPEAU:int, INCONNU:int) -> bool:
    """
    renvoie True lorsque que le plateau contient les drapeaux exactement
    sur les cases minées et que toutes les autres cases sont découvertes
    """
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j]["mine"] and plateau[i][j]["etat"] != DRAPEAU:
                return False
            if not plateau[i][j]["mine"] and plateau[i][j]["etat"] == INCONNU:
                return False
    return True

def decouvre_case(plateau:list, x:int, y:int, INCONNU:int, PERDU:int)->bool:
    """Découvre une case sur le plateau. Le plateau est mis à jour en
    découvrant toute la composante connexe de la case "(x,y)", et la fonction
    renvoie un booléen pour dire si la case "(x,y)" était une mine ou pas.
    Attention, c'est à la fois une procédure (modification de l'argument 
    "plateau" et une fonction (qui renvoie un booléen).
    """
    if not dans_plateau(plateau, x, y) or plateau[x][y]["etat"] != INCONNU:
        return False
    if plateau[x][y]["mine"]:
        plateau[x][y]["etat"] = PERDU
        print(f"OUPS... La case ({x},{y}) contenait une mine !")
        return True
    composante_connexe(plateau, x, y, INCONNU)
    return False

def compte_mines_solution(plateau:list)->None:
    """
    Met le plateau à jour en comptant le nombre de mines partout.
    Attention, c'est une procédure.
    """
    for i, ligne in range(plateau):
        for j, case in range(ligne):
            plateau[i][j]["etat"] = compte_mines_voisines(plateau, i, j)
    return
