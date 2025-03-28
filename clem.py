import pygame

class Humain : 
    def __init__(self, name, x , y):
        self.name = name # nom de l'humain
        self.bot = pygame.Rect(0, 0, 50, 50)
        self.bot_area  = "blue"
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = 5 # vitesse de déplacement
        self.velocity = [0, 0] # vecteur de déplacement

    
    def move(self):
        """
        multiplie la vitesse par le vecteur de déplacement
        """
        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)
        
    def draw(self, screen):
        """
        dessine l'humain sur l'écran
        """
        pygame.draw.rect(screen, self.bot_area, self.rect)

