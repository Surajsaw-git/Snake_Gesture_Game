import pygame
import cv2
import mediapipe as mp
import random
import time
import math
import os

# ===================== CONFIG =====================
WIDTH, HEIGHT = 600, 600
BLOCK = 20

# ===================== GAME CLASS =====================
class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gesture Controlled Snake Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.big_font = pygame.font.SysFont(None, 45)

        self.colors()
        self.load_sounds()
        self.reset_game()

        self.game_state = "STOPPED"
        self.base_speed = 10
        self.dynamic_speed = self.base_speed

        self.setup_camera()
        self.setup_mediapipe()

    # ---------------- COLORS ----------------
    def colors(self):
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (60, 60, 60)

    # ---------------- SOUNDS ----------------
    def load_sounds(self):
        self.eat_sound = pygame.mixer.Sound("sounds/eat.wav")
        self.gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")
        pygame.mixer.music.load("sounds/bg_music.mp3")
        pygame.mixer.music.play(-1)

    # ---------------- RESET GAME ----------------
    def reset_game(self):
        self.snake = [(100, 100)]
        self.direction = "RIGHT"
        self.food = self.random_food()
        self.score = 0
        self.level = 1

    def random_food(self):
        return (
            random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK)
        )

    # ---------------- CAMERA ----------------
    def setup_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.prev_x, self.prev_y = 0, 0
        self.last_move = time.time()

    # ---------------- MEDIAPIPE ----------------
    def setup_mediapipe(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    # ---------------- DRAW BUTTON ----------------
    def draw_button(self, x, y, w, h, text):
        pygame.draw.rect(self.win, self.GRAY, (x, y, w, h), border_radius=8)
        label = self.font.render(text, True, self.WHITE)
        self.win.blit(label, (x + w//2 - label.get_width()//2,
                              y + h//2 - label.get_height()//2))

    # ---------------- DRAW GAME ----------------
    def draw_game(self):
        self.win.fill(self.BLACK)

        for x, y in self.snake:
            pygame.draw.rect(self.win, self.GREEN, (x, y, BLOCK, BLOCK))

        pygame.draw.rect(self.win, self.RED, (*self.food, BLOCK, BLOCK))

        self.win.blit(self.font.render(f"Score: {self.score}", True, self.WHITE), (10, 10))
        self.win.blit(self.font.render(f"Level: {self.level}", True, self.WHITE), (10, 40))
        self.win.blit(self.font.render(f"Speed: {int(self.dynamic_speed)}", True, self.WHITE), (10, 70))

        self.draw_button(50, 550, 120, 40, "START")
        self.draw_button(240, 550, 120, 40, "RESTART")
        self.draw_button(430, 550, 120, 40, "STOP")

        if self.game_state == "PAUSED":
            txt = self.big_font.render("PAUSED", True, self.RED)
            self.win.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))

        pygame.display.update()

    # ---------------- FINGER COUNT ----------------
    def finger_count(self, hand):
        tips = [4, 8, 12, 16, 20]
        return sum(hand.landmark[tip].y < hand.landmark[tip - 2].y for tip in tips)

    # ---------------- HAND SPEED CONTROL ----------------
    def control_speed_by_hand_distance(self, hand):
        wrist = hand.landmark[0]
        middle_tip = hand.landmark[12]

        distance = math.hypot(
            wrist.x - middle_tip.x,
            wrist.y - middle_tip.y
        )

        # Near camera → slow
        self.dynamic_speed = max(5, min(20, int(20 - distance * 50)))

    # ---------------- DRAW ARROWS ----------------
    def draw_arrows(self, img):
        h, w, _ = img.shape
        c = (w // 2, h // 2)

        cv2.arrowedLine(img, (c[0], c[1] - 40), (c[0], c[1] - 80), (0,255,0), 3)
        cv2.arrowedLine(img, (c[0], c[1] + 40), (c[0], c[1] + 80), (0,255,0), 3)
        cv2.arrowedLine(img, (c[0] - 40, c[1]), (c[0] - 80, c[1]), (0,255,0), 3)
        cv2.arrowedLine(img, (c[0] + 40, c[1]), (c[0] + 80, c[1]), (0,255,0), 3)

    # ---------------- MAIN LOOP ----------------
    def run(self):
        running = True
        while running:
            self.clock.tick(self.dynamic_speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 50 < x < 170 and 550 < y < 590:
                        self.game_state = "RUNNING"
                    if 240 < x < 360 and 550 < y < 590:
                        self.reset_game()
                        self.game_state = "RUNNING"
                    if 430 < x < 550 and 550 < y < 590:
                        self.game_state = "STOPPED"

            success, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)

            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                h, w, _ = frame.shape

                ix, iy = int(hand.landmark[8].x * w), int(hand.landmark[8].y * h)
                cv2.circle(frame, (ix, iy), 10, (0,0,255), -1)

                self.control_speed_by_hand_distance(hand)

                fingers = self.finger_count(hand)
                if fingers == 5:
                    self.game_state = "PAUSED"
                elif fingers == 0 and self.game_state == "PAUSED":
                    self.game_state = "RUNNING"

                dx, dy = ix - self.prev_x, iy - self.prev_y
                if self.game_state == "RUNNING" and time.time() - self.last_move > 0.15:
                    if abs(dx) > abs(dy):
                        self.direction = "RIGHT" if dx > 0 else "LEFT"
                    else:
                        self.direction = "DOWN" if dy > 0 else "UP"
                    self.last_move = time.time()

                self.prev_x, self.prev_y = ix, iy

            self.draw_arrows(frame)
            cv2.imshow("Hand Control", frame)
            cv2.waitKey(1)

            if self.game_state == "RUNNING":
                self.update_snake()

            self.draw_game()

        self.cap.release()
        cv2.destroyAllWindows()
        pygame.quit()

    # ---------------- UPDATE SNAKE ----------------
    def update_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == "UP": head_y -= BLOCK
        if self.direction == "DOWN": head_y += BLOCK
        if self.direction == "LEFT": head_x -= BLOCK
        if self.direction == "RIGHT": head_x += BLOCK

        new_head = (head_x, head_y)

        if (
            new_head in self.snake or
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT
        ):
            self.gameover_sound.play()
            self.game_state = "STOPPED"
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.eat_sound.play()
            self.score += 1
            if self.score % 5 == 0:
                self.level += 1
            self.food = self.random_food()
        else:
            self.snake.pop()

# ===================== RUN =====================
if __name__ == "__main__":
    SnakeGame().run()
