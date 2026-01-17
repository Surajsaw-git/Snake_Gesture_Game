import pygame
import random

pygame.init()

# Window
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

clock = pygame.time.Clock()
block = 20

snake = [(100,100)]
direction = "RIGHT"

food = (random.randrange(0, WIDTH, block),
        random.randrange(0, HEIGHT, block))

score = 0
font = pygame.font.SysFont(None, 35)

def draw():
    win.fill(BLACK)
    for x, y in snake:
        pygame.draw.rect(win, GREEN, (x, y, block, block))
    pygame.draw.rect(win, RED, (*food, block, block))
    text = font.render(f"Score: {score}", True, (255,255,255))
    win.blit(text, (10,10))
    pygame.display.update()

running = True
while running:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: direction = "UP"
    if keys[pygame.K_DOWN]: direction = "DOWN"
    if keys[pygame.K_LEFT]: direction = "LEFT"
    if keys[pygame.K_RIGHT]: direction = "RIGHT"

    head_x, head_y = snake[0]
    if direction == "UP": head_y -= block
    if direction == "DOWN": head_y += block
    if direction == "LEFT": head_x -= block
    if direction == "RIGHT": head_x += block

    new_head = (head_x, head_y)

    # Collision
    if new_head in snake or not (0 <= head_x < WIDTH and 0 <= head_y < HEIGHT):
        running = False

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        food = (random.randrange(0, WIDTH, block),
                random.randrange(0, HEIGHT, block))
    else:
        snake.pop()

    draw()

pygame.quit()
