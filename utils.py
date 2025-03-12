# utils.py
import random
from settings import EASY_MIN_GAP, EASY_MAX_GAP, NORMAL_MIN_GAP, NORMAL_MAX_GAP, PLATFORM_SIZE_STANDARD, PLATFORM_SIZE_SMALL

def get_platform_gap(score):
    if score < 2000:
        return (EASY_MIN_GAP, EASY_MAX_GAP)
    else:
        return (NORMAL_MIN_GAP, NORMAL_MAX_GAP)

def get_gravity(score):
    return 0.5

def is_on_platform(player, platforms, epsilon=10):
    for plat in platforms:
        if player.rect.right > plat.rect.left and player.rect.left < plat.rect.right:
            if abs(player.rect.bottom - plat.rect.top) <= epsilon and player.vel_y >= 0:
                return True
    return False

def get_platform_size(score):
    if score >= 16000:
        return PLATFORM_SIZE_SMALL
    else:
        return PLATFORM_SIZE_STANDARD
