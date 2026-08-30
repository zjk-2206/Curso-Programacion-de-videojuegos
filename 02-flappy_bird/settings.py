"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the game settings that include the association of the
inputs with an their ids, constants of values to set up the game, sounds,
textures, and fonts.
"""

from pathlib import Path

import pygame

from gale import input_handler

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "confirm")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_SPACE, "jump")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_TAB, "pause_tab")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_DOWN, "down")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_UP, "up")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "left")


TITLE = "Flappy Bird"

# Size of our actual window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Size we are trying to emulate
VIRTUAL_WIDTH = 512
VIRTUAL_HEIGHT = 288

BIRD_WIDTH = 39
BIRD_HEIGHT = 28

LOG_WIDTH = 70
LOG_HEIGHT = 288
LOGS_GAP = 90
POWER_UP_WIDTH = 15
POWER_UP_HEIGHT = 15


GROUND_HEIGHT = 16

BACKGROUND_LOOPING_POINT = 1157

MAIN_SCROLL_SPEED = 100
BACK_SCROLL_SPEED = 50  # MAIN_SCROLL_SPEED / 2
UP_SCROLL_LOGS_SPEED = 60

GRAVITY = 980
JUMP_TAKEOFF_SPEED = GRAVITY / 6
BIRD_SPEED = 80.0

TIME_TO_SPAWN_LOGS = 1.5
TIME_TO_SPAWN_LOGS_HARD_1 = 1.4
TIME_TO_SPAWN_LOGS_HARD_2 = 1.7
TIME_TO_SPAWN_POWERUP = 1.5
PROBABILITY_TO_SPAWN_POWERUP = 10
TIME_POWERUP = 6

MEDIUM_TEXT_SIZE = 18
HUGE_TEXT_SIZE = 56
FLAPPY_TEXT_SIZE = 28

BASE_DIR = Path(__file__).parent

TEXTURES = {
    "bird": pygame.image.load(BASE_DIR / "assets" / "graphics" / "bird.png"),
    "background": pygame.image.load(BASE_DIR / "assets" / "graphics" / "background.png"),
    "ground": pygame.image.load(BASE_DIR / "assets" / "graphics" / "ground.png"),
    "log": pygame.image.load(BASE_DIR / "assets" / "graphics" / "log.png"),
    "powerup":pygame.image.load(BASE_DIR / "assets" / "graphics" / "PowerUp.png"),
    "deathbird":pygame.image.load(BASE_DIR / "assets" / "graphics" / "death_bird.png"),
}
# The top log of every pair is the same image, flipped upside down.
TEXTURES["log_inverted"] = pygame.transform.flip(TEXTURES["log"], False, True)

SOUNDS = {
    "jump": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "jump.wav"),
    "explosion": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "explosion.wav"),
    "hurt": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "pik_audio.wav"),
    "score": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "score.wav"),
    "pause": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "smth-inforamtion-5.wav"),
    "crash": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "classic_hurt.wav"),
    "powerup_take": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "powerup_take.wav"),
    "music_powerup": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "music_powerup.wav"),
}


pygame.mixer.music.load(BASE_DIR / "assets" / "sounds" / "marios_way.ogg")


FONTS = {
    "medium": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", MEDIUM_TEXT_SIZE),
    "huge": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "font.ttf", HUGE_TEXT_SIZE),
    "flappy": pygame.font.Font(
        BASE_DIR / "assets" / "fonts" / "flappy.ttf", FLAPPY_TEXT_SIZE
    ),
}

COLOR_BACKGROUND = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 215, 0)

