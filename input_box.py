import pygame
from utils import carregar_icone
from placeholder import AnimatedPlaceholder
from config import fonte_regular, Tema_Poliedro, icone_olho_on, icone_olho_off, som_clicar

class InputBox:
    CURSOR_BLINK_INTERVAL = 0.6
    BACKSPACE_REPEAT_DELAY = 0.5
    BACKSPACE_REPEAT_INTERVAL = 0.05

    def __init__(self, rel_rect, placeholder, icone_caminho=None, is_senha=False):
        self.rel_rect = rel_rect
        self.placeholder = placeholder
        self.text = ""
        self.ativo = False
        self.is_senha = is_senha
        self.exibir_senha = False
        self.theme = Tema_Poliedro

        self.tamanho_icone = 26
        self.icone = carregar_icone(icone_caminho, self.tamanho_icone) if icone_caminho else None
        self.fonte = fonte_regular

        # Placeholder animado para texto do input
        self.placeholder = AnimatedPlaceholder(
            placeholder, self.fonte, (0, 0),
            self.tema["placeholder"], self.tema["accent"]
        )

        self.cursor_visivel = True
        self.cursor_timer = 0

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.apagar_segurado = False
        self.apagar_timer = 0

        self.olho_tamanho_icone = 24
        self.icone_olho = None
        self.icone_olho_off = None
        self.olho_rect = None

        # Ícones para mostrar/ocultar senha
        if self.is_senha:
            self.icone_olho = carregar_icone(icone_olho_on, self.olho_tamanho_icone)
            self.icone_olho_off = carregar_icone(icone_olho_off, self.olho_tamanho_icone)
            self.olho_rect = pygame.Rect(0, 0, self.olho_tamanho_icone, self.olho_tamanho_icone)

        self.atualizar_rect()

    """def atualizar_rect(self):
        w, h = self.surface.get_size()
        self.rect = pygame.Rect(
            int(w * self.rel_rect[0]),
            int(h * self.rel_rect[1]),
            int(w * self.rel_rect[2]),
            int(h * self.rel_rect[3])
        )

        padding_left = 12 + (self.tamanho_icone + 4 if self.icon else 0)
        self.placeholder.pos = (
            self.rect.x + padding_left,
            self.rect.y + self.rect.height // 2 - self.font.get_height() // 2
        )

        if self.is_senha and self.olho_rect:
            eye_x = self.rect.right - 10 - self.olho_tamanho_icone
            eye_y = self.rect.y + (self.rect.height - self.olho_tamanho_icone) // 2
            self.olho_rect.topleft = (eye_x, eye_y)"""

    def handle_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Ativa o input se clicado dentro da área
            if self.rect.collidepoint(evento.pos):
                self.ativo = True
                self.cursor_visivel = True
                self.cursor_timer = 0
                if self.is_senha and self.olho_rect and self.olho_rect.collidepoint(evento.pos):
                    self.exibir_senha = not self.exibir_senha
                    if som_clicar:
                        som_clicar.play()
                    return  # Evita entrada de texto ao clicar no olho
            else:
                self.ativo = False

        if self.ativo:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.apagar_segurado = True
                    self.apagar_timer = 0
                    if self.text:
                        self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                    pass
                else:
                    # Adiciona caracteres imprimíveis ao texto
                    if event.unicode and event.unicode.isprintable():
                        self.text += event.unicode

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.apagar_segurado = False
                    self.apagar_timer = 0

    def update(self, dt):
        # Controla o piscar do cursor
        self.cursor_timer += dt
        if self.cursor_timer >= self.CURSOR_BLINK_INTERVAL:
            self.cursor_timer = 0
            self.cursor_visivel = not self.cursor_visivel

        self.atualizar_rect()
        # Atualiza animação do placeholder
        self.placeholder.update(self.ativo, bool(self.text), dt)

        # Lógica para repetir backspace ao segurar a tecla
        if self.ativo and self.apagar_segurado:
            self.apagar_timer += dt
            if self.apagar_timer >= self.BACKSPACE_REPEAT_DELAY:
                repeats = int((self.apagar_timer - self.BACKSPACE_REPEAT_DELAY) / self.BACKSPACE_REPEAT_INTERVAL)
                if repeats > 0 and self.text:
                    self.text = self.text[:-1]
                    self.apagar_timer -= self.BACKSPACE_REPEAT_INTERVAL

    def draw(self):
        # Desenha o fundo e borda do input box
        pygame.draw.rect(self.surface, self.theme["input_bg"], self.rect, border_radius=12)
        border_color = self.theme["input_focus"] if self.ativo else self.theme["input_border"]
        pygame.draw.rect(self.surface, border_color, self.rect, width=2, border_radius=12)

        # Desenha o ícone
        icon_x = self.rect.x + 10
        icon_y = self.rect.y + self.rect.height // 2 - self.tamanho_icone // 2
        if self.icon:
            self.surface.blit(self.icon, (icon_x, icon_y))

        # Define posição do texto dentro do input
        text_x = icon_x + (self.tamanho_icone + 10 if self.icon else 10)
        text_y = self.rect.y + self.rect.height // 2

        display_text = self.text if (not self.is_senha or self.exibir_senha) else "*" * len(self.text)
        text_surf = self.font.render(display_text, True, self.theme["text"])
        text_rect = text_surf.get_rect()
        text_rect.midleft = (text_x, text_y)
        self.surface.blit(text_surf, text_rect)

        if self.ativo and self.cursor_visivel:
            cursor_x = text_rect.right + 2
            pygame.draw.line(self.surface, self.theme["text"], (cursor_x, text_rect.top), (cursor_x, text_rect.bottom), 2)

        self.placeholder.draw(self.surface)

        # Desenha o ícone do olho para senha
        if self.is_senha and self.olho_rect:
            eye_icon = self.icone_olho if self.exibir_senha else self.icone_olho_off
            if eye_icon:
                self.surface.blit(eye_icon, self.olho_rect.topleft)