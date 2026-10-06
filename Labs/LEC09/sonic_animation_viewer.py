from pico2d import close_canvas, delay, open_canvas


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        delay(1)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()