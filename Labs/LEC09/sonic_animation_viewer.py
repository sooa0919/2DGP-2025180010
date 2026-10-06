from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

from pico2d import (
    SDLK_LEFT,
    SDLK_RIGHT,
    SDL_KEYDOWN,
    SDL_KEYUP,
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
REPEATS_PER_ANIMATION = 5
TRANSITION_DELAY = 1.0
BACKGROUND_COLOR = (230, 238, 232)
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")


@dataclass(frozen=True)
class AnimationStrip:
    name: str
    top: int
    height: int
    frame_count: int
    moves_with_input: bool = False


ANIMATIONS = (
    AnimationStrip("걷기", 39, 39, 9, True),
    AnimationStrip("달리기", 79, 39, 10, True),
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
    phase: str = "play"
    phase_elapsed: float = 0.0

    def advance_time(self, delta_time, animations):
        remaining_time = max(0.0, delta_time)
        while remaining_time > 0.0:
            if self.phase == "pause":
                pause_remaining = TRANSITION_DELAY - self.phase_elapsed
                consumed_time = min(remaining_time, pause_remaining)
                self.phase_elapsed += consumed_time
                remaining_time -= consumed_time
                if self.phase_elapsed < TRANSITION_DELAY:
                    break

                self.animation_index = (self.animation_index + 1) % len(animations)
                self.frame_index = 0
                self.elapsed = 0.0
                self.completed_cycles = 0
                self.phase = "play"
                self.phase_elapsed = 0.0
                continue

            animation = animations[self.animation_index]
            frame_remaining = FRAME_DURATION - self.elapsed
            consumed_time = min(remaining_time, frame_remaining)
            self.elapsed += consumed_time
            remaining_time -= consumed_time
            if self.elapsed < FRAME_DURATION:
                break

            self.elapsed = 0.0
            if self.frame_index < animation.frame_count - 1:
                self.frame_index += 1
            else:
                self.frame_index = 0
                self.completed_cycles += 1
                if self.completed_cycles >= REPEATS_PER_ANIMATION:
                    self.frame_index = animation.frame_count - 1
                    self.phase = "pause"
                    self.phase_elapsed = 0.0


@dataclass
class MovementInput:
    left_pressed: bool = False
    right_pressed: bool = False

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            is_pressed = True
        elif event.type == SDL_KEYUP:
            is_pressed = False
        else:
            return

        if event.key == SDLK_LEFT:
            self.left_pressed = is_pressed
        elif event.key == SDLK_RIGHT:
            self.right_pressed = is_pressed


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


def validate_animation_map(sprite_sheet, animations=ANIMATIONS):
    if not animations:
        raise ValueError("재생할 애니메이션이 없습니다.")

    for animation in animations:
        if animation.top < 0 or animation.height <= 0:
            raise ValueError(f"{animation.name}의 세로 범위가 올바르지 않습니다.")
        if animation.top + animation.height > sprite_sheet.h:
            raise ValueError(f"{animation.name}의 프레임이 이미지 높이를 벗어납니다.")
        if animation.frame_count <= 0:
            raise ValueError(f"{animation.name}의 프레임 수가 올바르지 않습니다.")
        last_frame_left = (animation.frame_count - 1) * FRAME_WIDTH
        if last_frame_left >= sprite_sheet.w:
            raise ValueError(f"{animation.name}의 프레임이 이미지 너비를 벗어납니다.")


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

        try:
            validate_animation_map(sprite_sheet)
        except ValueError as error:
            print(f"애니메이션 프레임 구성이 올바르지 않습니다: {error}")
            return

        playback = PlaybackState()
        movement_input = MovementInput()
        previous_time = perf_counter()
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                else:
                    movement_input.handle_event(event)

            current_time = perf_counter()
            delta_time = current_time - previous_time
            previous_time = current_time
            playback.advance_time(delta_time, ANIMATIONS)
            animation = ANIMATIONS[playback.animation_index]

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