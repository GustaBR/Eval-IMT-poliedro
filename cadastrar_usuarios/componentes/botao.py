import pygame

class BotaoTela:
    def __init__(self, rect, texto, fonte, cor_normal, cor_hover, cor_texto=(255,255,255), border_radius=15):
        self.rect = rect
        self.texto = texto
        self.fonte = fonte
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
        self.border_radius = border_radius

    def desenhar(self, surface):
        pos_mouse = pygame.mouse.get_pos()
        cor = self.cor_hover if self.rect.collidepoint(pos_mouse) else self.cor_normal
        pygame.draw.rect(surface, cor, self.rect, border_radius=self.border_radius)
        txt_surf = self.fonte.render(self.texto, True, self.cor_texto)
        surface.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))

    def clicado(self, pos):
        return self.rect.collidepoint(pos)
