import pygame
import config

# Classe Botão
class BotaoMenu:
    def __init__(self, texto, pos, cor_padrao, cor_texto, cor_hover, fonte, acao=None):
        self.fonte = fonte
        self.tamanho = config.figma_para_tela(340, 74)
        self.rect = pygame.Rect(pos, self.tamanho)
        self.texto = texto
        self.cor_padrao = cor_padrao
        self.cor_texto = cor_texto
        self.cor_hover = cor_hover
        self.hovered = False
        self.acao = acao

    def atualizar_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def exibir_botao(self, tela):
        color = self.cor_hover if self.hovered else self.cor_padrao
        pygame.draw.rect(tela, color, self.rect, border_radius=10)

        texto = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto.get_rect(center=self.rect.center)
        tela.blit(texto, texto_rect)

    def realizar_acao(self):
        if self.acao and self.hovered:
            self.acao()