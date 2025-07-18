import pygame

class Paddle:
    def __init__(self, x, y, width, height, color):
        # Initialize paddle as a rectangle
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 7  # Speed of paddle movement

    def move(self, keys, screen_width):
        # Move left if LEFT key is pressed and paddle isn't at the edge
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

        # Move right if RIGHT key is pressed and paddle isn't at the edge
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

    def draw(self, screen):
        # Draw paddle on screen as a rectangle
        pygame.draw.rect(screen, self.color, self.rect)
