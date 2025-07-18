import pygame

class Ball:
    def __init__(self, x, y, radius, color):
        # Set initial position and appearance
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        # Set initial speed (dx = horizontal, dy = vertical)
        self.dx = 5  # Moves right initially
        self.dy = -5 # Moves upward initially

    def move(self):
        # Update ball position based on speed
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        # Draw the ball on screen as a filled circle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def bounce_wall(self, screen_width, screen_height, wall_sound):
        # Bounce off left or right walls
        if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
            self.dx *= -1  # Reverse horizontal direction
            wall_sound.play()

        # Bounce off top wall
        if self.y - self.radius <= 0:
            self.dy *= -1  # Reverse vertical direction
            wall_sound.play()

    def bounce_paddle(self, paddle_rect, paddle_sound):
        # Check if ball hits paddle while moving downward
        if paddle_rect.collidepoint(self.x, self.y + self.radius) and self.dy > 0:
            self.dy *= -1  # Bounce upward
            paddle_sound.play()

    def reset(self, x, y):
        # Reset ball to given position and speed
        self.x = x
        self.y = y
        self.dx = 4
        self.dy = -4
