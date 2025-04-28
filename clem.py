pygame.init()
clock = pygame.time.Clock()
running = True 
game_active = False

poisson = Poisson(0, 0)
hunger = 300
max_hunger = 300

mechants_poissons = []
for _ in range(10):
                x = random.randint(350, 575)
                y = random.randint(240, 305)
                mechant_poisson = PoissonBouffe(x, y)
                print(f"Poisson à ({x}, {y})")
                mechants_poissons.append(mechant_poisson)
font = pygame.font.Font(None, 74)
Death_text = font.render("YOU DIED", True, (255, 0, 0))
Start_text = font.render("PRESS SPACE TO START", True, (255, 0, 0))
bar_width = 200
bar_height = 30
requin = PoissonRequin(300,300)
algue = Algues(500,500)
timer = 0
timer += 1
background = pygame.Surface((25*32, 25*32))
