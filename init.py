import pygame
from config import screen_width, screen_height
from foods import carrot, taureau


screen = pygame.display.set_mode((screen_width, screen_height))
game = True


foods = [carrot() for _ in range(10)]
taureaus = [taureau() for _ in range(5)]
timer = pygame.time.Clock()

#definir ce qu'il s'affiche sur l'écran 
screen.fill(pygame.Color("white"))  # Remplit l'écran avec une couleur blanche
for food in foods:
    food.draw_food(screen)  # Affiche chaque carotte sur l'écran
for tau in taureaus:
    tau.draw_food(screen)  # Affiche chaque taureau sur l'écran
pygame.display.update() 

while game : 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            pygame.quit()

pygame.init()  # Initialisation de pygame