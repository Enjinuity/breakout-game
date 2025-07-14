import pygame

class PowerUp:
    def __init__(self, x, y, width, height, type_):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 255, 0) if type_ == "life" else (0, 0, 255) if type_ == "big" else (255, 255, 0)
        self.type = type_
        self.dy = 3
        self.active = True

    def update(self):
        self.rect.y += self.dy
        if self.rect.top > 600:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
