# main.py
import pygame
import sys
from settings import *
from sprites import Frog, Obstacle

# 1. Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Frogger")
clock = pygame.time.Clock()

# 2. Group Setup
# Groups help us update and draw many objects at once
all_sprites = pygame.sprite.Group()
cars = pygame.sprite.Group()
logs = pygame.sprite.Group()

# 3. Create Objects

# Create the Player
player = Frog(WIDTH // 2 - TILE_SIZE // 2, HEIGHT - TILE_SIZE)
all_sprites.add(player)

# Create Cars (Rows 8 to 12)
# We loop through rows and create cars with alternating speeds
for row in range(8, 13):
    y_pos = row * TILE_SIZE
    # Alternating direction based on even/odd row
    speed = 3 if row % 2 == 0 else -3
    
    # Create 2 cars per lane
    car1 = Obstacle(0, y_pos, TILE_SIZE * 2, RED, speed)
    car2 = Obstacle(WIDTH // 2, y_pos, TILE_SIZE * 2, RED, speed)
    
    cars.add(car1, car2)
    all_sprites.add(car1, car2)

# Create Logs (Rows 2 to 6)
for row in range(2, 7):
    y_pos = row * TILE_SIZE
    speed = 2 if row % 2 == 0 else -2
    
    # Create 2 logs per lane, make them wider than cars
    log1 = Obstacle(0, y_pos, TILE_SIZE * 3, BROWN, speed)
    log2 = Obstacle(WIDTH // 2 + 100, y_pos, TILE_SIZE * 3, BROWN, speed)
    
    logs.add(log1, log2)
    all_sprites.add(log1, log2)

# --- GAME LOOP ---
running = True
while running:
    # A. Event Handling (Input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Move frog only on Key Press (not hold)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move(0, -1)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1)
            elif event.key == pygame.K_LEFT:
                player.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)

    # B. Update everything
    all_sprites.update()

    # C. Collision Logic
    
    # 1. Car Collision (Instant Death)
    # spritecollide checks if 'player' hits anything in 'cars' group
    # The 'False' argument means "do not delete the car on hit"
    if pygame.sprite.spritecollide(player, cars, False):
        print("Hit by car!")
        player.reset_position()

    # 2. Water/Log Logic
    # First, check if player is in the river area
    if RIVER_TOP <= player.rect.y < RIVER_BOTTOM:
        # Check if touching a log
        # hitting_log will be a list of logs the player is touching
        hitting_log = pygame.sprite.spritecollide(player, logs, False)
        
        if hitting_log:
            # Move the frog at the same speed as the log
            # We grab the first log in the list [0]
            player.rect.x += hitting_log[0].speed
        else:
            # In river but NOT on a log = Drown
            print("Drowned!")
            player.reset_position()

    # D. Win Condition (Reached Top)
    if player.rect.top < TILE_SIZE:
        print("You Win!")
        player.reset_position()

    # E. Drawing
    screen.fill(BLACK) # Clear screen
    
    # Draw simple background strips for Road and River
    # (Rect arguments: x, y, width, height)
    pygame.draw.rect(screen, BLUE, (0, RIVER_TOP, WIDTH, RIVER_BOTTOM - RIVER_TOP))
    pygame.draw.rect(screen, GRAY, (0, ROAD_TOP, WIDTH, ROAD_BOTTOM - ROAD_TOP))
    
    # Draw all sprites on top of background
    all_sprites.draw(screen)

    pygame.display.flip() # Update the display
    clock.tick(FPS)       # Keep consistent speed

pygame.quit()
sys.exit()