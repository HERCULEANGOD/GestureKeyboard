import cv2
import pygame
import time
import math

from config import *
from hand_tracking import HandTracker
from keyboard import Key

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Keyboard")

font = pygame.font.Font(None, 50)
big_font = pygame.font.Font(None, 80)

cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

tracker = HandTracker()

last_click_time = 0
CLICK_COOLDOWN = 0.6

click_hold_start = None
HOLD_TIME = 0.7

keys_layout = [
    ["Q","W","E","R","T","Y","U","I","O","P","<-"],
    ["A","S","D","F","G","H","J","K","L",";"],
    ["Z","X","C","V","B","N","M",",","."," "]
]

keyboard = []
for i, row in enumerate(keys_layout):
    for j, char in enumerate(row):
        w = 200 if char == " " else 100 if char == "<-" else KEY_WIDTH
        keyboard.append(
            Key(
                KEY_SPACING_X * j + 100,
                KEY_SPACING_Y * i + 250,
                char,
                w=w
            )
        )

typed_text = ""

running = True
while running:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = tracker.process(rgb)

    frame_surface = pygame.surfarray.make_surface(rgb.swapaxes(0, 1))
    screen.blit(frame_surface, (0, 0))

    cursor = None
    clicking = False

    if result.multi_hand_landmarks:
       for hand in result.multi_hand_landmarks:
        cursor, clicking = tracker.get_cursor_and_click(
            hand, WIDTH, HEIGHT, PINCH_THRESHOLD
        )

        if cursor:
            pygame.draw.circle(screen, (0, 255, 255), cursor, 20, 2)
            pygame.draw.circle(screen, (0, 255, 255), cursor, 2)
            break


    current_time = time.time()

    if clicking:
        if click_hold_start is None:
            click_hold_start = current_time
        hold_progress = min((current_time - click_hold_start) / HOLD_TIME, 1)
    else:
        click_hold_start = None
        hold_progress = 0

    if cursor and clicking:
        radius = 30
        pygame.draw.arc(
            screen,
            (255, 0, 255),
            (cursor[0] - radius, cursor[1] - radius, radius * 2, radius * 2),
            -math.pi / 2,
            -math.pi / 2 + 2 * math.pi * hold_progress,
            4
        )

    for key in keyboard:
        hovered = key.is_hovered(cursor)

        if (
            hovered
            and clicking
            and hold_progress >= 1
            and (current_time - last_click_time) > CLICK_COOLDOWN
        ):
            if key.char == "<-":
                typed_text = typed_text[:-1]
            else:
                typed_text += key.char

            last_click_time = current_time
            click_hold_start = None  

        key.draw(screen, font, hovered, hovered and clicking)


    pygame.draw.rect(screen, (0, 0, 0), (100, 50, 1080, 100), border_radius=15)
    pygame.draw.rect(screen, (0, 255, 255), (100, 50, 1080, 100), 2, border_radius=15)
    screen.blit(big_font.render(typed_text, True, (255, 255, 255)), (130, 70))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
pygame.quit() 
