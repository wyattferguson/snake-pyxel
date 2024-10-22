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
COL_SCORE = 10

# Movement Directions
UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)


class Snake:
    def __init__(self):
        pyxel.init(75, 100, title="Snake!Snake!Snake!")
        self.reset()
        pyxel.run(self.update, self.draw)

    def update(self):
        """Update game state every frame"""
        if pyxel.frame_count % self.speed == 0:
            self.keyboard()
            if not self.dead:
                snake_head = self.snake[0]
                new_head = Point(
                    snake_head.x + self.direction.x, snake_head.y + self.direction.y
                )

                self.dead = self.check_death(new_head)
                self.snake.insert(0, new_head)
                if not self.apple_collision(new_head):
                    self.snake.pop()

    def reset(self):
        """Full game restart"""
        self.snake = [Point(2, 2)]
        self.speed = PIXEL_SCALE
        self.dead = False
        self.score = 0
        self.direction = RIGHT
        self.apple = self.new_apple()

    def keyboard(self):
        """Watch keyboard for WASD and R(Reset)"""
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
        """Redraw game board and sprites"""

        # clear screen
        pyxel.cls(COL_BACKGROUND)

        if not self.dead:
            # draw snake body
            for body in self.snake:
                pyxel.rect(
                    body.x * PIXEL_SCALE,
                    body.y * PIXEL_SCALE,
                    PIXEL_SCALE,
                    PIXEL_SCALE,
                    COL_SNAKE,
                )

            # draw apple
            pyxel.rect(
                self.apple.x * PIXEL_SCALE,
                self.apple.y * PIXEL_SCALE,
                PIXEL_SCALE,
                PIXEL_SCALE,
                COL_APPLE,
            )

            # draw score
            pyxel.text(1, 1, f"{self.score:03}", COL_SCORE)
        else:
            # show gameover
            pyxel.text(pyxel.width // 4, 20, "GAME OVER", COL_SCORE)
            pyxel.text(7, 30, "'R' TO RESTART", COL_SCORE)

    def apple_collision(self, snake_head: Point) -> bool:
        """Has the snake head hit an apple"""
        if snake_head == self.apple:
            self.apple = self.new_apple()
            self.score += 1
            return True
        return False

    def check_death(self, snake_head: Point) -> bool:
        # Has snake crashed into its self
        for part in self.snake:
            if part == snake_head:
                return True

        # Has snake hit a wall
        if (
            snake_head.x < 0
            or snake_head.x == pyxel.width // PIXEL_SCALE
            or snake_head.y < 0
            or snake_head.y == pyxel.height // PIXEL_SCALE
        ):
            return True

        return False

    def new_apple(self) -> Point:
        """Generate a new apple at a random X,Y"""
        y = pyxel.rndi(PIXEL_SCALE, (pyxel.height - PIXEL_SCALE) // PIXEL_SCALE)
        x = pyxel.rndi(PIXEL_SCALE, (pyxel.width - PIXEL_SCALE) // PIXEL_SCALE)
        return Point(x, y)


if __name__ == "__main__":
    Snake()
