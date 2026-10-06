from pathlib import Path

from pico2d import (
    SDL_QUIT,
    clear_canvas,
    close_canvas,
    delay,
    get_events,
    load_image,
    open_canvas,
    update_canvas,
)


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")


def main():
    if not SPRITE_PATH.is_file():
        print(f"스프라이트 이미지를 찾을 수 없습니다: {SPRITE_PATH}")
        return

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        try:
            sprite_sheet = load_image(str(SPRITE_PATH))
        except Exception as error:
            print(f"스프라이트 이미지를 불러오지 못했습니다: {error}")
            return

        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False

            clear_canvas()
            update_canvas()
            delay(1 / 60)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()