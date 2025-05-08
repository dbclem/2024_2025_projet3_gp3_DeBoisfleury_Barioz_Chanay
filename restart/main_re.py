import pygame 
from game_re import Game

if __name__ == "__main__":
    pygame.init()

    try:
        image = pygame.image.load("map/1map.tmx")
        print("Image chargée avec succès")
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image : {e}")
    game = Game()
    game.run()
