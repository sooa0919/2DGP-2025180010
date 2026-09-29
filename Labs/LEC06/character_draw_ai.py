import math

from pico2d import *


open_canvas(800, 600)
character = load_image('character.png')


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)


def move_circle():
    for degree in range(0, 360, 3):
        radians = math.radians(degree)
        x = 400 + 200 * math.cos(radians)
        y = 300 + 200 * math.sin(radians)
        draw_character(x, y)


def move_rectangle():
    for x in range(50, 751, 5):
        draw_character(x, 550)
    for y in range(550, 49, -5):
        draw_character(750, y)
    for x in range(750, 49, -5):
        draw_character(x, 50)
    for y in range(50, 551, 5):
        draw_character(50, y)


while True:
    move_circle()
    move_rectangle()