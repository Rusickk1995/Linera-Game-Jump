# main.py

# Первоначальная инициализация Pygame и установка видеорежима!
import pygame
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

# Теперь можно импортировать остальные модули, которые зависят от установленного дисплея
import random, sys, time
from settings import WIDTH, HEIGHT, FPS, ROCKET_SPAWN_INTERVAL, MONSTER_SPAWN_INTERVAL, BLACK, LIGHT_COLOR, FONT, OVER_FONT, NORMAL_MAX_GAP
from settings import WIDTH, HEIGHT, FPS, ROCKET_SPAWN_INTERVAL, MONSTER_SPAWN_INTERVAL, BLACK, LIGHT_COLOR, FONT, OVER_FONT
from resources import BACKGROUND_IMG, PLAYER_IMG, ROCKET_IMG, MONSTER1_IMG, MONSTER2_IMG, MONSTER3_IMG
from utils import get_platform_gap, get_gravity, is_on_platform, get_platform_size
from sprites import Player, Platform, BreakablePlatform, MovingPlatform, Rocket, Monster

pygame.display.set_caption("Linera Jump")
clock = pygame.time.Clock()

# Масштабируем фон
background = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))

# Группы спрайтов
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
rockets = pygame.sprite.Group()
monsters = pygame.sprite.Group()

# Глобальные переменные
score = 0.0
game_over = False
game_started = False
last_rocket_spawn_time = 0
last_monster_spawn_time_monsters = 0

# Функция для позиционирования игрока на базовой платформе
def position_player_on_base(base, player):
    player.rect.midbottom = (base.rect.centerx, base.rect.top)
    player.vel_y = 0

# Функция создания платформ (использует логику выбора типа платформы)
def create_platform(x, y, score, base=False):
    w, h = get_platform_size(score)
    if base:
        return Platform(x, y, w, h)
    if score >= 9000 and random.random() < 0.10:
        return MovingPlatform(x, y, w, h)
    if score >= 10000 and random.random() < random.uniform(0.10, 0.25):
        return BreakablePlatform(x, y, w, h)
    return Platform(x, y, w, h)

def generate_non_overlapping_platform(y_min, y_max, score):
    attempts = 0
    w, h = get_platform_size(score)
    while attempts < 100:
        x = random.randint(0, WIDTH - w)
        y = random.randint(y_min, y_max)
        new_plat = create_platform(x, y, score)
        collision = any(new_plat.rect.colliderect(plat.rect) for plat in platforms)
        if not collision:
            return new_plat
        attempts += 1
    return None

def generate_platforms(num, score):
    generated = 0
    attempts = 0
    while generated < num and attempts < 200:
        w, h = get_platform_size(score)
        x = random.randint(0, WIDTH - w)
        y = random.randint(30, HEIGHT - 80)
        new_plat = create_platform(x, y, score)
        collision = any(new_plat.rect.colliderect(plat.rect) for plat in platforms)
        if not collision:
            platforms.add(new_plat)
            all_sprites.add(new_plat)
            generated += 1
        attempts += 1

def fill_platforms_upwards(score):
    if not platforms:
        return
    topmost_y = min(plat.rect.top for plat in platforms)
    while topmost_y > -100:
        gap_min, gap_max = get_platform_gap(score)
        gap = random.randint(gap_min, gap_max)
        new_y = topmost_y - gap
        w, h = get_platform_size(score)
        new_x = random.randint(0, WIDTH - w)
        plat = create_platform(new_x, new_y, score)
        platforms.add(plat)
        all_sprites.add(plat)
        topmost_y = new_y

