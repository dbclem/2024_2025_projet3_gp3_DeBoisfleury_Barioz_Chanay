import pygame  
import random
import sys

pygame.init()

nb_colones = 190
nb_lignes = 103
cell_size = 10

screen = pygame.display.set_mode((nb_colones * cell_size, nb_lignes * cell_size))

# def show_grid():
#     """
#     Affiche la grille de la carte
#     """
#     for i in range(0, nb_colones):
#         for j in range(0, nb_lignes):
#             rect = (i * cell_size, j * cell_size, cell_size, cell_size)
#             pygame.draw.rect(screen, pygame.Color("black"), rect, width=1)

class Food:
    def draw_food (self, screen):
        """
        Affiche la nourriture sur la carte
        """
        x = random.randint(0, nb_colones - 1) * cell_size
        y = random.randint(0, nb_lignes - 1) * cell_size
        rect = (x, y, cell_size, cell_size)
        pygame.draw.rect(screen, pygame.Color("orange"), rect)


food = Food()

timer = pygame.time.Clock()
game_on = True


while game_on :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(pygame.Color("white"))
    # show_grid()
    food.draw_food(screen)
    pygame.display.update()
    timer.tick(1)