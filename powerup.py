import pygame

class PowerUp:
    def __init__(self, x, y, width, height, type_):
        # Create a rectangular power-up object
        self.rect = pygame.Rect(x, y, width, height)

        # Set color based on power-up type
        # Green for extra life, Blue for bigger paddle, Yellow for multiball
        self.color = (0, 255, 0) if type_ == "life" else (0, 0, 255) if type_ == "big" else (255, 255, 0)

        self.type = type_      # Type of power-up: "life", "big", or "multi"
        self.dy = 3            # Falling speed
        self.active = True     # Whether it's still on screen or not

    def update(self):
        # Move power-up down the screen
        self.rect.y += self.dy

        # Deactivate if it falls below the screen
        if self.rect.top > 600:
            self.active = False

    def draw(self, screen):
        # Draw the power-up as a rectangle
        pygame.draw.rect(screen, self.color, self.rect)
