# main.py
import pygame
import sys
import random
import os
from settings import *
from sprites import Player, Car, Log, Tree, Lane

# Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crossy Road 3D Voxel")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30, bold=True)
game_over_font = pygame.font.SysFont("Arial", 60, bold=True)

# Groups
all_sprites = pygame.sprite.Group()
lanes = pygame.sprite.Group()
cars = pygame.sprite.Group()
logs = pygame.sprite.Group()
trees = pygame.sprite.Group()

# Variables
score = 0
high_score = 0
game_state = "playing"

# --- CONFIGURATION ---
# Slower scroll for smoother feel
SCROLL_SPEED = 0.2  
scroll_accumulator = 0.0

def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try: return int(f.read())
            except: return 0
    return 0

def save_high_score(new_score):
    with open("highscore.txt", "w") as f:
        f.write(str(new_score))

high_score = load_high_score()

def create_lane(y_pos, is_start=False):
    if is_start:
        lane_type = LANE_GRASS
    else:
        lane_type = random.choices([LANE_GRASS, LANE_ROAD, LANE_WATER], weights=[4, 3, 3])[0]

    lane = Lane(y_pos, lane_type)
    lanes.add(lane)
    all_sprites.add(lane)

    if lane_type == LANE_ROAD:
        direction = random.choice([-1, 1])
        speed = random.randint(2, 5) * direction
        for i in range(random.randint(1, 2)):
            # Random X position
            x_pos = random.randint(0, WIDTH)
            car = Car(x_pos, y_pos, speed)
            cars.add(car)
            all_sprites.add(car)
            
    elif lane_type == LANE_WATER:
        direction = random.choice([-1, 1])
        speed = random.randint(2, 4) * direction
        for i in range(random.randint(1, 3)): # More logs
            x_pos = random.randint(0, WIDTH)
            log = Log(x_pos, y_pos, speed)
            logs.add(log)
            all_sprites.add(log)
            
    elif lane_type == LANE_GRASS:
        if random.random() < 0.4: # 40% chance of tree
            # Snap tree to grid
            x_pos = random.choice(range(0, WIDTH, TILE_SIZE))
            tree = Tree(x_pos, y_pos)
            trees.add(tree)
            all_sprites.add(tree)

def reset_game():
    global score, player, game_state, scroll_accumulator, SCROLL_SPEED
    all_sprites.empty(); lanes.empty(); cars.empty(); logs.empty(); trees.empty()
    score = 0
    scroll_accumulator = 0.0
    SCROLL_SPEED = 0.2
    game_state = "playing"
    
    player = Player(WIDTH // 2, HEIGHT - 3 * TILE_SIZE)
    
    for i in range(GRID_HEIGHT + 2):
        y = HEIGHT - (i * TILE_SIZE)
        create_lane(y, is_start=(i < 4))

    all_sprites.add(player)

reset_game()

# --- MAIN LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if game_state == "playing":
                original_x = player.rect.x
                original_y = player.rect.y
                moved_forward = False
                
                if event.key == pygame.K_LEFT: player.move(-1, 0)
                elif event.key == pygame.K_RIGHT: player.move(1, 0)
                elif event.key == pygame.K_DOWN: player.move(0, 1)
                elif event.key == pygame.K_UP:
                    if player.move(0, -1):
                        moved_forward = True

                # Tree Collision
                if pygame.sprite.spritecollide(player, trees, False):
                    player.rect.x = original_x
                    player.rect.y = original_y
                    moved_forward = False

                # Camera Hop
                if moved_forward:
                    score += 1
                    # Push everything down by 1 tile
                    player.rect.y += TILE_SIZE 
                    for sprite in all_sprites:
                        if sprite != player:
                            sprite.rect.y += TILE_SIZE
                    
            elif game_state == "game_over":
                if event.key == pygame.K_RETURN:
                    reset_game()

    if game_state == "playing":
        # 1. SMOOTH SCROLL
        current_scroll_speed = SCROLL_SPEED + (score * 0.005) # Speed up very slowly
        scroll_accumulator += current_scroll_speed
        
        # Move pixels only when accumulator > 1 (sub-pixel rendering logic)
        if scroll_accumulator >= 1.0:
            pixels = int(scroll_accumulator)
            scroll_accumulator -= pixels
            for sprite in all_sprites:
                sprite.rect.y += pixels
        
        # 2. Infinite Generation
        min_y = min(lane.rect.y for lane in lanes)
        if min_y > -TILE_SIZE:
            create_lane(min_y - TILE_SIZE)
            
        # 3. Cleanup
        for sprite in all_sprites:
            if sprite.rect.top > HEIGHT:
                sprite.kill()
        
        # 4. Death Conditions
        if player.rect.top >= HEIGHT:
            game_state = "game_over"

        cars.update()
        logs.update()
        
        if pygame.sprite.spritecollide(player, cars, False):
            game_state = "game_over"

        current_lanes = pygame.sprite.spritecollide(player, lanes, False)
        if current_lanes:
            if current_lanes[0].type == LANE_WATER:
                on_log = pygame.sprite.spritecollide(player, logs, False)
                if on_log:
                    player.rect.x += on_log[0].speed
                else:
                    game_state = "game_over"
        
        if score > high_score:
            high_score = score
            save_high_score(high_score)

    # Drawing
    screen.fill(BLACK)
    if game_state == "playing":
        lanes.draw(screen)
        logs.draw(screen)
        cars.draw(screen)
        trees.draw(screen)
        screen.blit(player.image, player.rect)
        
        # Score
        score_bg = pygame.Surface((150, 40)); score_bg.set_alpha(100); score_bg.fill(BLACK)
        screen.blit(score_bg, (5, 5))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
    elif game_state == "game_over":
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(180); overlay.fill(BLACK)
        screen.blit(overlay, (0,0))
        
        game_over_text = game_over_font.render("GAME OVER", True, WHITE)
        text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(game_over_text, text_rect)
        
        score_msg = font.render(f"Score: {score}", True, WHITE)
        score_rect = score_msg.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
        screen.blit(score_msg, score_rect)
        
        high_msg = font.render(f"Best: {high_score}", True, BEAK_ORANGE)
        high_rect = high_msg.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
        screen.blit(high_msg, high_rect)
        
        restart_msg = font.render("Press ENTER to Restart", True, WHITE)
        restart_rect = restart_msg.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
        screen.blit(restart_msg, restart_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()