import pygame
from config import screen_width, screen_height
from foods import carrot, taureau


pygame.init()  # Initialisation de pygame
screen = pygame.display.set_mode((screen_width, screen_height))


foods = [carrot() for _ in range(10)]
taureaus = [taureau() for _ in range(5)]
timer = pygame.time.Clock()
