import pygame
from config import screen_width, screen_height
from foods import carrot, taureau
import random

screen = pygame.display.set_mode((screen_width, screen_height))


carrots = [carrot(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(10)]
taureaus = [taureau(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(5)]
timer = pygame.time.Clock()

