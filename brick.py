import pygame

class Brick:
    def __init__(self, x, y, width, height, color, points):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.destroyed = False
        self.points = points


    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # border
