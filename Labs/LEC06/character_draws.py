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
    for deg in range(0, 360, 3):
        rad = math.radians(deg)
        x = 400 + 200 * math.cos(rad)
        y = 300 + 200 * math.sin(rad)
        draw_character(x, y)
    
def draw_top():
    for x in range(50, 750, 7):
        draw_character(x, 550)
    pass


def draw_right(): 
    for y in range(550, 50, -7):
        draw_character(750, y)
    pass

def draw_bottom():
    for x in range(750, 50, -7):
        draw_character(x, 50)
    pass

def draw_left():
    for y in range(50, 550, 7):
        draw_character(50, y)
    pass


def move_rectangle():
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()
    


def draw_leftUp():
    for x in range(50, 400, 5):
        y = 50 + (x - 50) * (250 / 350)
        draw_character(x, y)
    pass

def draw_rightDown():
    for x in range(400, 750, 5):
            y = 250 - (x - 400) * (200 / 350)
            draw_character(x, y)
    pass

def draw_bottomTriangle():
    for x in range(750, 50, -5):
        draw_character(x, 50)
    pass



def move_triangle():
    draw_leftUp()
    draw_rightDown()
    draw_bottomTriangle()
    


while True:
    move_circle()
    move_rectangle()
    move_triangle()


close_canvas()