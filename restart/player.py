import pygame 

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("player.png") # recuperer l'image 
        self.image = self.get_image(0, 0) # recuperer une image de la sprite sheet
        self.image.set_colorkey((0, 0, 0)) # definir la couleur de transparence (noir)
        self.rect = self.image.get_rect() # recuperer le rectangle de l'image pour la positionner sur l'ecran
        self.feet = pygame.Rect(0, 0, self.rect.width // 2, 12) # recuperer le rectangle de la position du joueur

        self.dico_anim = {
            "down": [self.get_image(0, 0), self.get_image(32, 0), self.get_image(64, 0)], # recuperer les images de l'animation vers le bas
            "left": [self.get_image(0, 32), self.get_image(32, 32), self.get_image(64, 32)], # recuperer les images de l'animation vers le haut
            "right": [self.get_image(0, 64), self.get_image(32, 64), self.get_image(64, 64)], # recuperer les images de l'animation vers la gauche
            "up": [self.get_image(0, 96), self.get_image(32, 96), self.get_image(64, 96)] # recuperer les images de l'animation vers la droite
        }        

        self.position = [x, y]
        self.old_position = self.position.copy() # copier l'ancienne position du joueur
        self.speed = 2 # vitesse de deplacement du joueur

    def save_location (self) : 
        self.old_position = self.position.copy()


    def change_animation(self, direction):
        """
        Change l'animation du joueur en fonction de la direction*
        fonction demandée a copilot totalement mais pas le dico
        """
        if direction in self.dico_anim:
            # Pour animer, il faut parcourir les images de la liste d'animation
            if not hasattr(self, "anim_index"):
                self.anim_index = 0
            self.anim_index = (self.anim_index + 1) % len(self.dico_anim[direction])
            self.image = self.dico_anim[direction][self.anim_index]
            self.image.set_colorkey((0, 0, 0))

    def move_right(self):
        self.position[0] += self.speed*8
        
    def move_left(self):
        self.position[0] -= self.speed*8

    def move_up(self):
        self.position[1] -= self.speed*8

    def move_down(self):
        self.position[1] += self.speed*8



    def update(self):
        self.rect.topleft = self.position # topleft = position de coin supérieur gauche du rectangle = position du joueur
        self.feet.midbottom = self.rect.midbottom # midbottom = milieu du bas du rectangle = position des pieds du joueur

    def move_back(self) : 
        """
        Remet le joueur à sa position d'origine si il y a une collision
        """
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y) :
        """
        Récupère une des images de la sprite sheet à partir de ses coordonnées (x, y)
        Pour récupérer un seul element d'animation 
        """
        image = pygame.Surface((32, 32)) # taille du bout d'image qu'on veut récupérer (taile du joueur)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32)) # extraire un morceau de l'image 
        return image

