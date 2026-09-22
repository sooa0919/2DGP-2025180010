# 실습 과제 진행
## 여기를 채우시오.
from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')


def move_circle():
    print("circle")

def move_rectangle():
    print("rectangle")

def move_triangle():
    print("triangle")


while True:
    move_circle()
    move_rectangle()
    move_triangle()

    break

close_canvas()