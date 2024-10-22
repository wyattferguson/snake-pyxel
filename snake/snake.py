from dataclasses import dataclass

import pyxel


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# Scale of Game Board
PIXEL_SCALE = 4

# Colors
COL_BACKGROUND = 0
COL_APPLE = 8
COL_SNAKE = 3
COL_BODY = 11

# Movement Directions
UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)


class Snake:
    def __init__(self):
        pyxel.init(120, 120)
        self.speed = PIXEL_SCALE
        self.reset()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.frame_count % self.speed == 0:
            self.keyboard()
            if not self.dead:
                snake_head = self.snake.pop()
                new_head = Point(
                    snake_head.x + self.direction.x, snake_head.y + self.direction.y
                )
                self.dead = self.check_death(new_head)
                if self.apple_collision(new_head):
                    pass
                self.snake.insert(0, new_head)

    def reset(self):
        self.snake = [Point(2, 2)]
        self.dead = False
        self.direction = RIGHT
        self.apple = self.new_apple()

    def keyboard(self):
        """Watch keyboard for WASD and (R)Reset"""
        if pyxel.btn(pyxel.KEY_W):
            if self.direction is not DOWN:
                self.direction = UP
        elif pyxel.btn(pyxel.KEY_S):
            if self.direction is not UP:
                self.direction = DOWN
        elif pyxel.btn(pyxel.KEY_A):
            if self.direction is not RIGHT:
                self.direction = LEFT
        elif pyxel.btn(pyxel.KEY_D):
            if self.direction is not LEFT:
                self.direction = RIGHT
        elif pyxel.btn(pyxel.KEY_R):
            self.reset()

    def draw(self):
        if not self.dead:
            pyxel.cls(COL_BACKGROUND)
            for body in self.snake:
                pyxel.rect(
                    body.x * PIXEL_SCALE,
                    body.y * PIXEL_SCALE,
                    PIXEL_SCALE,
                    PIXEL_SCALE,
                    COL_SNAKE,
                )
            pyxel.rect(
                self.apple.x * PIXEL_SCALE,
                self.apple.y * PIXEL_SCALE,
                PIXEL_SCALE,
                PIXEL_SCALE,
                COL_APPLE,
            )

    def apple_collision(self, snake_head: Point):
        if snake_head == self.apple:
            print("HIT APPLE")
            self.apple = self.new_apple()

    def check_death(self, snake_head: Point) -> bool:
        # Has snake crashed into its self
        for part in self.snake:
            if part == snake_head:
                print("HIT BODY")
                return True

        # Has snake hit a wall
        if (
            snake_head.x < 0
            or snake_head.x > pyxel.width // PIXEL_SCALE
            or snake_head.y < 0
            or snake_head.y > pyxel.height // PIXEL_SCALE
        ):
            # print("HIT WALL")
            return True

        return False

    def new_apple(self) -> Point:
        y = pyxel.rndi(PIXEL_SCALE, (pyxel.height - 1) // PIXEL_SCALE)
        x = pyxel.rndi(PIXEL_SCALE, (pyxel.width - 1) // PIXEL_SCALE)
        # print(f"APPLE: {y}, {x}")
        return Point(x, y)


if __name__ == "__main__":
    Snake()
