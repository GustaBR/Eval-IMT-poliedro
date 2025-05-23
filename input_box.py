import pygame
from utils import carregar_icone
from placeholder import AnimatedPlaceholder
from config import fonte_regular, Tema_Poliedro, icone_olho_on, icone_olho_off, som_clicar, dt
import config
import math

class InputBox:
    CURSOR_BLINK_INTERVAL = 500
    REPEAT_DELAY = 500
    REPEAT_INTERVAL = 15

    def __init__(self, rel_rect, placeholder, icone_caminho=None, is_senha=False):
        self.rel_rect = rel_rect
        self.text = ""
        self.ativo = False
        self.is_senha = is_senha
        self.exibir_senha = False
        self.tema = Tema_Poliedro

        self.tamanho_icone = 26
        self.icone = carregar_icone(icone_caminho, self.tamanho_icone) if icone_caminho else None
        self.fonte = fonte_regular

        # Placeholder animado para texto do input
        self.placeholder = AnimatedPlaceholder(
            placeholder, self.fonte, (0, 0),
            self.tema["placeholder"], self.tema["accent"]
        )

        self.cursor_visivel = True
        self.cursor_timer = 0.0

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.apagar_segurado = False
        self.tecla_segurada = False
        self.ultima_tecla = None
        self.timer = 0

        self.olho_tamanho_icone = 24
        self.icone_olho = None
        self.icone_olho_off = None
        self.olho_rect = None

        if self.is_senha:
            self.icone_olho = carregar_icone(icone_olho_on, self.olho_tamanho_icone)
            self.icone_olho_off = carregar_icone(icone_olho_off, self.olho_tamanho_icone)
            self.olho_rect = pygame.Rect(0, 0, self.olho_tamanho_icone, self.olho_tamanho_icone)

    def atualizar_rect(self, janela): 
        w, h = janela.get_size()
        self.rect = pygame.Rect(
            int(w * self.rel_rect[0]),
            int(h * self.rel_rect[1]),
            int(w * self.rel_rect[2]),
            int(h * self.rel_rect[3])
        )

        padding_left = 12 + (self.tamanho_icone + 4 if self.icone else 0)

        self.placeholder.pos = (
            self.rect.x + padding_left,
            self.rect.y + self.rect.height // 2 - self.fonte.get_height() // 2
        )

        if self.is_senha and self.olho_rect:
            eye_x = self.rect.right - 10 - self.olho_tamanho_icone
            eye_y = self.rect.y + (self.rect.height - self.olho_tamanho_icone) // 2
            self.olho_rect.topleft = (eye_x, eye_y)

    def checar_eventos(self, evento, tela):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.ativo = True
                if tela.mensagem:
                    tela.mensagem = ""
                self.cursor_visivel = True
                self.cursor_timer = 0.0
                if self.is_senha and self.olho_rect and self.olho_rect.collidepoint(evento.pos):
                    self.exibir_senha = not self.exibir_senha
                    if som_clicar:
                        som_clicar.play()
                    return
            else:
                self.ativo = False

        if self.ativo:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    self.apagar_segurado = True
                    self.timer = 0.0
                    if self.text:
                        self.text = self.text[:-1]
                elif evento.key == pygame.K_RETURN:
                    pass
                elif evento.key == pygame.K_v and (evento.mod & pygame.KMOD_CTRL):
                    clip_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                    if clip_text:
                        self.text += clip_text.decode('utf-8')
                elif evento.unicode and evento.unicode.isprintable():
                    self.text += evento.unicode
                    self.ultima_tecla = evento.unicode
                    self.tecla_segurada = True

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_BACKSPACE:
                    self.apagar_segurado = False
                    
                elif evento.unicode == self.ultima_tecla:
                    self.tecla_segurada = False

                self.timer = 0.0

    def atualizar(self):
        # Controla o piscar do cursor
        self.cursor_timer += dt
        if self.cursor_timer >= self.CURSOR_BLINK_INTERVAL:
            self.cursor_timer -= self.CURSOR_BLINK_INTERVAL
            self.cursor_visivel = not self.cursor_visivel

        self.placeholder.update(self.ativo, bool(self.text), dt) # Atualiza a animação do placeholder

        # Lógica para repetir backspace ao segurar a tecla
        if self.ativo and self.apagar_segurado:
            self.timer += dt
            if self.timer >= self.REPEAT_DELAY + self.REPEAT_INTERVAL:
                self.timer = self.REPEAT_DELAY
                if self.text:
                    self.text = self.text[:-dt//self.REPEAT_INTERVAL+1] if dt//self.REPEAT_INTERVAL > 1 else self.text[:-1]
        
        # Lógica para repetir tecla segurada         
        if self.ativo and self.tecla_segurada:
            self.timer += dt
            if self.timer >= self.REPEAT_DELAY + self.REPEAT_INTERVAL:
                self.timer = self.REPEAT_DELAY
                print("teste")
                self.text += self.ultima_tecla

    def exibir(self, janela):
        pygame.draw.rect(janela, self.tema["input_bg"], self.rect, border_radius=12)
        border_color = self.tema["input_focus"] if self.ativo else self.tema["input_border"]
        pygame.draw.rect(janela, border_color, self.rect, width=2, border_radius=12)

        icon_x = self.rect.x + 10
        icon_y = self.rect.y + self.rect.height // 2 - self.tamanho_icone // 2
        if self.icone:
            janela.blit(self.icone, (icon_x, icon_y))

        # Define posição do texto dentro do input
        text_x = icon_x + (self.tamanho_icone + 10 if self.icone else 10)
        text_y = self.rect.y + self.rect.height // 2

        display_text = self.text if (not self.is_senha or self.exibir_senha) else "*" * len(self.text)
        text_surf = self.fonte.render(display_text, True, self.tema["text"])
        text_rect = text_surf.get_rect()
        text_rect.midleft = (text_x, text_y)
        janela.blit(text_surf, text_rect)

        if self.ativo and self.cursor_visivel:
            cursor_x = text_rect.right + 2
            pygame.draw.line(janela, self.tema["text"], (cursor_x, text_rect.top), (cursor_x, text_rect.bottom), 2)

        self.placeholder.draw(janela)

        # Desenha o ícone do olho para senha
        if self.is_senha and self.olho_rect:
            eye_icon = self.icone_olho if self.exibir_senha else self.icone_olho_off
            if eye_icon:
                janela.blit(eye_icon, self.olho_rect.topleft)
