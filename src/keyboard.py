import pygame

class Key:
    def __init__(self, x, y, char, w=80, h=80):
        self.x = x
        self.y = y
        self.char = char
        self.w = w
        self.h = h

    def is_hovered(self, pos):
        if not pos:
            return False
        x, y = pos
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    def draw(self, screen, font, hovered=False, pressed=False):

        if pressed:
            color = (255, 0, 255)   
            thickness = 4
        elif hovered:
            color = (0, 255, 255)   
            thickness = 3
        else:
            color = (200, 200, 200) 
            thickness = 2

        pygame.draw.rect(
            screen,
            color,
            (self.x, self.y, self.w, self.h),
            thickness,
            border_radius=10
        )

        label = "BS" if self.char == "<-" else "SPACE" if self.char == " " else self.char
        text_surface = font.render(label, True, color)
        text_rect = text_surface.get_rect(
            center=(self.x + self.w // 2, self.y + self.h // 2)
        )
        screen.blit(text_surface, text_rect)
