import pygame
from config import screen_width, screen_height
from foods import carrot, taureau

screen = pygame.display.set_mode((screen_width, screen_height))


carrots = [carrot() for _ in range(10)]
taureaus = [taureau() for _ in range(5)]
timer = pygame.time.Clock()

