# Bibliothèques
import pygame
import pyautogui
from button import Button
from input import Input
import sqlite3


def get_info(val):
    """
    Fonction qui renvoie les informations de la ligne qui a pour nom val
    :param val: string, valeur à rechercher
    :return: liste contenant toutes les informations
    """
    infos = []
    # récupérer chaque information de la requete sqlite
    for inf in cur.execute("SELECT * FROM main WHERE nom LIKE \"" + val + "\""):
        # ajouter chaque information à la liste
        infos.append(inf)
    return infos


def set_text(info):
    """
    Fonction qui renvoie le texte à afficher grâce aux informations de info
    ; => permet de séparer le texte en différents morceaux
    & => permet un retour à la ligne
    :param info: list, informations a afficher
    :return: string, avec les informations a afficher
    """
    # modification de l'affichage de l'emplacement
    environnement = ""
    for location in info[8].split(", "):
        environnement += f"      -  {location}&"

    # modification de l'affichage de la réputation
    reputation = ""
    for e, rep in enumerate(info[12].split("; ")):
        if e != len(info[12].split("; ")) - 1:
            reputation += f"{rep},&"
        else:
            reputation += f"{rep}.&"

    # modification de l'affichage de la description
    description = ""
    for e, desc in enumerate(info[13].split("; ")):
        if e != len(info[13].split("; ")) - 1:
            description += f"{desc}&"
        else:
            description += f"{desc}.&"

    # modification de l'affichage de la cause
    cause = ""
    for e, caus in enumerate(info[11].split("; ")):
        if e != len(info[11].split("; ")) - 1:
            cause += f"{caus},&"
        else:
            cause += f"{caus}."

    # afficher il ou elle en fonction de la deuxieme lettre du nom (la, le, l') => (elle, il, il)
    if info[1][1] == "a":
        genre = "Elle"
    else:
        genre = "Il"

    # texte à afficher
    return f"{genre} mesure en moyenne {info[2]} cm, avec un record de {info[3]} cm.&{genre} pèse {info[4]} kg{'' if info[5] == 'Inconnu' else f', au maximum {info[5]} kg'}.& {genre} peut vivre jusqu'à {info[6]} ans.&{genre} se nourrit de {info[7]}.&{info[1]} vit dans : &{environnement} On peut l{'a' if info[1][1] == 'a' else 'e'} retrouver {'à la surface' if info[9] == '0' else f'à {info[9]}m'}, jusqu'à {info[10]} m de profondeur.&Sa réputation est d'être {reputation}Cause de l'attaque : {cause}&Description : {description}"


# initialisation des composants de pygame
pygame.init()

# Fonts
titleFont = pygame.font.Font('freesansbold.ttf', 30)
textFont = pygame.font.Font('freesansbold.ttf', 18)

# création d'un écran redimensionnable, la taille de la fenetre lors de l'ouverture varie en fonction de l'écran de l'utilisateur
screen = pygame.display.set_mode((int(pyautogui.size()[0] * 0.7), int(pyautogui.size()[1] * 0.9)), pygame.RESIZABLE)
# changer le titre de la fenetre
pygame.display.set_caption("Dictionnaire des animaux marins les plus dangereux")

# initialisation des boutons & inputs
searchButton = Button(0, 0, 0, 0, 10, (0, 198, 177), "Envoyer", (255, 255, 255))
searchInput = Input(0, 0, 0, 0, 10, (0, 198, 177), 2, "Recherche", (255, 255, 255), False, (1, 80, 113))
viewButton = Button(0, 0, 0, 0, 10, (0, 198, 177), "Voir le dictionnaire", (255, 255, 255))

# connexion a la base de données
conn = sqlite3.connect("database.db")
# positionner le curseur
cur = conn.cursor()

# récupérer chaque nom de la base de données dans noms
noms = []
for nom in cur.execute("SELECT nom FROM main"):
    noms.append(list(nom)[0])

# récupérer chaque chemin d'image depuis la base de données dans paths
paths = []
for path in cur.execute("SELECT image_path FROM main"):
    paths.append(path[0])

# création de deux dictionnaires contenant les images (pour garder une bonne qualité d'image)
# images contient les images par défaut en 16/9
images = {}
# images_custom contient les images avec une résolution différente
images_custom = {}
for e, nom in enumerate(noms):
    # chargement de l'image
    image = pygame.image.load("assets/" + paths[e])
    # chaque nom à une image associée
    # images par défaut (16/9)
    images[nom] = pygame.transform.scale(image, (int(((screen.get_width()) * 16) / 9), int(screen.get_width())))
    # images qui auront une résolution différente, plus petite (16/9) / 8
    images_custom[nom] = pygame.transform.scale(image, (int(((screen.get_width() / 8) * 16) / 9), int(screen.get_width() / 8)))

