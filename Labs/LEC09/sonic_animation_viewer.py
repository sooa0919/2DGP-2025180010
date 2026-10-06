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


CANVAS_WIDTH = 1400
CANVAS_HEIGHT = 700
GROUND_Y = 60
FRAME_DURATION = 0.1
REPEATS_PER_ANIMATION = 5
TRANSITION_DELAY = 1.0
MOVEMENT_SPEED = 240.0
BACKGROUND_COLOR = (230, 238, 232)
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")


@dataclass(frozen=True)
class SpriteFrame:
    left: int
    top: int
    width: int
    height: int


def frame_from_bounds(left, top, right, bottom):
    return SpriteFrame(left, top, right - left + 1, bottom - top + 1)


@dataclass(frozen=True)
class AnimationStrip:
    name: str
    frames: tuple[SpriteFrame, ...]
    moves_with_input: bool = False

    @property
    def frame_count(self):
        return len(self.frames)

    @property
    def height(self):
        return max(frame.height for frame in self.frames)


ANIMATIONS = (
    AnimationStrip(
        "걷기",
        (
            frame_from_bounds(1, 39, 29, 77),
            frame_from_bounds(31, 40, 56, 77),
            frame_from_bounds(58, 39, 85, 77),
            frame_from_bounds(86, 40, 115, 77),
            frame_from_bounds(118, 40, 147, 77),
            frame_from_bounds(150, 40, 179, 77),
            frame_from_bounds(182, 40, 210, 77),
            frame_from_bounds(211, 39, 239, 76),
            frame_from_bounds(240, 39, 268, 76),
            frame_from_bounds(270, 45, 293, 76),
            frame_from_bounds(302, 51, 330, 76),
        ),
        True,
    ),
    AnimationStrip(
        "달리기",
        (
            frame_from_bounds(8, 80, 33, 116),
            frame_from_bounds(37, 80, 63, 116),
            frame_from_bounds(65, 80, 95, 117),
            frame_from_bounds(97, 80, 133, 116),
            frame_from_bounds(135, 80, 166, 114),
            frame_from_bounds(170, 79, 201, 116),
            frame_from_bounds(206, 79, 231, 116),
            frame_from_bounds(238, 80, 261, 116),
            frame_from_bounds(263, 80, 292, 116),
            frame_from_bounds(295, 80, 330, 116),
            frame_from_bounds(334, 80, 365, 115),
            frame_from_bounds(370, 79, 398, 116),
        ),
        True,
    ),
    AnimationStrip(
        "동작 03",
        (
            frame_from_bounds(1, 124, 33, 163),
            frame_from_bounds(39, 124, 73, 162),
            frame_from_bounds(89, 125, 123, 162),
            frame_from_bounds(130, 121, 163, 162),
            frame_from_bounds(181, 122, 214, 162),
            frame_from_bounds(228, 122, 260, 161),
        ),
    ),
    AnimationStrip(
        "동작 04",
        (
            frame_from_bounds(1, 169, 29, 198),
            frame_from_bounds(35, 167, 63, 197),
            frame_from_bounds(67, 169, 96, 197),
            frame_from_bounds(98, 169, 128, 197),
            frame_from_bounds(131, 168, 159, 197),
            frame_from_bounds(162, 168, 190, 198),
            frame_from_bounds(193, 170, 222, 198),
            frame_from_bounds(230, 170, 260, 198),
            frame_from_bounds(268, 170, 297, 199),
        ),
    ),
    AnimationStrip(
        "동작 05",
        (
            frame_from_bounds(1, 206, 30, 232),
            frame_from_bounds(36, 206, 64, 232),
            frame_from_bounds(70, 206, 98, 232),
            frame_from_bounds(105, 206, 133, 232),
            frame_from_bounds(139, 206, 167, 232),
            frame_from_bounds(174, 206, 202, 232),
        ),
    ),
    AnimationStrip(
        "동작 06",
        (
            frame_from_bounds(1, 239, 29, 273),
            frame_from_bounds(36, 239, 65, 273),
            frame_from_bounds(74, 239, 104, 273),
            frame_from_bounds(111, 238, 141, 273),
            frame_from_bounds(149, 239, 178, 273),
            frame_from_bounds(186, 238, 216, 273),
        ),
    ),
    AnimationStrip(
        "동작 07",
        (
            frame_from_bounds(1, 283, 29, 317),
            frame_from_bounds(36, 283, 65, 317),
            frame_from_bounds(72, 286, 110, 316),
            frame_from_bounds(123, 285, 161, 316),
            frame_from_bounds(172, 286, 210, 316),
            frame_from_bounds(218, 285, 255, 316),
        ),
    ),
    AnimationStrip(
        "동작 08",
        (
            frame_from_bounds(1, 326, 24, 370),
            frame_from_bounds(31, 327, 59, 370),
            frame_from_bounds(65, 327, 84, 370),
            frame_from_bounds(90, 327, 114, 369),
            frame_from_bounds(119, 327, 143, 369),
            frame_from_bounds(149, 327, 168, 370),
            frame_from_bounds(184, 341, 223, 368),
            frame_from_bounds(232, 341, 270, 367),
        ),
    ),
    AnimationStrip(
        "동작 09",
        (
            frame_from_bounds(1, 379, 27, 416),
            frame_from_bounds(31, 379, 61, 414),
            frame_from_bounds(64, 379, 94, 414),
            frame_from_bounds(99, 377, 131, 414),
            frame_from_bounds(136, 379, 167, 414),
            frame_from_bounds(176, 379, 208, 414),
            frame_from_bounds(217, 379, 249, 414),
            frame_from_bounds(254, 378, 286, 413),
        ),
    ),
    AnimationStrip(
        "동작 10",
        (
            frame_from_bounds(6, 429, 39, 468),
            frame_from_bounds(49, 426, 82, 468),
            frame_from_bounds(96, 427, 118, 465),
            frame_from_bounds(125, 427, 147, 465),
        ),
    ),
)
VIEWER_PADDING = 40
MAX_FRAME_WIDTH = max(frame.width for item in ANIMATIONS for frame in item.frames)
MAX_FRAME_HEIGHT = max(frame.height for item in ANIMATIONS for frame in item.frames)
SPRITE_SCALE = min(
    (CANVAS_WIDTH - 2 * VIEWER_PADDING) // MAX_FRAME_WIDTH,
    (CANVAS_HEIGHT - 2 * VIEWER_PADDING) // MAX_FRAME_HEIGHT,
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
        locomotion_time = 0.0
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
            if animation.moves_with_input:
                locomotion_time += consumed_time
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
        return locomotion_time


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


@dataclass
class MovementState:
    x: float = CANVAS_WIDTH / 2
    facing_left: bool = False

    def update(self, delta_time, movement_input, movement_enabled):
        direction = int(movement_input.right_pressed) - int(movement_input.left_pressed)
        if movement_enabled:
            self.x += direction * MOVEMENT_SPEED * max(0.0, delta_time)
            if direction:
                self.facing_left = direction < 0
        half_width = MAX_FRAME_WIDTH * SPRITE_SCALE / 2
        self.x = min(max(self.x, half_width), CANVAS_WIDTH - half_width)


def draw_frame(
    sprite_sheet,
    animation,
    frame_index,
    center_x=CANVAS_WIDTH // 2,
    facing_left=False,
):
    if not 0 <= frame_index < animation.frame_count:
        raise IndexError("프레임 인덱스가 애니메이션 범위를 벗어났습니다.")

    frame = animation.frames[frame_index]
    source_bottom = sprite_sheet.h - frame.top - frame.height
    draw_width = frame.width * SPRITE_SCALE
    draw_height = frame.height * SPRITE_SCALE
    sprite_sheet.clip_composite_draw(
        frame.left,
        source_bottom,
        frame.width,
        frame.height,
        0.0,
        "h" if facing_left else "",
        center_x,
        GROUND_Y + draw_height / 2,
        draw_width,
        draw_height,
    )


def validate_animation_map(sprite_sheet, animations=ANIMATIONS):
    if not animations:
        raise ValueError("재생할 애니메이션이 없습니다.")

    for animation in animations:
        if animation.frame_count <= 0:
            raise ValueError(f"{animation.name}의 프레임 수가 올바르지 않습니다.")
        for frame in animation.frames:
            if frame.left < 0 or frame.top < 0 or frame.width <= 0 or frame.height <= 0:
                raise ValueError(f"{animation.name}의 프레임 범위가 올바르지 않습니다.")
            if frame.left + frame.width > sprite_sheet.w:
                raise ValueError(f"{animation.name}의 프레임이 이미지 너비를 벗어납니다.")
            if frame.top + frame.height > sprite_sheet.h:
                raise ValueError(f"{animation.name}의 프레임이 이미지 높이를 벗어납니다.")


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
        movement = MovementState()
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
            locomotion_time = playback.advance_time(delta_time, ANIMATIONS)
            animation = ANIMATIONS[playback.animation_index]
            movement.update(
                locomotion_time,
                movement_input,
                locomotion_time > 0.0,
            )

            clear_canvas()
            draw_rectangle(
                0,
                0,
                CANVAS_WIDTH - 1,
                CANVAS_HEIGHT - 1,
                *BACKGROUND_COLOR,
                filled=True,
            )
            draw_frame(
                sprite_sheet,
                animation,
                playback.frame_index,
                movement.x,
                movement.facing_left,
            )
            update_canvas()
            delay(1 / 60)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()