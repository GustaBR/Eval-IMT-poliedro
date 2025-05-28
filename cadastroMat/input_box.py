import pygame

CINZA_ESCURO = (169, 169, 169)
AZUL_CLARO = (30, 144, 255)
PRETO = (0, 0, 0)

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = CINZA_ESCURO
        self.color_active = AZUL_CLARO
        self.color = self.color_inactive
        self.text = ''
        self.font = font
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 30:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        txt_surface = self.font.render(self.text, True, PRETO)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_text(self):
        return self.text.strip()

    def set_text(self, text):
        self.text = text

    def clear_text(self):
        self.text = ''