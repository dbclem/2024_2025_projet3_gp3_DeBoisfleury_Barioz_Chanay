import pygame
from init import screen, foods, taureaus, timer
from clem import Humain
print("fct = main.py")

# Initialisation de Pygame
pygame.init()

# Chargement du tileset
tileset = pygame.image.load('map/map_1er_jet.tmx')

# Découper des tiles (exemple : des carrés de 32x32 pixels)
TILE_SIZE = 32
tile = tileset.subsurface((0, 0, TILE_SIZE, TILE_SIZE))  # prend la première tuile

# Affichage dans une fenêtre
screen = pygame.display.set_mode((640, 480))
screen.blit(tile, (100, 100))  # affiche la tile à la position (100, 100)

pygame.display.update()

# Boucle simple pour garder la fenêtre ouverte
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

class Game : 
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.humain = Humain("clem", 100, 100)
        self.area = pygame.Rect(0, 0, 300, 300)
        self.area_color = "red"

    def handling_events(self):
        """
        gère les événements
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.humain.velocity[0] = -1
        elif keys[pygame.K_RIGHT]:
            self.humain.velocity[0] = 1
        else:
            self.humain.velocity[0] = 0
        
        if keys[pygame.K_UP]:
            self.humain.velocity[1] = -1
        elif keys[pygame.K_DOWN]:
            self.humain.velocity[1] = 1
        else:
            self.humain.velocity[1] = 0


    
    def update(self):

        """
        met à jour les données du jeu
        """
        self.humain.move()
        if self.area.colliderect(self.humain.rect):
            self.area_color = "green"
        else : 
            self.area_color = "red"

        # limite de carte avce l'ecran 
        if self.humain.rect.left < 0: # si le personnage sort à gauche
            self.humain.rect.left = 0  

        if self.humain.rect.right > self.screen.get_width(): # si le personnage sort à droite
            self.humain.rect.right = self.screen.get_width()

        if self.humain.rect.top < 0: # si le personnage sort en haut
            self.humain.rect.top = 0    

        if self.humain.rect.bottom > self.screen.get_height(): # si le personnage sort en bas
            self.humain.rect.bottom = self.screen.get_height()


    def display(self):
        """
        affiche les données du jeu
        """
        self.humain.draw(self.screen)
        pygame.display.flip()

    def run(self):
        """
        lance le jeu
        """
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)







game = Game(screen)  # Création de l'objet Game


# Dessine toutes les carottes et les taureaux une fois et stocke leurs positions
screen.fill(pygame.Color("white"))  # Remplit l'écran avec une couleur blanche
for food in foods:
    food.draw_food(screen)  # Affiche chaque carotte sur l'écran
for tau in taureaus:
    tau.draw_food(screen)  # Affiche chaque taureau sur l'écran
pygame.display.update()  # Met à jour l'affichage

# Lancement de la boucle de jeu principale
while game.running:
    game.handling_events()
    game.update()
    game.display()

    # Gestion des événements pour quitter le jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Vérifie si l'utilisateur ferme la fenêtre
            game.running = False

    # Limite la boucle à 30 itérations par seconde
    timer.tick(30)

pygame.quit()  # Quitte pygame proprement
