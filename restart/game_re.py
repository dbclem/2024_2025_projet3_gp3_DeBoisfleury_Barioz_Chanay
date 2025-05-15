import pygame
import pytmx  
import pyscroll
import pytmx.util_pygame
from player import Player   
from random import randint
from tools import adding_one


class Game : 
    def __init__(self):
        

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Game")


        # charger la carte
        # tmx_data = pytmx.util_pygame.load_pygame("map/1map -niveau0.tmx")
        tmx_data = pytmx.util_pygame.load_pygame("map/1map -niveau0.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # charger le joueur 
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y) # position du joueur sur la carte

        # definir une lsite qui stock les rectangles de collision
        self.collision_rects = []
        self.goal_rects = []
        for obj in tmx_data.objects: # pour chaque objet de la carte
            if obj.type == "collision":
                self.collision_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) # recuperer les rectangles de collision
            elif obj.type == "goal": # si l'objet est un but
                self.goal_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) # recuperer les rectangles de but
        
        # charger les calques de la carte
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3) # group de sprites
        self.group.add(self.player) # ajouter le joueur au groupe de sprites

        self.current_episode = 0 # initialiser le nombre d'episodes


    def appliquer_action(self, state,action): 
        x, y = state # recuperer la position du joueur

        if action == "up": # si l'action est de deplacer le joueur vers le haut
            self.player.move_up() # deplacer le joueur vers le haut
            self.player.change_animation("up") # changer l'animation du joueur vers le haut
            self.current_episode = adding_one(self.current_episode) # ajouter 1 au nombre d'episodes

        elif action == "down": # si l'action est de deplacer le joueur vers le bas
            self.player.move_down() # deplacer le joueur vers le bas    
            self.player.change_animation("down")
            self.current_episode = adding_one(self.current_episode)

        elif action == "left": # si l'action est de deplacer le joueur vers la gauche
            self.player.move_left() # deplacer le joueur vers la gauche
            self.player.change_animation("left")
            self.current_episode = adding_one(self.current_episode)
        
        elif action == "right": # si l'action est de deplacer le joueur vers la droite
            self.player.move_right() # deplacer le joueur vers la droite
            self.player.change_animation("right")
            self.current_episode = adding_one(self.current_episode)



        """ajouter une recompense en fonction de la distance entre le joueur et le but""" 
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collision_rects) > -1: # -1 est la valeur de retour si il n'y a pas de collision*
                return state, -1, False 
            if sprite.feet.collidelist(self.goal_rects) > -1: # si le joueur touche un rectangle de but
                return (x, y), 10, True # retourner la position du joueur, la recompense et si le jeu est fini
            
        return state, -0.1, False # mouvement normal, petite punition pour encourager l’efficacité



    


    def input(self) : 
        key_pressed = pygame.key.get_pressed() # recuperer les touches pressées
        
        if key_pressed[pygame.K_UP]: # si la touche haut est pressée
            self.player.move_up() # deplacer le joueur vers le haut
            self.player.change_animation("up") # changer l'animation du joueur vers le haut
            self.current_episode = adding_one(self.current_episode) # ajouter 1 au nombre d'episodes

        elif key_pressed[pygame.K_DOWN]:
            self.player.move_down() # deplacer le joueur vers le bas
            self.player.change_animation("down") # changer l'animation du joueur vers le bas
            self.current_episode = adding_one(self.current_episode)

        elif key_pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation("left") # changer l'animation du joueur vers la gauche
            self.current_episode = adding_one(self.current_episode)

        elif key_pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation("right") # changer l'animation du joueur vers la droite
            self.current_episode = adding_one(self.current_episode)



    def update(self):
        self.group.update() # mettre à jour le groupe de sprites

        #verif des collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collision_rects) > -1: # -1 est la valeur de retour si il n'y a pas de collision
                sprite.move_back() # si le joueur touche un rectangle de collision, il revient à sa position précédente
            if sprite.feet.collidelist(self.goal_rects) > -1: # si le joueur touche un rectangle de but
                self.player.position = [390, 783] # remettre le joueur à sa position d'origine
                self.current_episode = 0 

    def episode(self, init_x, init_y, goal_x, goal_y):
        """
        Calculer le nombre d'episodes en fonction de la distance entre le joueur et le but
        """
        multiplicateur_d_min = 0.35
        d_manhattan = abs(init_y - init_x) + abs(goal_y - goal_x)
        nb_episodes = int( ( int(d_manhattan) + int(d_manhattan) * multiplicateur_d_min) // 16) 
        print("nb episodes : ", nb_episodes)
        return nb_episodes

    def run(self):

        running = True
        nb_episode_max = self.episode(self.player.position[0], self.player.position[1], 510, 175)
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

            if self.current_episode >= nb_episode_max:
                pygame.time.wait(250)
                self.player.position = [390, 783] # remettre le joueur à sa position d'origine
                self.current_episode = 0

            time_clock.tick(30)

        pygame.quit()
        return running

