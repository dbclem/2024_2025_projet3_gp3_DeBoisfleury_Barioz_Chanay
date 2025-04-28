import pygame

class Humain : 
    def __init__(self, name, x , y):
        self.name = name # nom de l'humain
        self.bot = pygame.Rect(0, 0, 50, 50)
        self.init_position = (x, y) # position initiale de l'humain
        self.bot_area = (0, 0, 255, 128)  # Couleur bleue avec opacité réduite (RGBA)
        self.rect = pygame.Rect(x, y, 50, 50)
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
        pygame.draw.rect(screen, self.bot_area, self.rect)

#ici
# pygame.init()
# clock = pygame.time.Clock()
# running = True 
# game_active = False

# poisson = Poisson(0, 0)
# hunger = 300
# max_hunger = 300

# mechants_poissons = []
# for _ in range(10):
#                 x = random.randint(350, 575)
#                 y = random.randint(240, 305)
#                 mechant_poisson = PoissonBouffe(x, y)
#                 print(f"Poisson à ({x}, {y})")
#                 mechants_poissons.append(mechant_poisson)
# font = pygame.font.Font(None, 74)
# Death_text = font.render("YOU DIED", True, (255, 0, 0))
# Start_text = font.render("PRESS SPACE TO START", True, (255, 0, 0))
# bar_width = 200
# bar_height = 30
# requin = PoissonRequin(300,300)
# algue = Algues(500,500)
# timer = 0
# timer += 1
# background = pygame.Surface((25*32, 25*32))
