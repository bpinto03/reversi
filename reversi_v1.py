import datetime
import sys
from doctest import testmod
import tkinter

from upemtk import *

TAILLE_CASE = 75
TAILLE_PLATEAU = 8

DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

B = 1    # Blancs
N = 0    # Noirs
V = "."  # Vide
C = "?"  # Coup possible


def pixel_vers_case(pixel: tuple, taille_case: int):
    """
    Convertit les coordonées d'un pixel en coordonées d'une case du plateau.
    :param tuple pixel: Coordonées du pixel.
    :param int taille_case: Taille des cases.
    :return tuple: Coordonées de la case.

    >>> pixel_vers_case((100, 200), 50)
    (2, 4)
    """
    i, j = pixel
    return i // taille_case, j // taille_case


def case_vers_pixel(case: tuple, taille_case: int):
    """
    Donne le pixel au centre d'une case à partir de ses coordonées.
    :param tuple case: Coordonées de la case.
    :param int taille_case: Taille des cases.
    :return tuple: Coordonées du pixel.

    >>> case_vers_pixel((0, 0), 50)
    (25.0, 25.0)
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def init_plateau(taille: int):
    """
    Génère une liste de listes correspondant au plateau.
    :param int taille: Longueur et largueur du plateau.
    :return list: Liste de listes d'entiers.

    >>> init_plateau(2)
    [['.', '.'], ['.', '.']]
    """
    resultat = []
    for i in range(taille):
        resultat.append([V] * taille)
    return resultat


def dessine_plateau(plateau: list, ex_plateau: list, boutons: dict, joueur: int):
    """
    Dessine le plateau à partir d'une liste de listes ainsi que la barre inférieure.
    :param list plateau: Liste contenant le plateau.
    :param list ex_plateau: Plateau du tour précédent.
    :param dict boutons: Dictionnaires des boutons du jeu.
    :param int joueur: Joueur actuel.
    """
    index = 0
    y = 0
    efface_tout()
    while y < len(plateau):
        x = 0
        while x < len(plateau[y]):
            rectangle(x * TAILLE_CASE, y * TAILLE_CASE, x * TAILLE_CASE + TAILLE_CASE, y * TAILLE_CASE + TAILLE_CASE,
                      tag=str(index), remplissage='darkgreen')
            x_pixel, y_pixel = case_vers_pixel((x, y), TAILLE_CASE)
            if plateau[y][x] == B:
                cercle(x_pixel, y_pixel, 9 * TAILLE_CASE / 20, remplissage="white")
            elif plateau[y][x] == N:
                cercle(x_pixel, y_pixel, 9 * TAILLE_CASE / 20, remplissage="black")
            elif plateau[y][x] == C:
                cercle(x_pixel, y_pixel, 9 * TAILLE_CASE / 20, remplissage="green", couleur="darkgreen")
            index += 1
            x += 1
        y += 1
    if joueur == B:
        rectangle(0, len(plateau) * TAILLE_CASE, len(plateau) * TAILLE_CASE,
                  len(plateau) * TAILLE_CASE + regles['taille_barre'], remplissage="white")
        texte(10, 10 + len(plateau) * TAILLE_CASE, "Au tour des blancs")
    if joueur == N:
        rectangle(0, len(plateau) * TAILLE_CASE, len(plateau) * TAILLE_CASE,
                  len(plateau) * TAILLE_CASE + regles['taille_barre'], remplissage="black")
        texte(10, 10 + len(plateau) * TAILLE_CASE, "Au tour des noirs", couleur="white")
    boutons["quitter"] = dessine_bouton(len(plateau) * TAILLE_CASE - 5,
                                        len(plateau) * TAILLE_CASE + regles['taille_barre'] - 5,
                                        "Quitter", ancrage='se')
    if ex_plateau is not None:
        boutons["annuler"] = dessine_bouton(
            len(plateau) * TAILLE_CASE - 10 - (boutons["quitter"][2] - boutons["quitter"][0]),
            len(plateau) * TAILLE_CASE + regles['taille_barre'] - 5, "Annuler", ancrage='se')


def dessine_bouton(x: int, y: int, contenu: str, ancrage: str = 'nw', couleur: str = 'white', taille: int = 24,
                   largeur: str = None):
    """
    Dessine un bouton aux coordonnées renseignées.
    :param x: Abscisse du point d'ancrage.
    :param y: Ordonnée du point d'ancrage.
    :param contenu: Texte à insérer dans le bouton.
    :param ancrage: Ancrage du bouton.
    :param couleur: Couleur de remplissage du bouton.
    :param taille: Taille du texte.
    :param largeur: Chaîne de caractère déterminant la largeur du bouton.
    :return tuple: Coordonées du bouton.

    >>> cree_fenetre(0, 0)
    >>> dessine_bouton(0, 0, "test")
    (0, 0, 49, 35)
    >>> ferme_fenetre()
    """
    if largeur is None:
        largeur = contenu
    longueur, hauteur = taille_texte(largeur, taille=taille)
    hauteur -= hauteur % 5
    if ancrage == 'nw':
        rectangle(x, y, x + longueur + 2 * 5, y + hauteur + 2 * 5, remplissage=couleur)
        texte(x + (longueur + 2 * 5) // 2, y + (hauteur + 2 * 5) // 2, contenu, ancrage='center', taille=taille)
        return x, y, x + longueur + 2 * 5, y + hauteur + 2 * 5
    elif ancrage == 'n':
        rectangle(x - (longueur + 2 * 5) // 2, y, x + (longueur + 2 * 5) // 2, y + hauteur + 2 * 5, remplissage=couleur)
        texte(x, y + (hauteur + 2 * 5) // 2, contenu, ancrage='center', taille=taille)
        return x - (longueur + 2 * 5) // 2, y, x + (longueur + 2 * 5) // 2, y + hauteur + 2 * 5
    elif ancrage == 'ne':
        rectangle(x - longueur - 2 * 5, y, x, y + hauteur + 2 * 5, remplissage=couleur)
        texte(x + (longueur + 2 * 5) // 2, y - (hauteur + 2 * 5) // 2, contenu, ancrage='center', taille=taille)
        return x - longueur - 2 * 5, y, x, y + hauteur + 2 * 5
    elif ancrage == 'e':
        rectangle(x - hauteur - 2 * 5, y - (hauteur + 2 * 5) // 2, x, y + (hauteur + 2 * 5) // 2, remplissage=couleur)
        texte(x - (longueur + 2 * 5) // 2, y, contenu, ancrage='center', taille=taille)
        return x - hauteur - 2 * 5, y - (hauteur + 2 * 5) // 2, x, y + (hauteur + 2 * 5) // 2
    elif ancrage == 'se':
        rectangle(x - longueur - 2 * 5, y - hauteur - 2 * 5, x, y, remplissage=couleur)
        texte(x - (longueur + 2 * 5) // 2, y - (hauteur + 2 * 5) // 2, contenu, ancrage='center', taille=taille)
        return x - longueur - 2 * 5, y - hauteur - 2 * 5, x, y
    elif ancrage == 's':
        rectangle(x - (longueur + 2 * 5) // 2, y - hauteur - 2 * 5, x + (longueur + 2 * 5) // 2, y, remplissage=couleur)
        texte(x, y - (hauteur + 2 * 5) // 2, contenu, ancrage='center', taille=taille)
        return x - (longueur + 2 * 5) // 2, y - hauteur - 2 * 5, x + (longueur + 2 * 5) // 2, y
    elif ancrage == 'sw':
        rectangle(x, y - hauteur - 2 * 5, x + longueur + 2 * 5, y, remplissage=couleur)
        texte(x + (longueur + 2 * 5) // 2, y - (hauteur + 2 * 5) // 2, contenu, ancrage='center', taille=taille)
        return x, y - hauteur - 2 * 5, x + longueur + 2 * 5, y
    elif ancrage == 'w':
        rectangle(x, y - (hauteur + 2 * 5) // 2, x + hauteur + 2 * 5, y + (hauteur + 2 * 5) // 2, remplissage=couleur)
        texte(x + (longueur + 2 * 5) // 2, y, contenu, ancrage='center', taille=taille)
        return x, y - (hauteur + 2 * 5) // 2, x + hauteur + 2 * 5, y + (hauteur + 2 * 5) // 2
    elif ancrage == 'center':
        rectangle(x - (longueur + 2 * 5) // 2, y - (hauteur + 2 * 5) // 2, x + (longueur + 2 * 5) // 2,
                  y + (hauteur + 2 * 5) // 2, remplissage=couleur)
        texte(x, y, contenu, ancrage='center', taille=taille)
        return x - (longueur + 2 * 5) // 2, y - (hauteur + 2 * 5) // 2, x + (longueur + 2 * 5) // 2, \
               y + (hauteur + 2 * 5) // 2


def chercher_coups(plateau: list, joueur: int):
    """
    Parcoure le plateau et recherche les coups disponibles.
    :param list plateau: Liste contenant le plateau.
    :param int joueur: Joueur actuel.
    :return list: Liste des coups possibles

    >>> chercher_coups([[B, B, B], \
                        [N, N, N], \
                        [V, V, B]], B)
    [(0, 2), (1, 2)]
    """
    resultat = []
    for y in range(len(plateau)):
        for x in range(len(plateau[y])):
            if coup_valide(plateau, (x, y), joueur):
                resultat.append((x, y))
    return resultat


def verifier_victoire(plateau: list, joueur: int):
    """
    Vérifie si un des deux joueurs remporte la partie.
    :param list plateau: Liste contenant le plateau.
    :param int joueur: Joueur en cours.
    :return tuple: Numéro du joueur gagnant, 0 si le jeu continu et booléen symbolisant une victoire écrasante.

    >>> verifier_victoire([[B, N, B], \
                           [N, N, N], \
                           [B, N, B]], B)
    (0, False)
    """
    compteur_b = 0
    compteur_n = 0
    for y, ligne in enumerate(plateau):
        for x, case in enumerate(ligne):
            if coup_valide(plateau, (x, y), joueur) or coup_valide(plateau, (x, y), joueur * -1):
                return 0, False
            if case == N:
                compteur_n += 1
            elif case == B:
                compteur_b += 1
    if compteur_b > compteur_n:
        return B, abs(compteur_n - compteur_b) > 10
    elif compteur_n > compteur_b:
        return N, abs(compteur_n - compteur_b) > 10
    else:
        return None, False


def explore(plateau: list, case: tuple, direction: tuple):
    """
    Explore une direction à partir d'une case pour
    :param list plateau: Liste contenant le plateau.
    :param tuple case: Coordonées de la case.
    :param tuple direction: Direction de la vérification.
    :return list: Liste des cases.

    >>> explore([[V, B, B, V], \
                 [B, N, N, B], \
                 [B, N, N, B], \
                 [V, B, B, N]], (0, 0), (1, 1))
    [0, 0, 0]
    """
    resulat = []
    x_case, y_case = case[0] + direction[0], case[1] + direction[1]

    explorer = True
    while explorer:
        if 0 <= x_case < len(plateau) and 0 <= y_case < len(plateau) and (
                plateau[y_case][x_case] == B or plateau[y_case][x_case] == N):
            resulat.append(plateau[y_case][x_case])
            x_case += direction[0]
            y_case += direction[1]
        else:
            explorer = False

    return resulat


def coup_valide(plateau: list, case: tuple, joueur: int):
    """
    Détermine si un coup est autorisé.
    :param list plateau: Liste contenant le plateau.
    :param tuple case: Coordonées de la case.
    :param int joueur: Numéro du joueur.
    :return bool: Le coup est autorisé.

    >>> coup_valide([[V, B, B, V], \
                     [B, N, N, B], \
                     [B, N, N, B], \
                     [V, B, B, V]], (0, 0), N)
    False
    """
    if plateau[case[1]][case[0]] != V and plateau[case[1]][case[0]] != C:
        return False
    for direction in DIRECTIONS:
        ligne = explore(plateau, case, direction)
        if len(ligne) == 0:
            continue
        if ligne[0] == abs(joueur - 1) and joueur in ligne:
            return True
    return False


def retournement(plateau: list, case: tuple, pions: list, joueur: int, direction: tuple):
    """
    Retourne les pions nécessaires.
    :param list plateau: Liste contenant le plateau.
    :param tuple case: Coordonée de la case.
    :param tuple pions: Liste de coordonées des pions à retourner.
    :param int joueur: Numéro du joueur.
    :param tuple direction: Direction de la ligne.
    """
    x, y = case
    for pion in pions:
        x += direction[0]
        y += direction[1]
        if joueur not in pions:
            return
        if pion == joueur or pion == V:
            break
        elif pion == abs(joueur - 1):
            plateau[y][x] = joueur


def sauvegarder(plateau: list, joueur: int, nom_fichier: str):
    """
    Sauvegarde la partie actuelle dans un fichier.
    :param list plateau: Liste contenant le plateau.
    :param int joueur: Joueur actuel.
    :param str nom_fichier: Nom de la sauvegarde à écraser.
    """
    if nom_fichier is None:
        nom_fichier = datetime.datetime.now().strftime("%d-%m-%Y %H-%M") + ".rsi"
    fichier = open(nom_fichier, "w")

    fichier.write(str(joueur))
    for ligne in plateau:
        fichier.write("\n")
        for case in ligne:
            fichier.write(str(case))
    fichier.close()


def affiche_victoire(gagnant: int, ecrasante: bool):
    """
    Affiche le message de fin de partie.
    :param int gagnant: Numéro du joueur gagnant.
    :param bool ecrasante: Victoire avec plus de 10 pions d'avance.
    """
    if gagnant is None:
        rectangle(0, len(plateau) * TAILLE_CASE, len(plateau) * TAILLE_CASE,
                  len(plateau) * TAILLE_CASE + regles['taille_barre'], remplissage="white")
        texte(10, 10 + len(plateau) * TAILLE_CASE, "Égalité !")
    elif gagnant == N:
        rectangle(0, len(plateau) * TAILLE_CASE, len(plateau) * TAILLE_CASE,
                  len(plateau) * TAILLE_CASE + regles['taille_barre'], remplissage="black")
        texte(10, 10 + len(plateau) * TAILLE_CASE,
              "Victoire " + ("écrasante " if ecrasante else "") + "des noirs !",
              couleur="white")
    elif gagnant == B:
        rectangle(0, len(plateau) * TAILLE_CASE, len(plateau) * TAILLE_CASE,
                  len(plateau) * TAILLE_CASE + regles['taille_barre'], remplissage="white")
        texte(10, 10 + len(plateau) * TAILLE_CASE,
              "Victoire " + ("écrasante " if ecrasante else "") + "des blancs !")


def dessine_menu(regles: dict, boutons: dict):
    """
    Dessine le menu principal et modifie les variables de jeu.
    :param dict regles: Variables de jeu.
    :param dict boutons: Dictionnaire ou ajouter les coordonnées des boutons.
    """
    efface_tout()
    image(TAILLE_PLATEAU * TAILLE_CASE // 2, TAILLE_PLATEAU * TAILLE_CASE // 2, "background.gif", ancrage='center')
    texte(TAILLE_PLATEAU * TAILLE_CASE // 2, TAILLE_CASE, "REVERSI", taille=50, couleur="black", ancrage='n')

    boutons["nouvelle_partie"] = \
        dessine_bouton(TAILLE_PLATEAU * TAILLE_CASE // 2, 3 * TAILLE_CASE, "Nouvelle partie", ancrage='center',
                       largeur="Afficher les coups disponibles")
    boutons["charger_partie"] = \
        dessine_bouton(TAILLE_PLATEAU * TAILLE_CASE // 2, 4 * TAILLE_CASE, "Charger une partie", ancrage='center',
                       largeur="Afficher les coups disponibles")
    boutons["afficher_coups"] = \
        dessine_bouton(TAILLE_PLATEAU * TAILLE_CASE // 2, 5 * TAILLE_CASE, "Afficher les coups disponibles",
                       ancrage='center', largeur="Afficher les coups disponibles",
                       couleur="green" if regles["afficher_coups"] else "red")
    boutons["quitter"] = dessine_bouton(TAILLE_PLATEAU * TAILLE_CASE // 2, 7 * TAILLE_CASE, "Quitter", ancrage='center')


def clone(plateau: list):
    """
    Retourne un clone du plateau.
    :param plateau: Plateau à cloner.
    :return: Plateau cloné.

    >>> clone([[1, 1, 1], \
               [1, 1, 1], \
               [1, 1, 1]])
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    """
    clone_plateau = []
    for list in plateau:
        clone_plateau.append(list.copy())
    return clone_plateau


regles = {'joueur': N,
          'nouvelle_partie': True,
          'afficher_coups': False,
          'sauvegarde': None}
ex_plateau = None
boutons = {}

if __name__ == "__main__":

    cree_fenetre(0, 0)
    regles['taille_barre'] = taille_texte('X')[1] - taille_texte('X')[1] % 5 + 20
    ferme_fenetre()

    testmod()
    cree_fenetre(TAILLE_PLATEAU * TAILLE_CASE, TAILLE_PLATEAU * TAILLE_CASE + regles['taille_barre'])

    menu = True
    while menu:
        dessine_menu(regles, boutons)
        x, y = attend_clic_gauche()

        for bouton in boutons:
            if int(boutons[bouton][0]) <= x <= int(boutons[bouton][2]) and \
                    int(boutons[bouton][1]) <= y <= int(boutons[bouton][3]):
                if bouton == "nouvelle_partie":
                    menu = False
                elif bouton == "charger_partie":
                    regles['nouvelle_partie'] = False
                    menu = False
                elif bouton == "afficher_coups":
                    regles['afficher_coups'] = not regles['afficher_coups']
                    break
                elif bouton == "quitter":
                    sys.exit()

    if regles['nouvelle_partie']:

        regles['joueur'] = N
        plateau = init_plateau(TAILLE_PLATEAU)

        plateau[TAILLE_PLATEAU // 2 - 1][TAILLE_PLATEAU // 2 - 1] = B
        plateau[TAILLE_PLATEAU // 2][TAILLE_PLATEAU // 2] = B
        plateau[TAILLE_PLATEAU // 2 - 1][TAILLE_PLATEAU // 2] = N
        plateau[TAILLE_PLATEAU // 2][TAILLE_PLATEAU // 2 - 1] = N

    else:

        nom_fichier = input("Entrer le nom du fichier de sauvegarde : ")

        fichier = open(nom_fichier, "r")
        lignes = fichier.readlines()
        regles['joueur'] = int(lignes[0])

        plateau = []
        for i in range(TAILLE_PLATEAU):
            ligne = []
            for case in lignes[i + 1].strip():
                if case == str(B) or case == str(N):
                    ligne.append(int(case))
                else:
                    ligne.append(case)
            plateau.append(ligne)

        regles['afficher_coups'] = False
        for ligne in plateau:
            if C in ligne:
                regles['afficher_coups'] = True
                break

        fichier.close()
        regles['sauvegarde'] = nom_fichier

    gagnant = None
    ecrasante = False

    # BOUCLE PRINCIPALE
    while True:

        coups_dispo = chercher_coups(plateau, regles['joueur'])

        if regles['afficher_coups']:
            for case in coups_dispo:
                plateau[case[1]][case[0]] = C

        dessine_plateau(plateau, ex_plateau, boutons, regles['joueur'])

        if verifier_victoire(plateau, regles['joueur'])[0] != 0:
            gagnant, ecrasante = verifier_victoire(plateau, regles['joueur'])
            break

        if len(coups_dispo) == 0:
            rectangle(0, len(plateau) * TAILLE_CASE, len(plateau) * TAILLE_CASE,
                      len(plateau) * TAILLE_CASE + regles['taille_barre'], remplissage="white")
            texte(10, 10 + len(plateau) * TAILLE_CASE, "Les " + (
                "blancs" if regles['joueur'] == B else "noirs") + " ne peuvent pas jouer, ils passent leur tour.")
            mise_a_jour()
            attente(3)
            regles['joueur'] = abs(regles['joueur'] - 1)
            continue

        x, y = attend_clic_gauche()

        if boutons["quitter"][0] <= x <= boutons["quitter"][2] and boutons["quitter"][1] <= y <= boutons["quitter"][3]:
            sauvegarder(plateau, regles['joueur'], regles['sauvegarde'])
            sys.exit()
        if "annuler" in boutons:
            if boutons["annuler"][0] <= x <= boutons["annuler"][2] and \
                    boutons["annuler"][1] <= y <= boutons["annuler"][3]:
                regles['joueur'] = abs(regles['joueur'] - 1)
                plateau = clone(ex_plateau)
                ex_plateau = None
                continue

        for case in coups_dispo:
            plateau[case[1]][case[0]] = V

        x_case, y_case = pixel_vers_case((x, y), TAILLE_CASE)

        if pixel_vers_case((x, y), TAILLE_CASE) not in coups_dispo:
            continue

        ex_plateau = clone(plateau)
        plateau[y_case][x_case] = regles['joueur']

        for direction in DIRECTIONS:
            ligne = explore(plateau, (x_case, y_case), direction)
            retournement(plateau, (x_case, y_case), ligne, regles['joueur'], direction)

        regles['joueur'] = abs(regles['joueur'] - 1)

    affiche_victoire(gagnant, ecrasante)
    attend_fermeture()