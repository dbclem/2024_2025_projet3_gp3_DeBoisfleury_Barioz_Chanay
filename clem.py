import pygame

class Humain : 
    def __init__(self, name, x , y):
        self.name = name # nom de l'humain
        self.image = pygame.image.load("images/humain.png") # image de l'humain
        self.rect = self.image.get_rect(x=x, y=y) # rectangle de l'image
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
        screen.blit(self.image, self.rect)