# chargement de la fleche de retour
back_arrow = pygame.transform.scale(pygame.image.load("assets/arrowLeft.png"), (100, 100))

# chargement fleche gauche
arrowLeft = pygame.transform.scale(pygame.image.load("assets/arrowLeft.png"), (50, 50))
# chargement fleche droite
arrowRight = pygame.transform.scale(pygame.image.load("assets/arrowRight.png"), (50, 50))
# chargement de la bannière
banner = pygame.transform.scale(pygame.image.load("assets/background_image.jpg"), (1680, 1120))

# si le dictionnaire est en cours de lecture
viewDic = False
# page actuelle
page = 1
# animal actuel
animal = noms[(page - 1) % len(noms)]
# information sur l'animal actuel
info = get_info(animal)[0]
# résultat de la recherche (rien trouvé ou trop)
msg = ""
# liste des boutons (ceux de la recherche)
resultSearchButton = []

# si la fenetre est en cours d'execution
running = True
# tant que la fenetre est ouverte
while running:
    # changer la couleur de fond
    screen.fill((1, 80, 113))
    # afficher le fond d'écran
    screen.blit(banner, (screen.get_width() / 2 - banner.get_width() / 2, screen.get_height() / 2 - banner.get_height() / 2))
    # si l'utilisateur est sur la page d'accueil
    if not viewDic:
        
        # afficher chaque bouton des recherches
        for btn in resultSearchButton:
            btn.hover(pygame.mouse.get_pos())
            btn.draw(screen)

        # affichage du texte
        text = titleFont.render("Espèces animales", True, (0, 0, 0))
        # text = pygame.transform.smoothscale(text, (text.get_width() * screen.get_width() // 1920, text.get_height() * screen.get_height() // 1080))
        screen.blit(text, (screen.get_width() / 2 - text.get_rect().w / 2, screen.get_height() / 12))

        # repositionnement et redimmensionnement du bouton de recherche
        searchButton.set_pos(screen.get_width() / 2 + (searchInput.w * 1) / 3 + 10,
                             int(screen.get_height() * 0.60), screen.get_width() / 8, screen.get_height() / 12)
        # affichage du bouton
        searchButton.hover(pygame.mouse.get_pos())
        searchButton.draw(screen)

        # repositionnement et redimmensionnement de la barre de recherche
        searchInput.set_pos(screen.get_width() / 2 - (searchInput.w * 2) / 3, int(screen.get_height() * 0.60),
                            int(screen.get_width() / 3), screen.get_height() / 12)
        # affichage de la barre de recherche
        searchInput.draw(screen)

        # afficher le résultat de la recherche (par défaut "")
        t = textFont.render(msg, True, (255, 255, 255))
        screen.blit(t, (screen.get_width() / 2 - t.get_width() / 2, int(screen.get_height() * 0.62)))

        # repositionnement et redimmensionnement du bouton de visionnage du dictionnaire
        viewButton.set_pos(screen.get_width() / 2 - viewButton.w / 2, (screen.get_height() * 3) /
                           4, screen.get_width() / 5, screen.get_height() / 12)
        # affichage du bouton de visionnage
        viewButton.hover(pygame.mouse.get_pos())
        viewButton.draw(screen)
    # si le dictionnaire est en cours de lecture
    else:
        # affichage du rectangle bleu clair (ce qui délimite la page)
        pygame.draw.rect(screen, (102, 155, 207), (screen.get_width() / 4, screen.get_height() /
                         8, screen.get_width() / 2, screen.get_height() - screen.get_height() / 5))
        # affichage de la fleche de retour
        screen.blit(back_arrow, (screen.get_width() / 4, screen.get_height() / 8))

        # affichage de la fleche gauche
        screen.blit(arrowLeft, (0, screen.get_height() / 2 - arrowLeft.get_height() / 2))

        # affichage de la fleche droite
        screen.blit(arrowRight, (screen.get_width() - arrowRight.get_width(), screen.get_height() / 2 - arrowLeft.get_height() / 2))

        # affichage du titre (nom de l'animal)
        screen.blit(titleFont.render(info[1], True, (255, 255, 255)), (screen.get_width()
                    / 2 - titleFont.render(info[1], True, (255, 255, 255)).get_rect().centerx, screen.get_height() / 8 + screen.get_height() / 12))
        # affichage de l'image
        screen.blit(images_custom[info[1]], (screen.get_width() / 2 -
                    images_custom[info[1]].get_rect().centerx, screen.get_height() / 4 + screen.get_height() / 20))

        # récupérer le texte à afficher
        text = set_text(info)

        # affichage du texte sous forme de ligne
        for e, word in enumerate(text.split("&")):
            t = textFont.render(word, True, (255, 255, 255))
            screen.blit(t, (screen.get_width() / 4 + screen.get_width() / 64, screen.get_height() / 2 + e * 25))

        # affichage du status de conservation
        statusConservation = textFont.render(info[14], True, (255, 255, 255))
        screen.blit(statusConservation, (screen.get_width() / 4 + screen.get_width() / 2 -
                    statusConservation.get_width() * 2, screen.get_height() / 8 + statusConservation.get_height()))

    # mise a jour de l'ecran
    pygame.display.flip()

    # recuperer tout les evenements
    for event in pygame.event.get():
        # si une touche est enfoncée
        if event.type == pygame.KEYDOWN:
            # si la touche est échap, on arrete le programme
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
            else:
                # si le dictionnaire n'est pas en cours de lecture
                if not viewDic:
                    # écrire dans la barre de recherche
                    searchInput.write(event)
                else:
                    # fleche de gauche
                    if event.key == pygame.K_LEFT:
                        # on affiche la page précédente
                        page -= 1
                        # on récupère les informations de l'animal à afficher
                        info = get_info(noms[(page - 1) % len(noms)])[0]
                    # fleche de droite
                    if event.key == pygame.K_RIGHT:
                        # affichage de la page suivante
                        page += 1
                        # récupération des informations de l'animal ) afficher
                        info = get_info(noms[(page - 1) % len(noms)])[0]
        # si un bouton de souris est enfoncé
        if event.type == pygame.MOUSEBUTTONDOWN:
            # si c'est le bouton gauche (clic gauche)
            if event.button == 1:
                # récupérer chaque bouton de la recherche
                for btn in resultSearchButton:
                    # s'il est appyué
                    if btn.click(event.pos):
                        # afficher le dictionnaire
                        viewDic = True
                        # récupération des informations de l'animal à afficher
                        info = get_info(btn.textStr)[0]
                # si le bouton de recherche est appuyer
                if searchButton.click(event.pos):
                    # si la barre de recherche n'est pas vide
                    if searchInput.inputStr != "":
                        # sauvegarder le(s) résultat(s) dans une liste
                        result = []
                        # supprimer les anciens résultats
                        resultSearchButton.clear()
                        # récupérer les informations grâce à une requete sqlite
                        for res in cur.execute("SELECT nom FROM main WHERE nom LIKE ?", ('%' + searchInput.inputStr + "%", )):
                            # ajouter chaque résultat
                            result.append(res)
                        # s'il n'y a aucun résultat
                        if len(result) == 0:
                            # le message à afficher est "Aucun résultat trouvé"
                            msg = "Aucun résultat trouvé"
                        # s'il y a plus d'un résulat
                        elif len(result) >= 2:
                            # récupérer chaque résultat
                            for e, res in enumerate(result):
                                # créer un bouton pour chaque résultat
                                b = Button(screen.get_width() / 2 - 350 / 2, screen.get_height() /
                                           6 + 35 * e, 350, 25, 10, (0, 198, 177), res[0])
                                # ajouter chaque bouton dans la liste qui les contient tous
                                resultSearchButton.append(b)
                        # s'il y a un seul résultat
                        else:
                            # afficher le dictionnaire
                            viewDic = True
                            # récupérer les informations sur l'animal
                            info = get_info(result[0][0])[0]
                # si la barre de recherche est appuyer
                if searchInput.click(event.pos):
                    # rien à faire, tout est géré dans la méthode
                    pass
                # si le bouton de visionnage du dictionnaire est appuyer
                if viewButton.click(event.pos):
                    # afficher le dictionnaire
                    viewDic = True
                # si le dictionnaire est en cours de lecture
                if viewDic:
                    # si on appuye à gauche de la page
                    if 0 < event.pos[0] < screen.get_width() / 4:
                        # page précédente
                        page -= 1
                        info = get_info(noms[(page - 1) % len(noms)])[0]
                    # si on appuye à droite de la page
                    if (screen.get_width() / 4 + screen.get_width() / 2) < event.pos[0] < screen.get_width():
                        # page suivante
                        page += 1
                        info = get_info(noms[(page - 1) % len(noms)])[0]
                    # si on appuye sur la fleche de retour
                    if screen.get_width() / 4 < event.pos[0] < screen.get_width() / 4 + back_arrow.get_rect().w and screen.get_height() / 8 < event.pos[1] < screen.get_height() / 8 + back_arrow.get_rect().h:
                        viewDic = False
        # si on redimmensionne la fenetre
        if event.type == pygame.VIDEORESIZE:
            # redimmentionnement des images
            for key, value in images.items():
                images_custom[key] = pygame.transform.scale(
                    value, (int(((screen.get_width() / 8) * 16) / 9), int(screen.get_width() / 8)))
        # si on ferme la fenetre
        if event.type == pygame.QUIT:
            # arret de la fenetre
            running = False
            pygame.quit()
