import pygame
import config

# Classe Botão
class Botao():
    def __init__(self, texto, pos, cor_padrao, cor_texto, cor_hover):
        self.fonte = config.fonte_botao
        self.tamanho = config.figma_para_tela(340, 74)
        self.rect = pygame.Rect(pos, self.tamanho)
        self.texto = texto
        self.cor_padrao = cor_padrao
        self.cor_texto = cor_texto
        self.cor_hover = cor_hover
        self.hovered = False

    def atualizar_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def exibir_botao(self, tela):
        color = self.cor_hover if self.hovered else self.cor_padrao
        pygame.draw.rect(tela, color, self.rect, border_radius=10)

        texto_surf = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)