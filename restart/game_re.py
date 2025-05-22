import pygame
import pytmx  
import pyscroll
import pytmx.util_pygame
import numpy as np
from player import Player   
from q_table import create_q_table, find_biggest_q_value_with_numpy
from tools import read_from_numpy_file, write_in_numpy_file, index_in_list
import random
from tools import adding_one


class Game : 
    def __init__(self):
        

        self.screen = pygame.display.set_mode((54*16, 54*16))
        pygame.display.set_caption("Game")


        # charger la carte
        # tmx_data = pytmx.util_pygame.load_pygame("map/1map -niveau0.tmx")
        tmx_data = pytmx.util_pygame.load_pygame("map/1map -niveau0.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

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
        self.nb_episode_max = self.episode(self.player.position[0], self.player.position[1], 510, 175)

    def show_grid(self):
        """
        Afficher la grille de la carte
        """
        for x in range(0, self.screen.get_width(), 16):
            pygame.draw.line(self.screen, (255, 0, 0), (x, 0), (x, self.screen.get_height()), 1)
        for y in range(0, self.screen.get_height(), 16):
            pygame.draw.line(self.screen, (255, 0, 0), (0, y), (self.screen.get_width(), y), 1)   


    def appliquer_action(self, state, action): 
        x, y = state # recuperer la position du joueur

        if action == "up": # si l'action est de deplacer le joueur vers le haut
            for _ in range(8): # deplacer le joueur vers le haut
                self.player.move_up() # deplacer le joueur vers le haut
                self.player.change_animation("up") # changer l'animation du joueur vers le haut
            self.current_episode = adding_one(self.current_episode) # ajouter 1 au nombre d'episodes
            new_state = (int(self.player.position[0]/16) + 1 , int(self.player.position[1]/16) + 1) # recuperer la nouvelle position du joueur
            return new_state, -0.1, False # retourner la position du joueur, la recompense et si le jeu est fini

        elif action == "down": # si l'action est de deplacer le joueur vers le bas
            for _ in range(8): # deplacer le joueur vers le bas
                self.player.move_down() # deplacer le joueur vers le bas
                self.player.change_animation("down") # changer l'animation du joueur vers le bas
            self.current_episode = adding_one(self.current_episode)
            new_state = (int(self.player.position[0]/16) + 1 , int(self.player.position[1]/16) + 1) # recuperer la nouvelle position du joueur
            return new_state, -0.1, False # retourner la position du joueur, la recompense et si le jeu est fini

        elif action == "left": # si l'action est de deplacer le joueur vers la gauche
            for _ in range(8): # deplacer le joueur vers la gauche
                self.player.move_left() # deplacer le joueur vers la gauche
                self.player.change_animation("left") # changer l'animation du joueur vers la gauche
            self.current_episode = adding_one(self.current_episode)
            new_state = (int(self.player.position[0]/16) + 1 , int(self.player.position[1]/16) + 1) # recuperer la nouvelle position du joueur
            return new_state, -0.1, False # retourner la position du joueur, la recompense et si le jeu est fini

        elif action == "right": # si l'action est de deplacer le joueur vers la droite
            for _ in range(8): # deplacer le joueur vers la droite
                self.player.move_right() # deplacer le joueur vers la droite
                self.player.change_animation("right") # changer l'animation du joueur vers la droite
            self.current_episode = adding_one(self.current_episode)
            new_state = (int(self.player.position[0]/16) + 1 , int(self.player.position[1]/16) + 1) # recuperer la nouvelle position du joueur
            return new_state, -0.1, False # retourner la position du joueur, la recompense et si le jeu est fini


        """ajouter une recompense en fonction de la distance entre le joueur et le but""" 
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collision_rects) > -1: # -1 est la valeur de retour si il n'y a pas de collision*
                return state, -1, False 
            if sprite.feet.collidelist(self.goal_rects) > -1: # si le joueur touche un rectangle de but
                return (x, y), 10, True # retourner la position du joueur, la recompense et si le jeu est fini
            
        return state, -0.1, False # mouvement normal, petite punition pour encourager l’efficacité



    def input(self) : 
        key_pressed = pygame.key.get_pressed() # recuperer les touches pressées
        
        if key_pressed[pygame.K_ESCAPE]: # si la touche echap est pressée
            pygame.quit() # quitter le jeu
        
        if key_pressed[pygame.K_i] : 
            self.ia(self.nb_episode_max)  # lancer l'ia si la touche i est pressée

        if key_pressed[pygame.K_UP]: # si la touche haut est pressée
            for _ in range(8):
                self.player.move_up() # deplacer le joueur vers le haut
                self.player.change_animation("up") # changer l'animation du joueur vers le haut
            self.current_episode = adding_one(self.current_episode) # ajouter 1 au nombre d'episodes

        elif key_pressed[pygame.K_DOWN]:
            for _ in range(8):
                self.player.move_down() # deplacer le joueur vers le bas
                self.player.change_animation("down") # changer l'animation du joueur vers le bas
            self.current_episode = adding_one(self.current_episode)

        elif key_pressed[pygame.K_LEFT]:
            for _ in range(8):
                self.player.move_left()
                self.player.change_animation("left") # changer l'animation du joueur vers la gauche
            self.current_episode = adding_one(self.current_episode)

        elif key_pressed[pygame.K_RIGHT]:
            for _ in range(8):
                self.player.move_right()
                self.player.change_animation("right") # changer l'animation du joueur vers la droite
            self.current_episode = adding_one(self.current_episode)

        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
                
        #         if event.key == pygame.K_UP:
        #             for _ in range(8):
        #                 self.player.move_up()
        #                 self.player.change_animation("up")
        #             self.current_episode = adding_one(self.current_episode)
                
        #         elif event.key == pygame.K_DOWN:
        #             for _ in range(8):
        #                 self.player.move_down()
        #                 self.player.change_animation("down")
        #             self.current_episode = adding_one(self.current_episode)
               
        #         elif event.key == pygame.K_LEFT:
        #             for _ in range(8):
        #                 self.player.move_left()
        #                 self.player.change_animation("left")
        #             self.current_episode = adding_one(self.current_episode)
               
        #         elif event.key == pygame.K_RIGHT:
        #             for _ in range(8):
        #                 self.player.move_right()
        #                 self.player.change_animation("right")
        #             self.current_episode = adding_one(self.current_episode)

    def update(self):
        self.group.update() # mettre à jour le groupe de sprites        

        #verif des collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collision_rects) > -1: # -1 est la valeur de retour si il n'y a pas de collision
                sprite.move_back() # si le joueur touche un rectangle de collision, il revient à sa position précédente
           
            if sprite.feet.collidelist(self.goal_rects) > -1: # si le joueur touche un rectangle de but
                font_finish = pygame.font.SysFont(None, 60)
                text_finish = font_finish.render("VOUS AVEZ ATTEINT LA SORTIE", True, (0, 255, 0))
                text_rect = text_finish.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
                self.screen.blit(text_finish, text_rect)
                pygame.display.flip()
                pygame.time.wait(1500) 
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

    def ia (self, nb_episode_max):

        self.current_episode = 0 # initialiser le nombre d'episodes

        alpha = 0.1     # taux d'apprentissage
        gamma = 0.9     # facteur de récompense future
        epsilon = 0.1   # probabilité d'explorer plutôt que d'exploiter
        actions = ["up", "down", "left", "right"] # actions possibles
        
        for episode in range(nb_episode_max):
            self.player.save_location() # sauvegarder la position du joueur
            self.update()
            self.group.center(self.player.rect) # centrer la camera sur le joueur
            self.group.draw(self.screen) # dessiner le groupe de sprites sur l'ecran
            self.show_grid() # afficher la grille de la carte
            
            # Afficher le nombre max d'épisodes en haut à gauche
            font_episode_max = pygame.font.SysFont(None, 36)
            max_episode_text = font_episode_max.render(f"Max Episodes: {nb_episode_max}", True, (0, 0, 0))
            self.screen.blit(max_episode_text, (10, 40))
            # Afficher le current_episode en haut à gauche
            font_current_episode = pygame.font.SysFont(None, 36)
            episode_text = font_current_episode.render(f"Episode: {self.current_episode}", True, (0, 0, 0))
            self.screen.blit(episode_text, (10, 10))

            pygame.display.flip() # rafraichir l'ecran


            position_player = self.player.position # recuperer la position du joueur
            print("position joueur : ", position_player)
            state = (int(position_player[0]/16) + 1, int(position_player[1]/16) + 1) # recuperer la position du joueur
            done = False
            # Initialiser la Q-table si elle n'existe pas
            try:
                q_table = read_from_numpy_file("q_table.npy")
            except FileNotFoundError:
                q_table = create_q_table(54, 54, actions)
            except EOFError:
                q_table = create_q_table(54, 54, actions)
                print("--- \n Le fichier Q-table est corrompu, création d'une nouvelle table... \n ---")

            # Choisir une action (exploration ou exploitation)
            if random.uniform(0, 1) < (1 - epsilon ) :
                action = random.choice(actions)
                print("exploration :", action)
            else:
                biggest_value_action = find_biggest_q_value_with_numpy(q_table[state]) # choisir l'action avec la plus grande valeur Q
                action = actions[biggest_value_action]
                print("--- \n exploitation :", action, "\n ---")
            # Appliquer l'action, obtenir le nouvel état et la récompense

            new_state, reward, done = self.appliquer_action(state, action)
            self.update() # mettre à jour le groupe de sprites

            action_index = index_in_list(actions, action) # recuperer l'indice de l'action choisie

            # Mise à jour de la Q-table
            old_value = q_table[state][action_index]
            future_max = np.argmax(q_table[new_state])

            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * future_max)
            q_table[state][action_index] = new_value

            # Enregistrer la Q-table
            write_in_numpy_file("q_table.npy", q_table)
            # Mettre à jour l'état
            state = new_state
            print("state : ", state)


    def run(self):

        running = True
        time_clock = pygame.time.Clock() # horloge pour gerer le temps

        while running:
             
            self.player.save_location() # sauvegarder la position du joueur
            self.input()
            self.update()
            self.group.center(self.player.rect) # centrer la camera sur le joueur
            self.group.draw(self.screen) # dessiner le groupe de sprites sur l'ecran
            self.show_grid() # afficher la grille de la carte
            
            # Afficher le nombre max d'épisodes en haut à gauche
            font_episode_max = pygame.font.SysFont(None, 36)
            max_episode_text = font_episode_max.render(f"Max Episodes: {self.nb_episode_max}", True, (0, 0, 0))
            self.screen.blit(max_episode_text, (10, 40))
            # Afficher le current_episode en haut à gauche
            font_current_episode = pygame.font.SysFont(None, 36)
            episode_text = font_current_episode.render(f"Episode: {self.current_episode}", True, (0, 0, 0))
            self.screen.blit(episode_text, (10, 10))

            pygame.display.flip() # rafraichir l'ecran
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.current_episode >= self.nb_episode_max:
                font_game_over = pygame.font.SysFont(None, 60)
                text_game_over = font_game_over.render("GAME OVER", True, (255, 0, 0))
                text_rect = text_game_over.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
                self.screen.blit(text_game_over, text_rect)
                pygame.display.flip()
                pygame.time.wait(1500) 
                self.player.position = [390, 783] # remettre le joueur à sa position d'origine
                self.current_episode = 0

            time_clock.tick(30)

        pygame.quit()
        return running
    


    # WIP arreter l'execution du programme si apres le nombre d'episodes max
    # comprendre pourquoi les states ne changent presque pas bouge pas ? bug ? 
    # pouvoir ralentir les actions de l'ia pour comprendre ce qu'elle fait

