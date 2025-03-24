import pygame
from clem import Humain

class Game : 
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.humain = Humain("clem", 100, 100)

    def handling_events(self):
        """
        gère les événements
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """
        met à jour les données du jeu
        """
        pass

    def display(self):
        """
        affiche les données du jeu
        """
        pass

    def run(self):
        """
        lance le jeu
        """
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)