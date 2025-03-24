import pygame
from clem import Humain

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

    
pygame.init()
screen = pygame.display.set_mode((800, 600))
game = Game(screen)
game.run()