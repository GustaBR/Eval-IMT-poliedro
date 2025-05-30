import pygame

class BotaoTela:
    def __init__(self, x, y, largura, altura, cor_fundo, cor_borda, texto, fonte, cor_texto, raio_borda=10):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_fundo = cor_fundo
        self.cor_borda = cor_borda
        self.texto = texto
        self.fonte = fonte
        self.cor_texto = cor_texto
        self.raio_borda = raio_borda

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_fundo, self.rect, border_radius=self.raio_borda)
        pygame.draw.rect(tela, self.cor_borda, self.rect, 2, border_radius=self.raio_borda)
        # Convertendo self.texto para string explicitamente antes de renderizar
        texto_render = self.fonte.render(str(self.texto), True, self.cor_texto)
        tela.blit(texto_render, (self.rect.x + 10, self.rect.y + (self.rect.height - texto_render.get_height()) // 2))

    def clicado(self, pos):
        return self.rect.collidepoint(pos)


