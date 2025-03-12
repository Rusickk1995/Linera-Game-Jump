# sprites.py
import pygame
import random
from settings import BLACK, LIGHT_COLOR
from resources import PLAYER_IMG, ROCKET_IMG, MONSTER1_IMG, MONSTER2_IMG, MONSTER3_IMG

# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.vel_y = 0
        self.jump_strength = -20

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Применяем гравитацию – увеличиваем vel_y
        # Можно использовать функцию get_gravity, которая возвращает 0.5
        from utils import get_gravity  # Если функция не импортирована ранее в этом модуле
        self.vel_y += get_gravity(0)  # или просто: self.vel_y += 0.5

        self.rect.y += self.vel_y

        # Зацикливание по горизонтали
        if self.rect.left > 400:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = 400

    def jump(self):
        self.vel_y = self.jump_strength

# Платформа
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.breakable = False
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        chain_link_width = 20
        chain_link_height = h
        line_thickness = 3
        for tile_x in range(0, w, chain_link_width):
            rect = (tile_x, 0, chain_link_width, chain_link_height)
            pygame.draw.ellipse(self.image, BLACK, rect, line_thickness)
        self.rect = self.image.get_rect(topleft=(x, y))

# Разрушаемая платформа
class BreakablePlatform(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.breakable = True
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        chain_link_width = 20
        chain_link_height = h
        line_thickness = 3
        for tile_x in range(0, w, chain_link_width):
            rect = (tile_x, 0, chain_link_width, chain_link_height)
            pygame.draw.ellipse(self.image, LIGHT_COLOR, rect, line_thickness)

# Движущаяся платформа
class MovingPlatform(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.speed_x = random.choice([-3, 3])
    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left <= 0 or self.rect.right >= 400:
            self.speed_x = -self.speed_x

# Ракета
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ROCKET_IMG
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_y = 1
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > 600:
            self.kill()

# Монстр
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_y = 1
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > 600:
            self.kill()
