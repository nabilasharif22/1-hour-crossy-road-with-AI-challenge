# sprites.py
import pygame
from settings import *

class Frog(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Initialize the parent Sprite class
        super().__init__()
        
        # Create the visual representation of the frog (a green square)
        self.image = pygame.Surface((TILE_SIZE - 4, TILE_SIZE - 4))
        self.image.fill(GREEN)
        
        # The 'rect' is used for positioning and collision detection
        self.rect = self.image.get_rect()
        self.start_pos = (x, y)
        self.rect.topleft = self.start_pos
        
        self.on_log = False

    def move(self, dx, dy):
        """Handles grid-based movement"""
        # Calculate new position
        new_x = self.rect.x + (dx * TILE_SIZE)
        new_y = self.rect.y + (dy * TILE_SIZE)

        # Boundary checks: Keep frog inside the screen
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
            self.rect.x = new_x
            self.rect.y = new_y

    def reset_position(self):
        """Sends frog back to start"""
        self.rect.topleft = self.start_pos

    def update(self):
        # We don't need constant updates here because movement is event-based,
        # but we can use this to clamp the frog to the screen if it rides a log off-screen.
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Obstacle(pygame.sprite.Sprite):
    """Used for both Cars and Logs"""
    def __init__(self, x, y, width, color, speed):
        super().__init__()
        self.image = pygame.Surface((width, TILE_SIZE - 4))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed

    def update(self):
        """Move the obstacle and wrap around the screen"""
        self.rect.x += self.speed
        
        # If moving right and goes off screen, move to left side
        if self.speed > 0 and self.rect.left > WIDTH:
            self.rect.right = 0
        
        # If moving left and goes off screen, move to right side
        if self.speed < 0 and self.rect.right < 0:
            self.rect.left = WIDTH