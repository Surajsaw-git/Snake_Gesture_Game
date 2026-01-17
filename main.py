import pygame
import cv2
import mediapipe as mp
import random
import time

# -------------------- PYGAME SETUP --------------------
pygame.init()

WIDTH, HEIGHT = 600, 600
BLOCK = 20

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Controlled Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# -------------------- SNAKE SETUP --------------------
snake = [(100, 100)]
direction = "RIGHT"

food = (
    random.randrange(0, WIDTH, BLOCK),
    random.randrange(0, HEIGHT, BLOCK)
)

score = 0

# -------------------- OPENCV + MEDIAPIPE SETUP --------------------
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Finger tracking helpers
prev_x, prev_y = 0, 0
last_move = time.time()

# -------------------- DRAW FUNCTION --------------------
def draw():
    win.fill(BLACK)

    for x, y in snake:
        pygame.draw.rect(win, GREEN, (x, y, BLOCK, BLOCK))

    pygame.draw.rect(win, RED, (*food, BLOCK, BLOCK))

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(text, (10, 10))

    pygame.display.update()

# -------------------- MAIN LOOP --------------------
running = True
while running:
    clock.tick(10)

    # ---- Pygame Events ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---- Webcam Read ----
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # ---- Gesture Detection ----
    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        h, w, _ = frame.shape

        lm = hand.landmark[8]  # Index finger tip
        x, y = int(lm.x * w), int(lm.y * h)

        dx = x - prev_x
        dy = y - prev_y

        if time.time() - last_move > 0.15:
            if abs(dx) > abs(dy):
                if dx > 20:
                    direction = "RIGHT"
                elif dx < -20:
                    direction = "LEFT"
            else:
                if dy > 20:
                    direction = "DOWN"
                elif dy < -20:
                    direction = "UP"

            last_move = time.time()

        prev_x, prev_y = x, y

    # ---- Show Webcam ----
    cv2.imshow("Hand Control", frame)
    cv2.waitKey(1)

    # ---- Snake Movement ----
    head_x, head_y = snake[0]

    if direction == "UP":
        head_y -= BLOCK
    elif direction == "DOWN":
        head_y += BLOCK
    elif direction == "LEFT":
        head_x -= BLOCK
    elif direction == "RIGHT":
        head_x += BLOCK

    new_head = (head_x, head_y)

    # ---- Collision ----
    if (
        new_head in snake or
        head_x < 0 or head_x >= WIDTH or
        head_y < 0 or head_y >= HEIGHT
    ):
        running = False

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        food = (
            random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK)
        )
    else:
        snake.pop()

    draw()

# -------------------- CLEANUP --------------------
cap.release()
cv2.destroyAllWindows()
pygame.quit()
