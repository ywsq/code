import pygame
import sys

largeur, hauteur = 800, 800
fenetre = pygame.display.set_mode((largeur, hauteur))
TAILLE_CASE = 100
MARGE = 50

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROSE = (237, 170, 200)

class ChessPiece:
    def __init__(self, image, position):
        self.image = image
        self.position = position

class ChessBoard:
    def __init__(self, width, height, taille_case, marge):
        self.width = width
        self.height = height
        self.taille_case = taille_case
        self.marge = marge
        self.pieces = []
        self.creer_pieces()

    def creer_pieces(self):
        # creer des listes des positions et des listes des images pour les joueurs A et B
        pieces_positions_A = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7)]
        pieces_images_A = [tour_image,cavalier_image,fou_image,dame_image,roi_image,fou_image,cavalier_image,tour_image]
        pieces_positions_B = [(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)]
        pieces_images_B = [tour_image,cavalier_image,fou_image,dame_image,roi_image,fou_image,cavalier_image,tour_image]

        # Placer les 8 pieces des joueurs A et B
        for i in range(8):
            piece_A = ChessPiece(pieces_images_A[i], pieces_positions_A[i])
            self.ajouter_pion(piece_A)
            piece_B = ChessPiece(pieces_images_B[i], pieces_positions_B[i])
            self.ajouter_pion(piece_B)
        # Placer les pions des joueurs A et B
        for i in range(8):
            pion_A = ChessPiece(pion_image,(1,i))
            self.ajouter_pion(pion_A)
            pion_B = ChessPiece(pion_image,(6,i))
            self.ajouter_pion(pion_B)



    def ajouter_pion(self, piece):
        self.pieces.append(piece)

    def dessiner_plateau(self):
        for i in range(8):
            for j in range(8):
                couleur = BLANC if (i + j) % 2 == 0 else ROSE
                pygame.draw.rect(fenetre, couleur, (j * TAILLE_CASE, i * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

    def dessiner_pions(self):
        for piece in self.pieces:
            x = piece.position[1] * TAILLE_CASE + MARGE - 50 + (TAILLE_CASE - piece.image.get_width()) // 2
            y = piece.position[0] * TAILLE_CASE + MARGE - 50 + (TAILLE_CASE - piece.image.get_height()) // 2
            fenetre.blit(piece.image, (x, y))
class ChessGame:
    def __init__(self):
        self.largeur, self.hauteur = 800, 800
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        self.board = ChessBoard(self.largeur, self.hauteur, TAILLE_CASE, MARGE)

    def run(self):

        # Dessiner l'echiquier des le lancement
        self.fenetre.fill(BLANC)
        self.board.dessiner_plateau()
        self.board.dessiner_pions()  # Appel pour dessiner les pièces
        pygame.display.flip()

        en_cours = True
        pion_selectionne = None  # stocker la piece selectionnee


        jouabilite = 0
        while jouabilite != "2" and jouabilite != "1":
            jouabilite = input("Choisissez votre mode de jouabilité, tapez le numéro 1 (Souris) ou 2 (Terminal) :")

        if jouabilite == "1":
            jouabilite = "souris"
        elif jouabilite == "2":
            jouabilite = "terminal"
        if jouabilite == "souris":
            while en_cours:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        en_cours = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        for piece in self.board.pieces:
                            center_x = piece.position[1] * TAILLE_CASE + MARGE - 50 + TAILLE_CASE / 2
                            center_y = piece.position[0] * TAILLE_CASE + MARGE - 50 + TAILLE_CASE / 2

                            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5

                            if distance <= TAILLE_CASE / 2:
                                pion_selectionne = piece
                                break
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if pion_selectionne:
                            x, y = pygame.mouse.get_pos()
                            x -= MARGE - 50
                            y -= MARGE - 50
                            nouvelle_position = (y // TAILLE_CASE, x // TAILLE_CASE)

                            # Vérifie s'il y a déjà une pièce à la nouvelle position
                            for piece in self.board.pieces:
                                if piece.position == nouvelle_position:
                                    self.board.pieces.remove(piece)  # Supprime la pièce existante

                            pion_selectionne.position = nouvelle_position  # Mise à jour de la position
                            pion_selectionne = None  # Réinitialisation de la pièce sélectionnée

                # Effacer l'écran
                self.fenetre.fill(BLANC)
                self.board.dessiner_plateau()
                self.board.dessiner_pions()  # Appel pour dessiner les pièces
                pygame.display.flip()
                            
        elif jouabilite == "terminal":
            while en_cours:
                # Demande à l'utilisateur de fournir la position de la pièce à déplacer
                user_input = input("Entrez la position de la pièce à déplacer (ligne colonne) : ")

                # Convertit la saisie de l'utilisateur en une paire de coordonnées (ligne, colonne)
                coordonnees = user_input.split()  # Sépare la saisie en une liste de valeurs
                ligne = int(coordonnees[0])  # Prend la première valeur comme numéro de ligne
                colonne = int(coordonnees[1])  # Prend la deuxième valeur comme numéro de colonne
                position = (ligne, colonne)  # Crée un tuple avec les coordonnées (ligne, colonne)

                # Recherche de la pièce à la position spécifiée dans la liste des pièces sur l'échiquier
                selected_piece = None
                for piece in self.board.pieces:
                    if piece.position == position:  # Vérifie si la position de la pièce correspond à la saisie de l'utilisateur
                        selected_piece = piece  # Si la pièce est trouvée, elle est assignée à selected_piece
                        break  # Arrête la recherche dès qu'une pièce est trouvée

                if selected_piece:  # Vérifie si une pièce a été trouvée à la position spécifiée
                    # Demande à l'utilisateur de fournir la nouvelle position pour déplacer la pièce
                    new_position_input = input("Entrez la nouvelle position (ligne colonne) : ")

                    # Convertit la nouvelle saisie de l'utilisateur en une paire de coordonnées (ligne, colonne)
                    new_coordonnees = new_position_input.split()  # Sépare la nouvelle saisie en une liste de valeurs
                    new_ligne = int(new_coordonnees[0])  # Prend la première valeur comme nouveau numéro de ligne
                    new_colonne = int(new_coordonnees[1])  # Prend la deuxième valeur comme nouveau numéro de colonne
                    new_position = (new_ligne, new_colonne)  # Crée un tuple avec les nouvelles coordonnées (ligne, colonne)

                    if selected_piece:
                        for piece in self.board.pieces:
                            if piece.position == new_position:
                                self.board.pieces.remove(piece)
                                break

                    # Met à jour la position de la pièce sélectionnée avec la nouvelle position fournie par l'utilisateur
                    selected_piece.position = new_position


                # Effacer l'écran et rafraichissement
                self.fenetre.fill(BLANC)
                self.board.dessiner_plateau()
                self.board.dessiner_pions()  # Appel pour dessiner les pièces
                pygame.display.flip()
            
            """command = input("Entrez la position de la pièce à déplacer (ligne colonne) : ")
            position = tuple(map(int, command.split()))  # Convertit la saisie en coordonnées (ligne, colonne)

            # Recherche de la pièce à la position spécifiée
            selected_piece = None
            for piece in self.board.pieces:
                if piece.position == position:
                    selected_piece = piece
                    break

            if selected_piece:
                new_position = input("Entrez la nouvelle position (ligne colonne) : ")
                new_position = tuple(map(int, new_position.split()))  # Nouvelle position de la pièce
                selected_piece.position = new_position  # Met à jour la position de la pièce"""


        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    pygame.init()
    icon = pygame.image.load("./assets/icon.png")
    pygame.display.set_caption("Jeu Loufoque")
    pygame.display.set_icon(icon)

    # Charger l'image du pion
    pion_image = pygame.image.load("assets/pion.png")
    pion_image = pygame.transform.scale(pion_image, (80, 80))

    roi_image = pygame.image.load("assets/roi.png")
    roi_image = pygame.transform.scale(roi_image, (80, 80))

    dame_image = pygame.image.load("assets/dame.png")
    dame_image = pygame.transform.scale(dame_image, (80, 80))

    tour_image = pygame.image.load("assets/tour.png")
    tour_image = pygame.transform.scale(tour_image, (80, 80))

    fou_image = pygame.image.load("assets/fou.png")
    fou_image = pygame.transform.scale(fou_image, (80, 80))

    cavalier_image = pygame.image.load("assets/cavalier.png")
    cavalier_image = pygame.transform.scale(cavalier_image, (80, 80))


    game = ChessGame()
    game.run()