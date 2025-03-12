import pygame
import os

def load_image(filename, size=None):
    path = os.path.join("Images", filename)
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

PLAYER_IMG = load_image("Linera_LOGO.png", (30, 30))
BACKGROUND_IMG = load_image("Background.png", (400, 600))
CHAIN_IMG = load_image("Chain.png")
MONSTER1_IMG = load_image("Monster1.png")
MONSTER2_IMG = load_image("Monster2.png")
MONSTER3_IMG = load_image("Monster3.png")
ROCKET_IMG = load_image("Rokcet.png")
