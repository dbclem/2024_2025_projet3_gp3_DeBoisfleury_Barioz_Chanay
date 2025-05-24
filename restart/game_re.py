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
        self.zones_bonus_rects = []
        for obj in tmx_data.objects: # pour chaque objet de la carte
            if obj.type == "collision":
                self.collision_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) # recuperer les rectangles de collision
            elif obj.type == "goal": # si l'objet est un but
                self.goal_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) # recuperer les rectangles de but
            elif obj.type == "bonus": # si l'objet est un bonus
                self.zones_bonus_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) # recuperer les rectangles de bonus

        # charger les calques de la carte
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3) # group de sprites
        self.group.add(self.player) # ajouter le joueur au groupe de sprites

        self.d_manhattan_init_goal = abs(self.player.position[1] - self.goal_rects[0].y) + abs(self.player.position[0] - self.goal_rects[0].x)
        self.current_episode = 0 # initialiser le nombre d'episodes
        self.nb_episode_max = self.episode()

    def show_grid(self):
        """
        Afficher la grille de la carte
        """
        for x in range(0, self.screen.get_width(), 16):
            pygame.draw.line(self.screen, (255, 0, 0), (x, 0), (x, self.screen.get_height()), 1)
        for y in range(0, self.screen.get_height(), 16):
            pygame.draw.line(self.screen, (255, 0, 0), (0, y), (self.screen.get_width(), y), 1)   


    def def_reward (self, reward) : 
        d_reward = 0
        self.group.update()
        print("fct reward")
        # Récupérer la position du joueur (centre du rect)
        pos_x, pos_y = self.player.position[0], self.player.position[1]
        pos_goal_x , pos_goal_y = self.goal_rects[0].x, self.goal_rects[0].y

        # Récupérer la position du goal (on prend le centre du premier goal_rect)
        d_manhattan_player_goal = abs(int(pos_x - pos_goal_x)) + abs(int(pos_y - pos_goal_y))
        # Décomposition plus précise et logique des rewards basée sur la distance de Manhattan
        ratio = d_manhattan_player_goal / self.d_manhattan_init_goal

        if ratio < 0.05:
            d_reward = 15  # Extrêmement proche du but (récompense augmentée)
            print("Reward: Extrêmement proche du but", d_reward)
        elif ratio < 0.10:
            d_reward = 12  # Très proche du but
            print("Reward: Très proche du but", d_reward)
        elif ratio < 0.15:
            d_reward = 10
            print("Reward: Proche du but", d_reward)
        elif ratio < 0.20:
            d_reward = 7
            print("Reward: Assez proche du but", d_reward)
        elif ratio < 0.30:
            d_reward = 4
            print("Reward: Moyennement proche", d_reward)
        elif ratio < 0.40:
            d_reward = 2
            print("Reward: Un peu loin", d_reward)
        elif ratio < 0.50:
            d_reward = 0
            print("Reward: Loin", d_reward)
        elif ratio < 0.60:
            d_reward = -2
            print("Reward: Assez loin", d_reward)
        elif ratio < 0.70:
            d_reward = -4
            print("Reward: Très loin", d_reward)
        elif ratio < 0.85:
            d_reward = -6
            print("Reward: Très très loin", d_reward)
        elif ratio <= 1.0:
            d_reward = -8
            print("Reward: Presque au maximum de distance", d_reward)
        else:
            d_reward = -12  # Plus loin qu'au départ (s'éloigne du but)
            print("Reward: S'éloigne du but", d_reward)

        coll_reward = -1  # Par défaut, légère pénalité pour chaque mouvement

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collision_rects) > -1:
                print("------- collision -------")
                coll_reward = -10  # Pénalité plus faible pour collision
                print(coll_reward)
            elif sprite.feet.collidelist(self.goal_rects) > -1:
                print("------- but -------")
                coll_reward = 100  # Plus grande récompense pour atteindre le but
                print(coll_reward)
            elif sprite.feet.collidelist(self.zones_bonus_rects) > -1:
                print("------- bonus -------")
                coll_reward = 25
            else:
                print("------- rien -------")
                print(coll_reward)
        
        reward = d_reward + coll_reward # recompense finale
        print("reward : ", reward)
        return reward
    
    def appliquer_action(self, state, action): 
        reward = 0 

        if action == "up": # si l'action est de deplacer le joueur vers le haut
            for _ in range(8): # deplacer le joueur vers le haut
                self.player.move_up() # deplacer le joueur vers le haut
                self.player.change_animation("up") # changer l'animation du joueur vers le haut
            self.current_episode = adding_one(self.current_episode) # ajouter 1 au nombre d'episodes
            new_state = (int(self.player.position[0]/16) + 1 , int(self.player.position[1]/16) + 1) # recuperer la nouvelle position du joueur
            reward = self.def_reward(reward)     
            return new_state, reward # retourner la position du joueur, la recompense et si le jeu est fini

        elif action == "down": # si l'action est de deplacer le joueur vers le bas
            for _ in range(8): # deplacer le joueur vers le bas
                self.player.move_down() # deplacer le joueur vers le bas
                self.player.change_animation("down") # changer l'animation du joueur vers le bas
            self.current_episode = adding_one(self.current_episode)
            new_state = (int(self.player.position[0]/16) + 1 , int(self.player.position[1]/16) + 1) # recuperer la nouvelle position du joueur
            reward = self.def_reward(reward)
            return new_state, reward # retourner la position du joueur, la recompense et si le jeu est fini

        elif action == "left": # si l'action est de deplacer le joueur vers la gauche
            for _ in range(8): # deplacer le joueur vers la gauche
                self.player.move_left() # deplacer le joueur vers la gauche
                self.player.change_animation("left") # changer l'animation du joueur vers la gauche
            self.current_episode = adding_one(self.current_episode)
            new_state = (int(self.player.position[0]/16) + 1 , int(self.player.position[1]/16) + 1) # recuperer la nouvelle position du joueur
            reward = self.def_reward(reward)
            return new_state, reward # retourner la position du joueur, la recompense et si le jeu est fini

        elif action == "right": # si l'action est de deplacer le joueur vers la droite
            for _ in range(8): # deplacer le joueur vers la droite
                self.player.move_right() # deplacer le joueur vers la droite
                self.player.change_animation("right") # changer l'animation du joueur vers la droite
            self.current_episode = adding_one(self.current_episode)
            new_state = (int(self.player.position[0]/16) + 1 , int(self.player.position[1]/16) + 1) # recuperer la nouvelle position du joueur
            reward = self.def_reward(reward)
            return new_state, reward # retourner la position du joueur, la recompense et si le jeu est fini


    def input(self) : 
        key_pressed = pygame.key.get_pressed() # recuperer les touches pressées
        
        if key_pressed[pygame.K_ESCAPE]: # si la touche echap est pressée
            pygame.quit() # quitter le jeu
        
        if key_pressed[pygame.K_i] :           
            self.ia(self.nb_episode_max)  # lancer l'ia si la touche i est pressée

        # Si Ctrl+I est pressé, lancer l'IA en mode exploration
        if key_pressed[pygame.K_e]:
            for _ in range(200):
                self.ia(500)  # lancer l'ia en mode exploration si la touche e est pressée

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


    def episode(self):
        """
        Calculer le nombre d'episodes en fonction de la distance entre le joueur et le but
        """
        multiplicateur_d_min = 0.35
        nb_episodes = int( ( int(self.d_manhattan_init_goal) + int(self.d_manhattan_init_goal) * multiplicateur_d_min) // 16) 
        print("nb episodes : ", nb_episodes)
        return nb_episodes


    def ia (self, nb_episode_max):

        self.current_episode = 0 # initialiser le nombre d'episodes
        self.player.position = [390, 783]  # remettre le joueur à sa position d'origine

        alpha = 0.1   # taux d'apprentissage
        gamma = 0.99   # facteur de récompense future
        epsilon = 1    # probabilité d'explorer plutôt que d'exploiter
        actions = ["up", "down", "left", "right"] # actions possibles
        
    
        for episode in range(nb_episode_max):
            # Réduire epsilon de 0.1 tous les 100 épisodes après 1000
            if episode > 1000 and episode % 100 == 0 and epsilon > 0:
                epsilon = max(0, epsilon - 0.1)
                print(f"Nouvel epsilon: {epsilon}")
                
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
            # Initialiser la Q-table si elle n'existe pas
            try:
                q_table = read_from_numpy_file("q_table.npy")
                print(" ---- \n Q-table loaded \n ----")
            except FileNotFoundError:
                q_table = create_q_table(54, 54, actions)
            except EOFError:
                q_table = create_q_table(54, 54, actions)
                print("--- \n Le fichier Q-table est corrompu, création d'une nouvelle table... \n ---")

            # Choisir une action (exploration ou exploitation)
            if random.uniform(0, 1) < epsilon  :
                action = random.choice(actions)
                print("exploration :", action)
            else:
                biggest_value_action = find_biggest_q_value_with_numpy(q_table[state]) # choisir l'action avec la plus grande valeur Q
                action = actions[biggest_value_action]
                print("--- \n exploitation :", action, "\n ---")
            # Appliquer l'action, obtenir le nouvel état et la récompense

            new_state, reward = self.appliquer_action(state, action)
            self.update() # mettre à jour le groupe de sprites
            # def_final_reward_after_action = reward_after_action (reward)

            action_index = index_in_list(actions, action) # recuperer l'indice de l'action choisie

            # Mise à jour de la Q-table
            old_value = q_table[state][action_index]
            future_max = np.argmax(q_table[new_state])

            new_value =  alpha* old_value +  (1 - alpha)* (reward + gamma * future_max)
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
    


    # pour ajuster les récompenses on peut détécter si le joueur tourne en boucle et pénaliser la récompenses
    # un peu dur a faire 

