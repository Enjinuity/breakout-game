import pygame

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = 5  # Horizontal speed
        self.dy = -5 # Vertical speed

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def bounce_wall(self, screen_width, screen_height, wall_sound):
        if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
            self.dx *= -1
            wall_sound.play()

        if self.y - self.radius <= 0:
            self.dy *= -1
            wall_sound.play()

    def bounce_paddle(self, paddle_rect, paddle_sound):
        if paddle_rect.collidepoint(self.x, self.y + self.radius) and self.dy > 0:
            self.dy *= -1
            paddle_sound.play()

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.dx = 4
        self.dy = -4
