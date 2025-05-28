import pygame  # type: ignore
import sys
from database import Database
from jogador import Jogador

AZUL_CLARO = (30, 144, 255)
DOURADO = (218, 165, 32)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_CLARO = (220, 220, 220)
CINZA_ESCURO = (169, 169, 169)


class RankingApp:
    def __init__(self):
        pygame.init()
        self.LARGURA, self.ALTURA = 900, 600
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA), pygame.RESIZABLE)
        pygame.display.set_caption("Ranking")

        self.fonte_titulo = pygame.font.SysFont("comicsansms", 64)
        self.fonte_input = pygame.font.SysFont("comicsansms", 24)

        self.scroll_offset = 0
        self.input_ativo = False
        self.texto_busca = ""

        self.ITEM_ALTURA = 60
        self.ITENS_VISIVEIS = 6

        self.ranking = Database.carregar_dados()

    def desenhar_texto(self, texto, fonte, cor, superficie, x, y):
        texto_obj = fonte.render(texto, True, cor)
        superficie.blit(texto_obj, (x, y))

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.VIDEORESIZE:
                self.LARGURA, self.ALTURA = evento.w, evento.h
                self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA), pygame.RESIZABLE)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if 170 <= evento.pos[0] <= 650 and 135 <= evento.pos[1] <= 175:
                    self.input_ativo = True
                else:
                    self.input_ativo = False
                if evento.button == 4:
                    self.scroll_offset = max(self.scroll_offset - self.ITEM_ALTURA, 0)
                elif evento.button == 5:
                    self.scroll_offset += self.ITEM_ALTURA
            elif evento.type == pygame.KEYDOWN:
                if self.input_ativo:
                    if evento.key == pygame.K_BACKSPACE:
                        self.texto_busca = self.texto_busca[:-1]
                    else:
                        self.texto_busca += evento.unicode
                else:
                    if evento.key == pygame.K_UP:
                        self.scroll_offset = max(self.scroll_offset - self.ITEM_ALTURA, 0)
                    elif evento.key == pygame.K_DOWN:
                        self.scroll_offset += self.ITEM_ALTURA

    def desenhar_interface(self):
        self.tela.fill(AZUL_CLARO)
        self.desenhar_texto("Ranking", self.fonte_titulo, BRANCO, self.tela, self.LARGURA // 2 - 130, 30)

        pygame.draw.rect(self.tela, DOURADO, (70, 130, self.LARGURA - 140, 50))
        pygame.draw.rect(self.tela, BRANCO, (90, 135, 70, 40))
        self.desenhar_texto("Rank", self.fonte_input, PRETO, self.tela, 100, 140)

        pygame.draw.rect(self.tela, BRANCO, (170, 135, self.LARGURA - 320, 40))
        cor_borda = PRETO if self.input_ativo else CINZA_CLARO
        pygame.draw.rect(self.tela, cor_borda, (170, 135, self.LARGURA - 320, 40), 2)
        self.desenhar_texto(self.texto_busca or "🔍 Procurar", self.fonte_input, PRETO, self.tela, 180, 140)

        pygame.draw.rect(self.tela, BRANCO, (self.LARGURA - 240, 135, 150, 40))
        self.desenhar_texto("Pontuação", self.fonte_input, PRETO, self.tela, self.LARGURA - 230, 140)

    def desenhar_ranking(self):
        ranking_filtrado = [j for j in self.ranking if self.texto_busca.lower() in j.nome.lower()]
        total_itens = len(ranking_filtrado)
        max_offset = max(0, (total_itens - self.ITENS_VISIVEIS) * self.ITEM_ALTURA)
        self.scroll_offset = min(self.scroll_offset, max_offset)

        y_base = 200
        inicio = self.scroll_offset // self.ITEM_ALTURA
        fim = inicio + self.ITENS_VISIVEIS

        for i, jogador in enumerate(ranking_filtrado[inicio:fim]):
            pos_y = y_base + i * self.ITEM_ALTURA
            pygame.draw.rect(self.tela, PRETO, (80, pos_y, self.LARGURA - 160, 40))
            pygame.draw.rect(self.tela, CINZA_CLARO, (85, pos_y + 5, 60, 30))
            pygame.draw.rect(self.tela, CINZA_CLARO, (155, pos_y + 5, self.LARGURA - 460, 30))
            pygame.draw.rect(self.tela, CINZA_CLARO, (self.LARGURA - 235, pos_y + 5, 140, 30))
            self.desenhar_texto(str(inicio + i + 1), self.fonte_input, PRETO, self.tela, 95, pos_y + 10)
            self.desenhar_texto(jogador.nome, self.fonte_input, PRETO, self.tela, 165, pos_y + 10)
            self.desenhar_texto(str(jogador.pontuacao), self.fonte_input, PRETO, self.tela, self.LARGURA - 225, pos_y + 10)

    def executar(self):
        clock = pygame.time.Clock()
        while True:
            self.tratar_eventos()
            self.desenhar_interface()
            self.desenhar_ranking()
            pygame.display.flip()
            clock.tick(60)