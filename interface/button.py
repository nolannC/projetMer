# Bibliothèques
import pygame


# création d'une classe Butto
class Button:
    def __init__(self, x, y, w, h, radius=0, color=(255, 255, 255), text=None, textColor=(255, 255, 255)):
        """
        Constructeur du bouton
        :param x: int, position x
        :param y: int, position y
        :param w: int, largeur bouton
        :param h: int, hauteur bouton
        :param radius: int, radius du bouton
        :param color: tuple / list, couleur du bouton
        :param text: str, texte à afficher
        :param textColor: tuple / list, couleur du texte
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.radius = radius
        self.color = color
        self.textStr = text
        self.textColor = textColor
        self.hovered = False
        # la couleur de survol est la couleur par défaut plus foncé
        self.hoveredColor = []
        for i in range(len(self.color)):
            if self.color[i]-50 >= 0:
                self.hoveredColor.append(self.color[i]-50)
            else:
                self.hoveredColor.append(0)
        # s'il y a du texte
        if text is not None:
            # initialisation de la police
            self.font = pygame.font.Font('freesansbold.ttf', 20)
            # rendu du texte
            self.text = self.font.render(self.textStr, True, self.textColor)

    def set_pos(self, x=0, y=0, w=0, h=0):
        """
        Modification de la position du bouton
        :param x: int, position x
        :param y: int, position y
        :param w: int, largeur bouton
        :param h: int, hauteur du bouton
        :return:
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, screen):
        """
        Méthode pour afficher le bouton et son texte
        :param screen: Surface, surface à afficher
        :return:
        """
        # affichage du rectangle
        if self.hovered:
            pygame.draw.rect(screen, self.hoveredColor, (self.x, self.y, self.w, self.h), border_radius=self.radius)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), border_radius=self.radius)
        # si le texte à afficher existe
        if self.textStr is not None:
            # affichage du texte
            screen.blit(self.text, (self.text.get_rect().x + self.w / 2 + self.x - self.text.get_rect().w /
                        2, self.text.get_rect().y + self.h / 2 + self.y - self.text.get_rect().h / 2))

    def click(self, position):
        """
        Méthode pour vérifier si le bouton est cliqué
        :param position: tuple / list, position de la souris
        :return: bool, True si cliqué, False sinon
        """
        # position de la souris
        x = position[0]
        y = position[1]
        # si la souris est sur le bouton
        if (self.x < x < self.x + self.w) and (self.y < y < self.y + self.h):
            return True
        else:
            return False
    
    def hover(self, position):
        """
        Méthode qui permet de vérifier si la souris est sur ce bouton
        :param position: tuple, position de la souris
        :return: bool, True si survolé, False sinon
        """
        x = position[0]
        y = position[1]
        if (self.x < x < self.x + self.w) and (self.y < y < self.y + self.h):
            self.hovered = True
        else:
            self.hovered = False

