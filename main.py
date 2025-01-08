import pygame
import random
import time  

# Initialize pygame
pygame.init()

# Set up display
SCREEN = pygame.display.set_mode((500, 750))
pygame.display.set_caption("Flappy Bird")

# Load background and bird images with error handling
try:
    BACKGROUND_IMAGE = pygame.image.load('background.jpg')
    BIRD_IMAGE = pygame.image.load('bird1.png')
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# Bird
bird_x = 50
bird_y = 250  # Start higher to avoid immediate collision
bird_y_change = 0

def display_bird(x, y):
    SCREEN.blit(BIRD_IMAGE, (x, y))

# Obstacles
OBSTACLE_WIDTH = 70
OBSTACLE_COLOR = (211, 253, 117)
OBSTACE_X_CHANGE = -4
obstacle_x = 600  # Start obstacle further away
OBSTACLE_HEIGHT = random.randint(150, 450)

def display_obstacle(height):
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, 0, OBSTACLE_WIDTH, height))
    bottom_obstacle_height = 635 - height - 150
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, 635, OBSTACLE_WIDTH, -bottom_obstacle_height))

# Collision detection
def collision_detection(obstacle_x, obstacle_height, bird_y):
    bottom_obstacle_height = 635 - obstacle_height - 150
    if 50 <= obstacle_x <= (50 + OBSTACLE_WIDTH):  # Check if the bird is near the obstacle
        if bird_y <= obstacle_height or bird_y >= (bottom_obstacle_height - 64):  
            return True
    return False

# Score
score = 0
score_list = [0]
SCORE_FONT = pygame.font.Font('freesansbold.ttf', 32)

def score_display(score):
    display = SCORE_FONT.render(f"Score: {score}", True, (255, 255, 255))
    SCREEN.blit(display, (10, 10))

# Start screen
startFont = pygame.font.Font('freesansbold.ttf', 32)
def start():
    display = startFont.render("PRESS SPACE BAR TO START", True, (255, 255, 255))
    SCREEN.blit(display, (50, 200))
    pygame.display.update()

# Game over screen
game_over_font1 = pygame.font.Font('freesansbold.ttf', 64)
game_over_font2 = pygame.font.Font('freesansbold.ttf', 32)

def game_over():
    maximum = max(score_list)
    display1 = game_over_font1.render("GAME OVER", True, (200, 35, 35))
    SCREEN.blit(display1, (50, 300))
    display2 = game_over_font2.render(f"SCORE: {score} MAX SCORE: {maximum}", True, (255, 255, 255))
    SCREEN.blit(display2, (50, 400))
    if score == maximum:
        display3 = game_over_font2.render("NEW HIGH SCORE!!", True, (200, 35, 35))
        SCREEN.blit(display3, (80, 100))

# Game state variables
running = True
waiting = True
collision = False

# Debug prints to trace variables
def debug_state():
    print(f"Bird Y: {bird_y}, Obstacle X: {obstacle_x}, Collision: {collision}, Score: {score}")

# Main game loop
while running:
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))

    # Waiting for start or restart
    while waiting:
        if collision:
            game_over()
        start()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reset game variables
                score = 0
                bird_y = 250  
                bird_y_change = 0
                obstacle_x = 600  
                OBSTACLE_HEIGHT = random.randint(150, 450)
                collision = False
                waiting = False
                time.sleep(0.5)  
            if event.type == pygame.QUIT:
                waiting = False
                running = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_y_change = -6
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            bird_y_change = 3

    # Bird movement
    bird_y += bird_y_change
    bird_y = max(0, min(bird_y, 571))  # Prevent the bird from moving out of bounds

    # Obstacle movement
    obstacle_x += OBSTACE_X_CHANGE
    if obstacle_x <= -10:
        obstacle_x = 600
        OBSTACLE_HEIGHT = random.randint(150, 450)
        score += 1

    # Collision detection
    collision = collision_detection(obstacle_x, OBSTACLE_HEIGHT, bird_y)
    if collision:
        score_list.append(score)
        waiting = True

    # Display elements
    display_obstacle(OBSTACLE_HEIGHT)
    display_bird(bird_x, bird_y)
    score_display(score)

    debug_state()
    pygame.display.update()

# Quit pygame
pygame.quit()
