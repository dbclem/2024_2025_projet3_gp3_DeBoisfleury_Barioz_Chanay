import pygame
from init import screen, carrots, taureaus, timer
from clem import Humain
print("fct = main.py")


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

def draw_food(screen, image, pos_x, pos_y):
    """
    Dessine la nourriture sur la carte
    """
    rect = (pos_x, pos_y, 10, 10)  # Taille de la nourriture
    screen.blit(image, rect)  # Affiche l'image de la nourriture à la position donnée
    pygame.draw.rect(screen, pygame.Color("white"), rect)  # Dessine un rectangle orange pour la nourriture

# Dessine toutes les carottes et les taureaux une fois et stocke leurs positions
screen.fill(pygame.Color("white"))  # Remplit l'écran avec une couleur blanche
for carrot in carrots:
    draw_food(screen, carrot.image, carrot.init_position[0], carrot.init_position[1])  # Affiche chaque carotte sur l'écran
for tau in taureaus:
    draw_food(screen, tau.image, tau.init_position[0], tau.init_position[1])  # Affiche chaque taureau sur l'écran
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
