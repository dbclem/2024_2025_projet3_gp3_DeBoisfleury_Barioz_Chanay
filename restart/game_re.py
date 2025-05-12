import pygame
import pytmx  
import pyscroll
import pytmx.util_pygame
from player import Player   
from random import randint

class Game : 
    def __init__(self):
        

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Game")


        # charger la carte
        # tmx_data = pytmx.util_pygame.load_pygame("map/1map -niveau0.tmx")
        tmx_data = pytmx.util_pygame.load_pygame("map/1map -niveau1.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # charger le joueur 
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y) # position du joueur sur la carte

        # definir une lsite qui stock les rectangles de collision
        self.collision_rects = []
        for obj in tmx_data.objects: # pour chaque objet de la carte
            if obj.type == "collision":
                self.collision_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) # recuperer les rectangles de collision

        # charger les calques de la carte
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3) # group de sprites
        self.group.add(self.player) # ajouter le joueur au groupe de sprites


    def input(self) : 
        key_pressed = pygame.key.get_pressed() # recuperer les touches pressées
        
        if key_pressed[pygame.K_UP]: # si la touche haut est pressée
            self.player.move_up() # deplacer le joueur vers le haut
            self.player.change_animation("up") # changer l'animation du joueur vers le haut

        elif key_pressed[pygame.K_DOWN]:
            self.player.move_down() # deplacer le joueur vers le bas
            self.player.change_animation("down") # changer l'animation du joueur vers le bas

        elif key_pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation("left") # changer l'animation du joueur vers la gauche

        elif key_pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation("right") # changer l'animation du joueur vers la droite


        if key_pressed[pygame.K_r] : 
            random_nb = randint(0, 3) # generer un nombre aleatoire entre 0 et 100
            #random mvt
            if random_nb == 0: # si la touche haut est pressée
                self.player.move_up() # deplacer le joueur vers le haut
                self.player.change_animation("up") # changer l'animation du joueur vers le haut

            elif random_nb == 1:
                self.player.move_down() # deplacer le joueur vers le bas
                self.player.change_animation("down") # changer l'animation du joueur vers le bas

            elif random_nb == 2:
                self.player.move_left()
                self.player.change_animation("left") # changer l'animation du joueur vers la gauche

            elif random_nb == 3:
                self.player.move_right()
                self.player.change_animation("right") # changer l'animation du joueur vers la droite



    def update(self):
        self.group.update() # mettre à jour le groupe de sprites

        #verif des collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collision_rects) > -1: # -1 est la valeur de retour si il n'y a pas de collision
                sprite.move_back() # si le joueur touche un rectangle de collision, il revient à sa position précédente

    def episode(self, init_x, init_y, goal_x, goal_y):
        d_manhattan = abs(init_y - init_x) + abs(goal_y - goal_x)
        nb_episodes = int( ( int(d_manhattan) + int(d_manhattan) * 0.3) // 16) 
        print("nb episodes : ", nb_episodes)
        return nb_episodes

    def run(self):

        running = True
        self.episode(self.player.position[0], self.player.position[1], 510, 175)
        time_clock = pygame.time.Clock() # horloge pour gerer le temps

        while running:
            
            self.player.save_location() # sauvegarder la position du joueur
            self.input()
            self.update()
            self.group.center(self.player.rect) # centrer la camera sur le joueur
            self.group.draw(self.screen) # dessiner le groupe de sprites sur l'ecran
            pygame.display.flip() # rafraichir l'ecran

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            time_clock.tick(30)

        pygame.quit()
        return running

