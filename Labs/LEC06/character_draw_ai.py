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


while True:
    move_circle()