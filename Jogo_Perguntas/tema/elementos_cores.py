import pygame
from tema.tema_visual import Tema

class Pergunta:
    def __init__(self, id_questao, enunciado, alternativas, indice_correta, dica=""):
        self.id_questao = id_questao
        self.enunciado = enunciado
        self.alternativas = alternativas 
        self.indice_correta = indice_correta 
        self.dica = dica

    def __str__(self):
        correta_str = self.alternativas[self.indice_correta] if 0 <= self.indice_correta < len(self.alternativas) else "N/A"
        return f"ID: {self.id_questao}\nPergunta: {self.enunciado}\nAlternativas: {self.alternativas}\nCorreta: {correta_str}"

class Botao:
    def __init__(self, x, y, largura, altura, cor_normal, cor_hover, cor_borda, 
                 texto, fonte, cor_texto, raio_borda, acao=None, habilitado=True):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_borda = cor_borda
        self.texto = texto
        self.fonte = fonte
        self.cor_texto = cor_texto
        self.raio_borda = raio_borda
        self.acao = acao
        self.habilitado = habilitado
        self.mouse_sobre = False

    def desenhar(self, tela, y_offset_absoluto_tela=0):
        rect_desenho = self.rect.copy()
        if y_offset_absoluto_tela != 0:
            rect_desenho.y = y_offset_absoluto_tela

        cor_atual_fundo = self.cor_normal
        cor_atual_texto = self.cor_texto

        if not self.habilitado:
            cor_atual_fundo = Tema.CORES['botao_desabilitado']
            cor_atual_texto = Tema.CORES['texto_secundario']
        elif self.mouse_sobre:
            cor_atual_fundo = self.cor_hover
        
        pygame.draw.rect(tela, cor_atual_fundo, rect_desenho, border_radius=self.raio_borda)
        if self.cor_borda: # Desenha a borda se uma cor for especificada
            pygame.draw.rect(tela, self.cor_borda, rect_desenho, 2, border_radius=self.raio_borda)
        
        if self.texto:
            texto_surface = self.fonte.render(self.texto, True, cor_atual_texto)
            texto_rect = texto_surface.get_rect(center=rect_desenho.center)
            tela.blit(texto_surface, texto_rect)

    def verificar_hover(self, pos_mouse, y_offset_absoluto_tela=0):
        if not self.habilitado:
            self.mouse_sobre = False
            return

        rect_real_tela = self.rect.copy()
        if y_offset_absoluto_tela != 0: # Ajusta o y se o botão estiver em uma área que pode scrollar
             rect_real_tela.y = y_offset_absoluto_tela
        
        self.mouse_sobre = rect_real_tela.collidepoint(pos_mouse)

    def tratar_clique(self):
        if self.habilitado and self.mouse_sobre and self.acao:
            self.acao()
            return True 
        return False