# settings.py
import pygame

# Инициализация pygame
pygame.init()

# Параметры окна и игры
WIDTH, HEIGHT = 400, 600
FPS = 60

# Цвета и шрифты
BLACK = (0, 0, 0)
LIGHT_COLOR = (200, 200, 200)
FONT = pygame.font.SysFont("Arial", 24)
OVER_FONT = pygame.font.SysFont("Arial", 36, bold=True)

# Интервалы для спавна ракет и монстров
ROCKET_SPAWN_INTERVAL = 45000  # 45 секунд (мс)
MONSTER_SPAWN_INTERVAL = 5000  # 5 секунд (после 16000 очков)

# Интервалы между платформами
EASY_MIN_GAP = 30
EASY_MAX_GAP = 45
NORMAL_MIN_GAP = 40
NORMAL_MAX_GAP = 60

# Размеры платформ
PLATFORM_SIZE_STANDARD = (70, 15)
PLATFORM_SIZE_SMALL = (50, 15)

# Глобальные игровые переменные (будут переинициализированы в main.py)
score = 0.0
game_over = False
game_started = False
