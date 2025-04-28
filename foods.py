import pygame  
import random
from config import nb_colones, nb_lignes, cell_size


class carrot(): 
    def __init__(self, position_x, position_y):
        self.nutrition = 1
        self.init_position = (position_x, position_y)
        self.eat = False
        self.image = None
        self.rect = pygame.Rect(position_x, position_y, cell_size, cell_size)
        try:
            self.image = pygame.image.load("images/carrot.png").convert_alpha()
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image: {e}")
            self.image = None

        if self.eat :
            self.image = None

class taureau(): 
    def __init__(self, position_x, position_y):
        self.nutrition = 10
        self.init_position = (position_x, position_y)
        self.eat = False
        self.image = None
        self.rect = pygame.Rect(position_x, position_y, cell_size, cell_size)

        try:
            self.image = pygame.image.load("images/taureau.png").convert_alpha()
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image: {e}")
            self.image = None

        if self.eat :
            self.image = None

