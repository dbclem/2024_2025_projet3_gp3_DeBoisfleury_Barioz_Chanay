import pygame  
import random
from config import nb_colones, nb_lignes, cell_size

class Super_Food:
    def __init__(self):
        self.nutrition = 0
        self.init_position = (0, 0)
        self.image = None  # Placeholder for the image
        
    def draw_food(self, screen):
        """
        Affiche la nourriture sur la carte
        """
        x = random.randint(0, nb_colones - 1) * cell_size
        y = random.randint(0, nb_lignes - 1) * cell_size
        if self.image:  # Check if the image is loaded
            screen.blit(self.image, (x, y))
        else:
            rect = (x, y, cell_size, cell_size)
            pygame.draw.rect(screen, pygame.Color("orange"), rect)


class carrot(Super_Food): 
    def __init__(self):
        super().__init__()
        self.nutrition = 1
        self.init_position = (0, 0)
        try:
            self.image = pygame.image.load("images/carrot.png").convert_alpha()
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image: {e}")
            self.image = None

class taureau(Super_Food): 
    def __init__(self):
        super().__init__()
        self.nutrition = 10
        self.init_position = (0, 0)
        try:
            self.image = pygame.image.load("images/taureau.png").convert_alpha()
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image: {e}")
            self.image = None