# Инициализация базовой платформы и игрока
base = create_platform((WIDTH - get_platform_size(score)[0]) // 2, HEIGHT - 20, score, base=True)
platforms.add(base)
all_sprites.add(base)

player = Player()
all_sprites.add(player)
position_player_on_base(base, player)
fill_platforms_upwards(score)

# Основной игровой цикл
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                if is_on_platform(player, platforms):
                    if not game_started:
                        game_started = True
                        # Удаляем базовую платформу при первом прыжке
                        if base in platforms:
                            platforms.remove(base)
                        if base in all_sprites:
                            all_sprites.remove(base)
                    player.jump()
            if event.key == pygame.K_SPACE and game_over:
                # Перезапуск игры
                game_over = False
                score = 0.0
                game_started = False
                for plat in list(platforms):
                    if plat != base:
                        plat.kill()
                for rocket in list(rockets):
                    rocket.kill()
                for monster in list(monsters):
                    monster.kill()
                generate_platforms(7, score)
                position_player_on_base(base, player)
                if base not in platforms:
                    platforms.add(base)
                    all_sprites.add(base)

    if not game_over:
        all_sprites.update()

        # Столкновение с монстрами
        if pygame.sprite.spritecollide(player, monsters, False):
            game_over = True
            player.vel_y = abs(player.vel_y) if player.vel_y >= 0 else 20

        # Столкновение с ракетой
        rocket_hits = pygame.sprite.spritecollide(player, rockets, True)
        if rocket_hits:
            if score < 10000:
                bonus = random.randint(500, 2000)
            elif score >= 15000:
                bonus = random.randint(2000, 6000)
            else:
                bonus = random.randint(500, 2000)
            score += bonus
            player.vel_y = -40

        # Обработка столкновений с платформами
        if player.vel_y > 0:
            for plat in platforms:
                if player.rect.colliderect(plat.rect):
                    if (player.rect.bottom - player.vel_y) <= (plat.rect.top + 10):
                        player.rect.bottom = plat.rect.top
                        if game_started:
                            if hasattr(plat, 'breakable') and plat.breakable:
                                plat.kill()
                            else:
                                player.jump()
                        else:
                            player.vel_y = 0
                        break

        # Сдвиг спрайтов вниз, если игрок выше середины экрана
        if player.rect.top <= HEIGHT // 2:
            shift = (HEIGHT // 2) - player.rect.top
            player.rect.top = HEIGHT // 2
            score += shift * 0.5
            for spr in list(platforms) + list(rockets) + list(monsters):
                if spr != base:
                    spr.rect.y += shift
                    if spr.rect.top >= HEIGHT:
                        spr.kill()

        while len(platforms) < 7:
            new_plat = generate_non_overlapping_platform(-NORMAL_MAX_GAP, 0, score)
            if new_plat:
                platforms.add(new_plat)
                all_sprites.add(new_plat)
            else:
                break

        current_time = pygame.time.get_ticks()

        # Спавн ракеты: появляется после 5000 очков, в верхней части экрана, раз в 45 секунд
        if score >= 5000:
            if last_rocket_spawn_time == 0:
                last_rocket_spawn_time = current_time
            elif current_time - last_rocket_spawn_time >= ROCKET_SPAWN_INTERVAL:
                rx = random.randint(0, WIDTH - 90)
                ry = random.randint(0, 50)
                rocket = Rocket(rx, ry)
                rockets.add(rocket)
                all_sprites.add(rocket)
                last_rocket_spawn_time = current_time

        # Спавн монстров: начинается после 16000 очков
        if score >= 16000:
            if current_time - last_monster_spawn_time_monsters >= MONSTER_SPAWN_INTERVAL:
                r = random.random()
                spawn_count = 0
                if r < 0.10:
                    spawn_count = 3
                elif r < 0.10 + 0.20:
                    spawn_count = 2
                elif r < 0.10 + 0.20 + 0.40:
                    spawn_count = 1
                if spawn_count > 0:
                    for i in range(spawn_count):
                        img = random.choice([MONSTER1_IMG, MONSTER2_IMG, MONSTER3_IMG])
                        x = random.randint(0, WIDTH - img.get_width())
                        y = random.randint(50, 150)
                        monster = Monster(x, y, img)
                        monsters.add(monster)
                        all_sprites.add(monster)
                last_monster_spawn_time_monsters = current_time

        if player.rect.top > HEIGHT:
            game_over = True

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    score_text = FONT.render("Score: " + str(int(score)), True, BLACK)
    screen.blit(score_text, (10, 10))
    if game_over:
        over_text = OVER_FONT.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over_text, ((WIDTH - over_text.get_width()) // 2, HEIGHT - over_text.get_height() - 20))
    pygame.display.flip()
