'''
Projet servant à suivre une partie et avoir une fonction
déterminant le meilleur coup possible
'''
import networkx as nx
import unittest
import copy


### Pour le Graphe, pas touche!
def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.
    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0], 2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)

            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe


class Quoridor:

    def __init__(self, joueurs, murs=None):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie. 
<<<<<<< HEAD
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """

=======
        """  
        if not isinstance(joueurs, iter):
            raise QuoridorError("'joueurs' doit être un itérable")
        elif len(joueurs) > 2:
            raise QuoridorError("seulement 2 joueurs acceptés")
        
>>>>>>> 0b50a22288a55c6fede60a39fefca8e4edc5372d
        if isinstance(joueurs[0], str) and isinstance(joueurs[1], str):
            self.joueurs = [{nom: joueurs[0], murs: 10, pos: (5, 1)}, 
                            {nom: joueurs[1], murs: 10, pos: (5, 9)}]
            self.murs = {horizontaux: [], verticaux: []}

        elif isinstance(joueurs[0], dict) and isinstance(joueurs[1], dict):
            self.joueurs = joueurs

    def __str__(self):

        dico = self.état['joueurs'][0]

        legende = 'Légende: 1: ' + self.nom_joueur1 +  ' 2:' + self.nom_joueur2 + '\n'
        top = ' '*3 + '-'*35 + ' \n'
        temp_middle = []
        empty_mid_section = ' '*2 + '|' + ' '.join(['   ']*9) + '|\n'

        for i in list(range(1, 10))[::-1]:
            temp_middle.append(f'{i} |' + ' '.join([' . ']*9) + '|\n')

        middle = empty_mid_section.join(temp_middle)
        bot = '--|' + '-'*35 + ' \n'
        bot += '  | ' + '   '.join([f'{i}' for i in range(1, 10)])
        board = ''.join([legende, top, middle, bot])

        #Mettre le damier en liste
        board_split = [list(ligne) for ligne in board.split('\n')]

        #PLACER JOUEUR
        #position  joueur 1
        for position in range(1):
            self.position_X_j1, self.position_Y_j1 = dico["joueurs"][0]['pos']
            board_split[-2*self.position_Y_j1+20][self.position_X_j1*4] = '1'

        #position joueur 2
        for position in range(1):
            self.position_X_j2, self.position_Y_j2 = dico["joueurs"][1]['pos']
            board_split[-2*self.position_Y_j2+20][self.position_X_j2*4] = '2'

        #PLACER MURS
        #placer murs horizontaux
        for placement in range(len(dico["murs"]["horizontaux"])):
            x, y = dico["murs"]["horizontaux"][placement]
            for variable in range(7):
                board_split[-2*y+21][4*x-1+variable] = '-'

        #placer murs verticaux
        for placement in range(len(dico["murs"]["verticaux"])):
            x, y = dico["murs"]["verticaux"][placement]
            for variable in range(3):
                board_split[-2*y+18+variable][4*x-2] = '|'

        #Remettre le damier en str
        rep = '\n'.join([''.join(elem) for elem in board_split])
        print(rep)

    def déplacer_jeton(self, joueur, position):
            """
            Pour le joueur spécifié, déplacer son jeton à la position spécifiée.
            :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
            :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
            :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
            :raises QuoridorError: si la position est invalide (en dehors du damier).
            :raises QuoridorError: si la position est invalide pour l'état actuel du jeu.
            """

    def état_partie(self):
        """Cette fonction produit/retourne l'état actuel de la partie"""
        état_jeu = {
            'joueurs': [
                {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
            ],
            'murs': {
                'horizontaux': [...],
                'verticaux': [...],
            }
        }

        état_jeu2 = copy.deepcopy(état_jeu)

        return état_jeu2

        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
    
        où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée 
        au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est 
        associée à sa position sur le damier. Une position est représentée par un tuple 
        de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

        Les murs actuellement placés sur le damier sont énumérés dans deux listes de
        positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
        est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
        situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
        mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel 
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un 
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la partie est déjà terminée.
        """

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.
        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        if self.position_Y_j1 >= 10:
            return f'{self.nom_joueur1}'
        if self.position_Y_j2 <= 0:
            return f'{self.nom_joueur2}'
        else:
            return False
    def placer_mur(self, joueur, position, orientation):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.
        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du mur.
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si un mur occupe déjà cette position.
        :raises QuoridorError: si la position est invalide pour cette orientation.
        :raises QuoridorError: si le joueur a déjà placé tous ses murs."""


### Pour que l'erreur existe
class QuoridorError(Exception, Quoridor):
        
        # Erreurs à soulever:
        def __init__(self, joueurs, murs = None):
            if not isinstance(joueurs, iter):
                raise QuoridorError("'joueurs' doit être un itérable")
            elif len(joueurs) > 2:
                raise QuoridorError("seulement 2 joueurs acceptés")
