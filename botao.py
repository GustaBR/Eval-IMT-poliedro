from dropdown import *

class Botao:
    def __init__(self, texto, x, y, w, h, acao=None):
        self.retangulo, self.texto, self.acao = pygame.Rect(x, y, w, h), texto, acao
        self.em_cima, self.clicado = False, False
    def tratar_evento(self, evento):
        pos_mouse = pygame.mouse.get_pos(); self.em_cima = self.retangulo.collidepoint(pos_mouse)
        if self.em_cima and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: self.clicado = True
        if self.clicado and evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.em_cima and self.acao: self.acao()
            self.clicado = False
    def desenhar(self, superficie):
        desenhar_sombra(superficie, self.retangulo); cor = COR_DESTAQUE
        if self.em_cima: cor = COR_BOTAO_HOVER
        if self.clicado: cor = COR_BOTAO_CLIQUE
        pygame.draw.rect(superficie, cor, self.retangulo, border_radius=12)
        ts, tr = FONTE_TITULO.render(self.texto, COR_BRANCO)
        superficie.blit(ts, (self.retangulo.centerx - tr.width//2, self.retangulo.centery - tr.height//2))
    def atualizar(self, dt): pass