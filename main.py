import pygame
import cv2
import mediapipe as mp
import random

# ================= USER SETTINGS =================
SNAKE_SPEED = 5   # 🔴 Change this to control speed
# ================================================

WIDTH, HEIGHT = 600, 600
BLOCK = 20

class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Quadrant Hand Gesture Snake Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

        self.setup_camera()
        self.setup_mediapipe()
        self.load_sounds()

        self.reset_game()

    # ---------- SOUND ----------
    def load_sounds(self):
        self.eat_sound = pygame.mixer.Sound("sounds/eat.wav")
        self.gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")

    # ---------- RESET ----------
    def reset_game(self):
        self.snake = [(100, 100)]
        self.direction = "RIGHT"
        self.food = self.random_food()
        self.score = 0

    def random_food(self):
        return (
            random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK)
        )

    # ---------- CAMERA ----------
    def setup_camera(self):
        self.cap = cv2.VideoCapture(0)

    # ---------- MEDIAPIPE ----------
    def setup_mediapipe(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.drawer = mp.solutions.drawing_utils

    # ---------- DRAW GAME ----------
    def draw_game(self):
        self.win.fill((0, 0, 0))

        for x, y in self.snake:
            pygame.draw.rect(self.win, (0, 255, 0), (x, y, BLOCK, BLOCK))
        pygame.draw.rect(self.win, (255, 0, 0), (*self.food, BLOCK, BLOCK))

        self.win.blit(self.font.render(f"Score: {self.score}", True, (255,255,255)), (10, 10))
        self.win.blit(self.font.render(f"Speed: {SNAKE_SPEED}", True, (255,255,255)), (10, 40))

        pygame.display.update()

    # ---------- UPDATE SNAKE ----------
    def update_snake(self):
        x, y = self.snake[0]

        if self.direction == "UP": y -= BLOCK
        if self.direction == "DOWN": y += BLOCK
        if self.direction == "LEFT": x -= BLOCK
        if self.direction == "RIGHT": x += BLOCK

        head = (x, y)

        if head in self.snake or x < 0 or y < 0 or x >= WIDTH or y >= HEIGHT:
            self.gameover_sound.play()
            self.reset_game()
            return

        self.snake.insert(0, head)

        if head == self.food:
            self.eat_sound.play()
            self.score += 1
            self.food = self.random_food()
        else:
            self.snake.pop()

    # ---------- MAIN LOOP ----------
    def run(self):
        running = True
        while running:
            self.clock.tick(SNAKE_SPEED)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            success, frame = self.cap.read()
            frame = cv2.flip(frame, 1)

            # -------- GRAYSCALE --------
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
            display = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

            h, w = gray.shape

            # Draw quadrant lines
            cv2.line(display, (w//2, 0), (w//2, h), (255,255,255), 2)
            cv2.line(display, (0, h//2), (w, h//2), (255,255,255), 2)

            res = self.hands.process(rgb)

            if res.multi_hand_landmarks:
                hand = res.multi_hand_landmarks[0]

                self.drawer.draw_landmarks(
                    display,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS
                )

                # Hand center
                cx = int(sum(lm.x for lm in hand.landmark) / 21 * w)
                cy = int(sum(lm.y for lm in hand.landmark) / 21 * h)

                cv2.circle(display, (cx, cy), 8, (0,0,255), -1)

                # -------- QUADRANT LOGIC --------
                if cx < w//2 and cy < h//2:
                    self.direction = "UP"
                elif cx >= w//2 and cy < h//2:
                    self.direction = "RIGHT"
                elif cx < w//2 and cy >= h//2:
                    self.direction = "LEFT"
                else:
                    self.direction = "DOWN"

            cv2.imshow("Hand Control (Quadrant Mode)", display)
            cv2.waitKey(1)

            self.update_snake()
            self.draw_game()

        self.cap.release()
        cv2.destroyAllWindows()
        pygame.quit()

# ================= RUN =================
if __name__ == "__main__":
    SnakeGame().run()
