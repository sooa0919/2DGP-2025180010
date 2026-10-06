from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from pico2d import (
    SDL_QUIT,
    clear_canvas,
    close_canvas,
    delay,
    draw_rectangle,
    get_events,
    load_image,
    open_canvas,
    update_canvas,
)


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FRAME_WIDTH = 40
FRAME_DURATION = 0.1
BACKGROUND_COLOR = (230, 238, 232)
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
VIEWER_PADDING = 40
SPRITE_SCALE = min(
    (CANVAS_WIDTH - 2 * VIEWER_PADDING) // FRAME_WIDTH,
    (CANVAS_HEIGHT - 2 * VIEWER_PADDING) // max(item.height for item in ANIMATIONS),
)


@dataclass
class PlaybackState:
    animation_index: int = 0
    frame_index: int = 0
    elapsed: float = 0.0
    completed_cycles: int = 0

    def advance_time(self, delta_time, animation):
        self.elapsed += max(0.0, delta_time)
        while self.elapsed >= FRAME_DURATION:
            self.elapsed -= FRAME_DURATION
            if self.frame_index < animation.frame_count - 1:
                self.frame_index += 1
            else:
                self.frame_index = 0
                self.completed_cycles += 1


def draw_frame(sprite_sheet, animation, frame_index):
    if not 0 <= frame_index < animation.frame_count:
        raise IndexError("프레임 인덱스가 애니메이션 범위를 벗어났습니다.")

    source_left = frame_index * FRAME_WIDTH
    source_width = min(FRAME_WIDTH, sprite_sheet.w - source_left)
    source_bottom = sprite_sheet.h - animation.top - animation.height
    sprite_sheet.clip_draw(
        source_left,
        source_bottom,
        source_width,
        animation.height,
        CANVAS_WIDTH // 2,
        CANVAS_HEIGHT // 2,
        source_width * SPRITE_SCALE,
        animation.height * SPRITE_SCALE,
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

        playback = PlaybackState()
        previous_time = perf_counter()
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False

            current_time = perf_counter()
            delta_time = current_time - previous_time
            previous_time = current_time
            animation = ANIMATIONS[playback.animation_index]
            playback.advance_time(delta_time, animation)

            clear_canvas()
            draw_rectangle(
                0,
                0,
                CANVAS_WIDTH - 1,
                CANVAS_HEIGHT - 1,
                *BACKGROUND_COLOR,
                filled=True,
            )
            draw_frame(sprite_sheet, animation, playback.frame_index)
            update_canvas()
            delay(1 / 60)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()