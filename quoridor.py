'''
Projet servant à suivre une partie et avoir une fonction
déterminant le meilleur coup possible
'''
import networkx as nx


class QuoridorError(Exception):
    '''Pour que l'erreur existe'''


### Pour le Graphe, pas touche!
def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.
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
    '''Classe permettant à de jouer à Quorridor'''

    def __init__(self, joueurs, graphe, état, murs=None):
        """Méthode d'initiation"""

        if not isinstance(joueurs, iter):
            raise QuoridorError("'joueurs' doit être un itérable")
        elif len(joueurs) > 2:
            raise QuoridorError("seulement 2 joueurs acceptés")
        elif isinstance(joueurs[0], str) and isinstance(joueurs[1], str):
            self.joueurs = [{'nom': joueurs[0], 'murs': 10, 'pos': (5, 1)},
                            {'nom': joueurs[1], 'murs': 10, 'pos': (5, 9)}]
            self.murs = {'horizontaux': [], 'verticaux': []}

        elif isinstance(joueurs[0], dict) and isinstance(joueurs[1], dict):

            if joueurs['joueurs'][0]['murs'] or joueurs['joueurs'][0]['murs'] < 0 or joueurs['joueurs'][0]['murs'] 
                or joueurs['joueurs'][0]['murs'] > 10:
                raise QuoridorError('nombre de murs invalide')

            elif joueurs['joueurs'][0]['pos'][0] or joueurs['joueurs'][0]['pos'][1] or joueurs['joueurs'][1]['pos'][0]
                or joueurs['joueurs'][1]['pos'][1] < 0 or joueurs['joueurs'][0]['pos'][0] or joueurs['joueurs'][0]['pos'][1]
                or joueurs['joueurs'][1]['pos'][0] or joueurs['joueurs'][1]['pos'][1] > 9:
                raise QuoridorError('postion(s) invalide(s)')

            elif not isinstance(murs, dict):
                raise QuoridorError("l'argument 'murs' n'est pas un dictionnaire")

            elif joueurs['joueurs'][0]['murs'] + joueurs['joueurs'][1]['murs'] + len(joueurs['murs']['horizontaux']) +
                len(joueurs['murs']['verticaux']) != 20:
                raise QuoridorError("le total des murs placés et plaçables n'est pas égal à 20")

            for i in murs['horizontaux']:
                if 1 > i[0] > 8 or 2 > i[1] > 9:
                    raise QuoridorError("la position d'un mur est invalide")

            for i in murs['verticaux']:
                if 2 > i[0] > 9 or 1 > i[1] > 8:
                    raise QuoridorError("la position d'un mur est invalide")
            self.joueurs = joueurs
            self.murs = murs
            self.état = état
            self.graphe = graphe

    def __str__(self):
        '''Fonction qui donne le damier de jeu'''
        def afficher_damier_ascii(dico):
            legende = 'Légende: 1: ' + idul +  ' 2:automate' + '\n'

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
                x, y = dico["joueurs"][0]['pos']
                board_split[-2*y+20][x*4] = '1'

            #position joueur 2
            for position in range(1):
                x, y = dico["joueurs"][1]['pos']
                board_split[-2*y+20][x*4] = '2'

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


        afficher_damier_ascii(self.état_partie())

    def déplacer_jeton(self, joueur, position):
        '''Méthode qui détermine les déplacements possibles'''

        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in état['joueurs']],
            état['murs']['horizontaux'],
            état['murs']['verticaux'])

        # On doit s'assurer que le nombre qui représente le joueur est valide, que la position existe et est accessible
        if joueur in {1, 2}:
            if 0 < position[0] < 10 and 0 < position[1] < 10:
                if position in list(self.graphe.successors(self.joueurs[joueur - 1]['pos'])):
                    self.joueurs[joueur - 1]['pos'] = position
                else:
                    raise QuoridorError("Cette case n'est pas accessible")
            else:
                raise QuoridorError("Cette case n'existe pas")
        else:
            raise QuoridorError('Le numéro du joueur doit être 1 ou 2')

    def état_partie(self):
        """Cette fonction produit/retourne l'état actuel de la partie"""
        for i in range(1):
            position = self.joueurs[i]['pos']
            for pos in position:
                if not 1 <= pos <= 9:
                    raise QuoridorError("Position out of range")
        self.état = {'joueurs': self.joueurs, 'murs': self.murs}
        return self.état

    def jouer_coup(self, joueur):
        """Fonction qui détermine le meileur coup possible"""
        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in état['joueurs']],
            self.état['murs']['horizontaux'],
            self.état['murs']['verticaux'])
        # On trouve le chemin le plus court et se déplace dans cette direction
        if joueur in {1, 2}:
            path = nx.shortest_path(self.graphe, self.joueurs[joueur-1]['pos'], f'B{joueur}')
            if self.partie_terminée() is False:
                self.déplacer_jeton(joueur, chemin[1])
            else:
                raise QuoridorError('La partie est terminée')
        else:
            raise QuoridorError('Le numéro du joueur doit être 1 ou 2')

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.
        if self.état['joueurs'][0]['pos'][1] == 9:
            return f'{self.état['joueurs'][0]['nom']}'
        if self.état['joueurs'][1]['pos'][1] == 1:
            return f'{self.état["joueurs"][1]['nom']}'
        else:
            return False"""

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
