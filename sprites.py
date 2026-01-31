# sprites.py
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # We make the surface taller (50px) to fit the 3D height
        self.image = pygame.Surface((40, 50), pygame.SRCALPHA)
        
        # --- DRAW 3D CHICKEN ---
        # 1. Shadow/Side (The 3D thickness)
        pygame.draw.rect(self.image, CHICKEN_SHADOW, (5, 20, 30, 25)) 
        
        # 2. Main Body (Top Face) - Shifted Up by 5 pixels
        pygame.draw.rect(self.image, CHICKEN_WHITE, (5, 15, 30, 25))
        
        # 3. Details
        # Wing
        pygame.draw.rect(self.image, (200, 200, 200), (5, 25, 30, 10))
        # Comb (Red head)
        pygame.draw.rect(self.image, COMB_RED, (15, 5, 10, 10))
        # Beak
        pygame.draw.rect(self.image, BEAK_ORANGE, (30, 20, 10, 5))
        # Legs
        pygame.draw.rect(self.image, BEAK_ORANGE, (10, 40, 5, 5))
        pygame.draw.rect(self.image, BEAK_ORANGE, (25, 40, 5, 5))

        self.rect = self.image.get_rect()
        # Visual offset to align the "feet" with the grid
        self.rect.topleft = (x + 5, y - 5) 

    def move(self, dx, dy):
        # 1. Snap X to Grid
        current_grid_x = round(self.rect.x / TILE_SIZE)
        target_grid_x = current_grid_x + dx
        new_x = (target_grid_x * TILE_SIZE) + 5
        
        if 0 <= target_grid_x < (WIDTH // TILE_SIZE):
            self.rect.x = new_x
            # Simple Flip
            if dx > 0: self.image = pygame.transform.flip(self.original_image, False, False)
            elif dx < 0: self.image = pygame.transform.flip(self.original_image, True, False)

        # 2. Free Movement Y (For scrolling)
        new_y = self.rect.y + (dy * TILE_SIZE)
        
        if dy > 0: # Back
             if new_y < HEIGHT: self.rect.y = new_y
             return False 
        
        if dy < 0: # Forward
            self.rect.y = new_y
            return True 
        return False
    
    @property
    def original_image(self):
        # Helper to redraw for flipping
        img = pygame.Surface((40, 50), pygame.SRCALPHA)
        pygame.draw.rect(img, CHICKEN_SHADOW, (5, 20, 30, 25)) 
        pygame.draw.rect(img, CHICKEN_WHITE, (5, 15, 30, 25))
        pygame.draw.rect(img, (200, 200, 200), (5, 25, 30, 10))
        pygame.draw.rect(img, COMB_RED, (15, 5, 10, 10))
        pygame.draw.rect(img, BEAK_ORANGE, (30, 20, 10, 5))
        pygame.draw.rect(img, BEAK_ORANGE, (10, 40, 5, 5))
        pygame.draw.rect(img, BEAK_ORANGE, (25, 40, 5, 5))
        return img

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        width = 60
        height = 40 # Taller for 3D effect
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        base_color = (220, 60, 60) # Bright Red
        shadow_color = (160, 40, 40) # Dark Red

        # 1. Draw Shadow (Side/Bottom)
        pygame.draw.rect(self.image, shadow_color, (0, 15, width, 20))
        
        # 2. Draw Top Body (Shifted up 8px)
        pygame.draw.rect(self.image, base_color, (0, 7, width, 20))
        
        # 3. Windows / Roof
        pygame.draw.rect(self.image, (150, 200, 255), (10, 0, width-20, 12))
        
        # 4. Wheels
        pygame.draw.rect(self.image, BLACK, (5, 28, 12, 12))
        pygame.draw.rect(self.image, BLACK, (width-17, 28, 12, 12))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y + 5)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > WIDTH: self.rect.right = 0
        if self.speed < 0 and self.rect.right < 0: self.rect.left = WIDTH

class Log(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        width = 100
        height = 40
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # 1. Side (Darker Wood)
        pygame.draw.rect(self.image, LOG_SIDE, (0, 10, width, 25))
        # 2. Top (Lighter Wood)
        pygame.draw.rect(self.image, LOG_TOP, (0, 0, width, 25))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y + 5)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > WIDTH: self.rect.right = 0
        if self.speed < 0 and self.rect.right < 0: self.rect.left = WIDTH

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 60), pygame.SRCALPHA)
        
        # Trunk Side
        pygame.draw.rect(self.image, (100, 50, 10), (15, 35, 20, 20))
        # Trunk Top
        pygame.draw.rect(self.image, TRUNK_TOP, (15, 30, 20, 20))
        
        # Leaves Side (Dark Green Shadow)
        pygame.draw.rect(self.image, TREE_SIDE, (5, 10, 40, 25))
        # Leaves Top (Bright Green)
        pygame.draw.rect(self.image, TREE_TOP, (5, 0, 40, 25))

        self.rect = self.image.get_rect()
        # Offset to center on tile
        self.rect.topleft = (x, y - 10)

class Lane(pygame.sprite.Sprite):
    def __init__(self, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((WIDTH, TILE_SIZE))
        
        if self.type == LANE_GRASS:
            # Main Grass
            self.image.fill(GRASS_TOP)
            # Bottom edge shadow (fake 3D height for the ground layer)
            pygame.draw.rect(self.image, GRASS_SIDE, (0, TILE_SIZE-5, WIDTH, 5))
            
        elif self.type == LANE_ROAD:
            self.image.fill(ROAD_TOP)
            pygame.draw.rect(self.image, ROAD_SIDE, (0, TILE_SIZE-5, WIDTH, 5))
            # Markings
            pygame.draw.line(self.image, WHITE, (0, 5), (WIDTH, 5), 2)
            pygame.draw.line(self.image, WHITE, (0, TILE_SIZE-10), (WIDTH, TILE_SIZE-10), 2)
            
        elif self.type == LANE_WATER:
            self.image.fill(WATER_TOP)
            # Water looks deeper with a dark bottom edge
            pygame.draw.rect(self.image, WATER_DEEP, (0, TILE_SIZE-10, WIDTH, 10))
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, y)