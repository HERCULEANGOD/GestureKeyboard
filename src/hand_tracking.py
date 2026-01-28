import mediapipe as mp
import math
from collections import deque

class HandTracker:
    def __init__(self, detection_conf=0.8, tracking_conf=0.8):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )

        self.prev_x = None
        self.prev_y = None
        self.smooth_factor = 0.8

        self.pinch_history = deque(maxlen=8)  

    def process(self, image):
        return self.hands.process(image)

    def get_cursor_and_click(self, hand_landmarks, width, height, pinch_threshold):
        idx = hand_landmarks.landmark[8]
        thumb = hand_landmarks.landmark[4]

        idx_x, idx_y = int(idx.x * width), int(idx.y * height)
        thumb_x, thumb_y = int(thumb.x * width), int(thumb.y * height)

        distance = math.hypot(idx_x - thumb_x, idx_y - thumb_y)
        raw_pinch = distance < pinch_threshold

        self.pinch_history.append(raw_pinch)

        pinch_confident = sum(self.pinch_history) >= 6  

        if self.prev_x is None:
            self.prev_x, self.prev_y = idx_x, idx_y

        smooth_x = int(self.smooth_factor * self.prev_x + (1 - self.smooth_factor) * idx_x)
        smooth_y = int(self.smooth_factor * self.prev_y + (1 - self.smooth_factor) * idx_y)

        self.prev_x, self.prev_y = smooth_x, smooth_y

        return (smooth_x, smooth_y), pinch_confident
