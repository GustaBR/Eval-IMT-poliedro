from cadastrar_perguntas.dropdown import *

class Botao:
    def __init__(self, texto, x, y, w, h, acao=None):
        self.retangulo = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.acao = acao
        self.em_cima = False
    
    def tratar_evento(self, evento):
        pos_mouse = pygame.mouse.get_pos()
        self.em_cima = self.retangulo.collidepoint(pos_mouse)
        if self.em_cima and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.acao:
                self.acao()
            
    def desenhar(self, superficie):
        desenhar_sombra(superficie, self.retangulo); cor = COR_DESTAQUE
        if self.em_cima: cor = COR_BOTAO_HOVER
        pygame.draw.rect(superficie, cor, self.retangulo, border_radius=12)
        ts, tr = FONTE_TITULO.render(self.texto, COR_BRANCO)
        superficie.blit(ts, (self.retangulo.centerx - tr.width//2, self.retangulo.centery - tr.height//2))
    
    def atualizar(self, dt):
        pass