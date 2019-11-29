class QuoridorError(Exception):
    pass



class Quoridor:

    def __init__(self, joueurs, murs=None):

        # Erreurs à soulever:
        if not isinstance(joueurs, iter):
            raise QuoridorError("'joueurs' doit être un itérable")
        elif len(joueurs) > 2:
            raise QuoridorError("seulement 2 joueurs acceptés")

        if isinstance(joueurs[0], str) and isinstance(joueurs[1], str):
            self.joueurs = [{nom: joueurs[0], murs: 10, pos: (5, 1)}, 
                            {nom: joueurs[1], murs: 10, pos: (5, 9)}]
            self.murs = {horizontaux: [], verticaux: []}

        elif isinstance(joueurs[0], dict) and isinstance(joueurs[1], dict):
            self.joueurs = joueurs


        
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés, 
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        :param joueurs: un itérable de deux joueurs dont le premier est toujours celui qui 
        débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire. 
        Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans 
        l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut initialement
        placer 10 murs. Dans le cas où l'argument est un dictionnaire, celui-ci doit contenir 
        une clé 'nom' identifiant le joueur, une clé 'murs' spécifiant le nombre de murs qu'il 
        peut encore placer, et une clé 'pos' qui spécifie sa position (x, y) actuelle.
        
        :param murs: un dictionnaire contenant une clé 'horizontaux' associée à la liste des
        positions (x, y) des murs horizontaux, et une clé 'verticaux' associée à la liste des
        positions (x, y) des murs verticaux. Par défaut, il n'y a aucun mur placé sur le jeu.

        - :raises QuoridorError: si l'argument 'joueurs' n'est pas itérable. 
        - :raises QuoridorError: si l'itérable de joueurs en contient plus de deux.
        :raises QuoridorError: si le nombre de murs qu'un joueur peut placer est >10, ou négatif.
        :raises QuoridorError: si la position d'un joueur est invalide.
        :raises QuoridorError: si l'argument 'murs' n'est pas un dictionnaire lorsque présent.
        :raises QuoridorError: si le total des murs placés et plaçables n'est pas égal à 20.
        :raises QuoridorError: si la position d'un mur est invalide.
        """

    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie. 
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """
        nom1 = dic['état']['joueurs'][0]['nom']
        damier = ''
        pligne = f'Légende: 1 = {nom1}, 2 = automate \n' + '   ' + 35*'-' + '\n'
        for i in range(9, 0, -1):
            if i != 1:
                damier += f'{i}' +  ' | .' + 8*'   .' + ' |' '\n' + '  |' + 35* ' ' + '| \n'
            elif i == 1:
                damier += f'{i}' +  ' | .' + 8*'   .' + ' |' '\n'
        damier += '--|' + 35*'-' + '\n'
        dligne = '  | '
        for i in range(1, 10):
            if i != 9:
                dligne += f'{i}' + 3*' '
            elif i == 9:
                dligne += '9'
        damier += dligne
        damier = list(damier.splitlines())
        for i in range(len(damier)):
            damier[i] = list(damier[i])
        
        ### bonhommes

        x1 = dic['état']["joueurs"][0]["pos"][0]
        y1 = dic['état']["joueurs"][0]["pos"][1]
        x2 = dic['état']["joueurs"][1]["pos"][0]
        y2 = dic['état']["joueurs"][1]["pos"][1]

        damier[18-2*y1][4*x1] = '1'
        damier[18-2*y2][4*x2] = '2'

        ### murs horizontaux

        for i in range(len(dic['état']["murs"]["horizontaux"])):
            xh = dic['état']["murs"]["horizontaux"][i][0]
            yh = dic['état']["murs"]["horizontaux"][i][1]
            damier[19-2*yh][4*xh-1 : 4*xh+6] = '-------'

        ### murs verticaux

        for i in  range(len(dic['état']["murs"]["verticaux"])):
            xv = dic['état']["murs"]["verticaux"][i][0]
            yv = dic['état']["murs"]["verticaux"][i][1]
            damier[18-2*yv][4*xv-2] = '|'
            damier[17-2*yv][4*xv-2] = '|'
            damier[16-2*yv][4*xv-2] = '|'

        return(pligne + '\n'.join(''.join(i for i in ligne) for ligne in damier) + '\n')

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
        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
        {
            'joueurs': [
                {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
            ],
            'murs': {
                'horizontaux': [...],
                'verticaux': [...],
            }
        }
        
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

    def placer_mur(self, joueur, position, orientation):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.

        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du mur.
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si un mur occupe déjà cette position.
        :raises QuoridorError: si la position est invalide pour cette orientation.
        :raises QuoridorError: si le joueur a déjà placé tous ses murs.
        """