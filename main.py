import pygame
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
        self.screen.fill("white")
        pygame.draw.rect(self.screen, self.area_color, self.area)
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




pygame.init() # initialisation de pygame

screen_info = pygame.display.Info() # récupération de la taille de l'écran
screen_width = screen_info.current_w # largeur de l'écran
screen_height = screen_info.current_h # hauteur de l'écran
print(f"Screen width: {screen_width}, Screen height: {screen_height}")

screen = pygame.display.set_mode((screen_width, screen_height - 50))  # création de la fenêtre
game = Game(screen) # création de l'objet Game
game.run() # lancement de la boucle de jeu