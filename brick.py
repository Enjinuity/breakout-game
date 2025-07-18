import pygame

class Brick:
    def __init__(self, x, y, width, height, color, points):
        # Create a rectangle to represent the brick
        self.rect = pygame.Rect(x, y, width, height)
        
        self.color = color        # Color of the brick
        self.destroyed = False    # Flag to check if brick is destroyed
        self.points = points      # Points awarded when the brick is hit

    def draw(self, screen):
        # Only draw the brick if it hasn't been destroyed
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, self.rect)           # Fill
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)         # Black border
