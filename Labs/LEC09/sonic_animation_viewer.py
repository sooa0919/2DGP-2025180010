from dataclasses import dataclass
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
FRAME_WIDTH = 40
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")


@dataclass(frozen=True)
class AnimationStrip:
    name: str
    top: int
    height: int
    frame_count: int


ANIMATIONS = (
    AnimationStrip("동작 01", 39, 39, 9),
    AnimationStrip("동작 02", 79, 39, 10),
    AnimationStrip("동작 03", 121, 43, 7),
    AnimationStrip("동작 04", 167, 33, 8),
    AnimationStrip("동작 05", 206, 27, 5),
    AnimationStrip("동작 06", 238, 36, 6),
    AnimationStrip("동작 07", 283, 35, 7),
    AnimationStrip("동작 08", 326, 45, 7),
    AnimationStrip("동작 09", 377, 40, 7),
    AnimationStrip("동작 10", 426, 43, 4),
)


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