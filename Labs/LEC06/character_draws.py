# 실습 과제 진행
## 여기를 채우시오.
from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')

clear_canvas()
character.draw(400, 300)
update_canvas()
delay(1)

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)

def move_circle():
    print("circle")
    for deg in range(0, 360, 5):
        rad = math.radians(deg)
        x = 400 + 200 * math.cos(rad)
        y = 300 + 200 * math.sin(rad)
        draw_character(x, y)
    
def draw_top():
    print("top")
    for x in range(50, 750, 5):
        draw_character(x, 550)
    pass


def draw_right():
    print("right")  
    for y in range(550, 50, -5):
        draw_character(750, y)
    pass

def draw_bottom():
    print("bottom")
    for x in range(750, 50, -5):
        draw_character(x, 50)
    pass

def draw_left():
    print("left")
    pass


def move_rectangle():
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()
    print("rectangle")

def move_triangle():
    print("triangle")


while True:
   # move_circle()
    move_rectangle()
    move_triangle()

    break

close_canvas()