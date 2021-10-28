# Bibliothèques
import pygame
import time


# Création d'une classe Input
class Input:
    def __init__(self, x, y, w, h, radius, color, width, textStr, textColor, active=False, backgroundColor=(0, 0, 0)):
        """
        Constructeur de l'input
        :param x: int, position x
        :param y: int, position y
        :param w: int, largeur bouton
        :param h: int, hauteur bouton
        :param radius: int, radius du bouton
        :param color: tuple / list, couleur du bouton
        :param width: taille du contour de l'input
        :param textStr: str, texte à afficher
        :param textColor: tuple / list, couleur du texte
        :param active: si l'input est déjà actif
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.radius = radius
        self.color = color
        self.width = width
        self.textStr = textStr
        self.textColor = textColor
        self.active = active
        self.backgroundColor = backgroundColor
        # rendu de l'input
        self.input = None
        # rendu du texte de
        self.text = None
        # valeur de l'input (ce que l'utilisateur entre)
        self.inputStr = ""
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def set_pos(self, x=0, y=0, w=0, h=0):
        """
        Méthode pour repositionner l'input
        :param x: int, position x
        :param y: int, position y
        :param w: int, largeur de l'input
        :param h: int, hauteur de l'input
        :return:
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, screen):
        """
        Méthode pour dessiner l'input sur screen
        :param screen: Surface, surface sur laquelle afficher l'input
        :return:
        """
        # dessiner le rectangle de l'input
        pygame.draw.rect(screen, self.backgroundColor, (self.x, self.y, self.w, self.h), border_radius=self.radius)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), width=self.width, border_radius=self.radius)
        # s'il y a du texte par défaut, que l'input n'est pas actif et qu'il est vide
        if self.textStr is not None and not self.active and self.inputStr == "":
            # rendu du texte
            self.text = self.font.render(self.textStr, True, self.textColor)
            # affichage du texte
            screen.blit(self.text, (self.text.get_rect().x + self.x + 10,
                        self.text.get_rect().y + self.h / 2 + self.y - self.text.get_rect().h / 2))
        # afficher l'input
        self.input = self.font.render(self.inputStr, True, self.textColor)
        screen.blit(self.input, (self.input.get_rect().x + self.x + 10,
                                 self.input.get_rect().y + self.h / 2 + self.y - self.input.get_rect().h / 2))
        # si l'input est actif
        if self.active:
            # affichage 1 seconde sur 2 d'un '_' devant l'input
            if int(time.time() % 2) == 0:
                # afficher le '_'
                screen.blit(self.font.render("_", True, self.textColor), (self.x + self.input.get_rect().width +
                            10, self.input.get_rect().y + self.h / 2 + self.y - self.input.get_rect().h / 2))

    def click(self, position):
        """
        Méthode pour vérifier si le bouton est cliqué
        :param position: tuple / list, position de la souris
        :return: bool, True si cliqué, False sinon
        """
        x = position[0]
        y = position[1]
        # si on clique sur l'input
        if (self.x < x < self.x + self.w) and (self.y < y < self.y + self.h):
            self.active = True
            return True
        else:
            self.active = False
            return False

    def write(self, event):
        # écriture de l'input s'il est actif
        if self.active:
            # '\x08' => supprimer
            if event.unicode == '\x08':
                # enlever la dernière chaine de caractère
                self.inputStr = self.inputStr[0:-1]
            else:
                # ajouter les autres caractères
                self.inputStr += event.unicode
