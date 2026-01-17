import pygame
import cv2
import mediapipe as mp
import random
import time
import math

# -------------------- PYGAME SETUP --------------------
pygame.init()

WIDTH, HEIGHT = 600, 600
BLOCK = 20

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Controlled Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 45)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)

# -------------------- GAME STATE --------------------
STOPPED = 0
RUNNING = 1
PAUSED = 2
game_state = STOPPED

# -------------------- SNAKE DATA --------------------
def reset_game():
    global snake, direction, food, score
    snake = [(100, 100)]
    direction = "RIGHT"
    food = (
        random.randrange(0, WIDTH, BLOCK),
        random.randrange(0, HEIGHT, BLOCK)
    )
    score = 0

reset_game()

# -------------------- OPENCV + MEDIAPIPE --------------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

prev_x, prev_y = 0, 0
last_move = time.time()

# -------------------- UI BUTTONS --------------------
def draw_button(x, y, w, h, text):
    pygame.draw.rect(win, GRAY, (x, y, w, h), border_radius=8)
    label = font.render(text, True, WHITE)
    win.blit(label, (x + w//2 - label.get_width()//2,
                     y + h//2 - label.get_height()//2))

# -------------------- DRAW GAME --------------------
def draw_game():
    win.fill(BLACK)

    for x, y in snake:
        pygame.draw.rect(win, GREEN, (x, y, BLOCK, BLOCK))

    pygame.draw.rect(win, RED, (*food, BLOCK, BLOCK))

    score_text = font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))

    draw_button(50, 550, 120, 40, "START")
    draw_button(240, 550, 120, 40, "RESTART")
    draw_button(430, 550, 120, 40, "STOP")

    if game_state == PAUSED:
        pause_text = big_font.render("PAUSED", True, RED)
        win.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2))

    pygame.display.update()

# -------------------- FINGER COUNT --------------------
def finger_count(hand):
    tips = [4, 8, 12, 16, 20]
    count = 0
    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            count += 1
    return count

# -------------------- DRAW ARROWS --------------------
def draw_arrows(img):
    h, w, _ = img.shape
    center = (w // 2, h // 2)

    cv2.arrowedLine(img, (center[0], center[1] - 40), (center[0], center[1] - 80), (0,255,0), 3)  # UP
    cv2.arrowedLine(img, (center[0], center[1] + 40), (center[0], center[1] + 80), (0,255,0), 3)  # DOWN
    cv2.arrowedLine(img, (center[0] - 40, center[1]), (center[0] - 80, center[1]), (0,255,0), 3)  # LEFT
    cv2.arrowedLine(img, (center[0] + 40, center[1]), (center[0] + 80, center[1]), (0,255,0), 3)  # RIGHT

# -------------------- MAIN LOOP --------------------
running = True
while running:
    clock.tick(12)

    # ---------- EVENTS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 50 < mx < 170 and 550 < my < 590:
                game_state = RUNNING
            if 240 < mx < 360 and 550 < my < 590:
                reset_game()
                game_state = RUNNING
            if 430 < mx < 550 and 550 < my < 590:
                game_state = STOPPED

    # ---------- WEBCAM ----------
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        h, w, _ = frame.shape

        # Draw index point
        ix, iy = int(hand.landmark[8].x * w), int(hand.landmark[8].y * h)
        cv2.circle(frame, (ix, iy), 10, (0, 0, 255), -1)

        fingers = finger_count(hand)

        # Pause / Resume
        if fingers == 5:
            game_state = PAUSED
        elif fingers == 0 and game_state == PAUSED:
            game_state = RUNNING

        # Restart (pinch)
        dist = math.hypot(
            hand.landmark[4].x - hand.landmark[8].x,
            hand.landmark[4].y - hand.landmark[8].y
        )
        if dist < 0.03:
            reset_game()
            game_state = RUNNING

        # Direction control
        dx = ix - prev_x
        dy = iy - prev_y

        if game_state == RUNNING and time.time() - last_move > 0.15:
            if abs(dx) > abs(dy):
                if dx > 20: direction = "RIGHT"
                elif dx < -20: direction = "LEFT"
            else:
                if dy > 20: direction = "DOWN"
                elif dy < -20: direction = "UP"
            last_move = time.time()

        prev_x, prev_y = ix, iy

    draw_arrows(frame)
    cv2.imshow("Hand Control", frame)
    cv2.waitKey(1)

    # ---------- GAME LOGIC ----------
    if game_state == RUNNING:
        head_x, head_y = snake[0]

        if direction == "UP": head_y -= BLOCK
        elif direction == "DOWN": head_y += BLOCK
        elif direction == "LEFT": head_x -= BLOCK
        elif direction == "RIGHT": head_x += BLOCK

        new_head = (head_x, head_y)

        if (
            new_head in snake or
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT
        ):
            game_state = STOPPED

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = (
                random.randrange(0, WIDTH, BLOCK),
                random.randrange(0, HEIGHT, BLOCK)
            )
        else:
            snake.pop()

    draw_game()

# -------------------- CLEANUP --------------------
cap.release()
cv2.destroyAllWindows()
pygame.quit()
