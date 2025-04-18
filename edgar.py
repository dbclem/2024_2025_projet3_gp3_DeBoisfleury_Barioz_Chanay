import pygame  
from foods import carrot, taureau

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






# class Food:
#     def draw_food (self, screen):
#         """
#         Affiche la nourriture sur la carte
#         """
#         x = random.randint(0, nb_colones - 1) * cell_size
#         y = random.randint(0, nb_lignes - 1) * cell_size
#         rect = (x, y, cell_size, cell_size)
#         pygame.draw.rect(screen, pygame.Color("orange"), rect)



# Crée une liste de 10 carottes
foods = [carrot() for _ in range(10)]  

# Crée une liste de 5 taureaux
taureaus = [taureau() for _ in range(5)]  

# Initialise l'horloge pour contrôler la vitesse du jeu
timer = pygame.time.Clock()
game_on = True

# Dessine toutes les carottes et les taureaux une fois et stocke leurs positions
screen.fill(pygame.Color("white"))  # Remplit l'écran avec une couleur blanche
for food in foods:
    food.draw_food(screen)  # Affiche chaque carotte sur l'écran
for tau in taureaus:
    tau.draw_food(screen)  # Affiche chaque taureau sur l'écran
pygame.display.update()  # Met à jour l'affichage

# Boucle principale du jeu
while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Vérifie si l'utilisateur ferme la fenêtre
            pygame.quit()

    # Pas besoin de redessiner les carottes et les taureaux, on garde juste le jeu en cours
    timer.tick(30)  # Limite la boucle à 30 itérations par seconde


