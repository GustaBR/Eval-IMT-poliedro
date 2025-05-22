import pygame

class BotaoLogin:
    def __init__(self, surface, rel_rect, text, on_click=None, active=True):
        self.surface = surface
        self.rel_rect = rel_rect
        self.text = text
        self.on_click = on_click
        self.active = active
        self.hovered = False

        self.colors = { # Cores do botão para cada estado
            "normal": (0, 102, 204),
            "hover": (0, 80, 160),
            "inactive": (180, 180, 180)
        }

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update_rect()

        self.font = pygame.font.Font(None, 24) # Fonte para o texto do botão 

    def update_rect(self):
        largura, altura = self.surface.get_size()
        x = int(self.rel_rect[0] * largura)
        y = int(self.rel_rect[1] * altura)
        w = int(self.rel_rect[2] * largura)
        h = int(self.rel_rect[3] * altura)
        self.rect = pygame.Rect(x, y, w, h)

        font_size = max(int(h * 0.5), 12)  # Atualiza o tamanho da fonte para se ajustar à altura do botão
        self.font = pygame.font.Font(None, font_size)

    def set_active(self, state: bool):
        self.active = state

    def handle_event(self, event):
        if not self.active:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.on_click: #Chamar callback, se existir
                    self.on_click()
                return True
        return False

    def update(self, db):
        self.update_rect()  # Atualiza posição e tamanho do botão 

    def draw(self):
        if not self.active:
            cor = self.colors["inactive"] # Escolhe a cor de acordo com o estado do botão
        else:
            cor = self.colors["hover"] if self.hovered else self.colors["normal"]

        pygame.draw.rect(self.surface, cor, self.rect, border_radius=12)  # Desenha o retângulo arredondado

        text_surf = self.font.render(self.text, True, (255, 255, 255))  # Renderiza o texto branco no centro do botão
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surface.blit(text_surf, text_rect)