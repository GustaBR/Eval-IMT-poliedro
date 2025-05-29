import pygame  # type: ignore
import sys
from rank.database import Database
from rank.jogador import Jogador
import config

AZUL_CLARO = (30, 144, 255)
DOURADO = (218, 165, 32)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_CLARO = (220, 220, 220)
CINZA_ESCURO = (169, 169, 169)

class RankingTela:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador

        self.fonte_titulo = pygame.font.SysFont("comicsansms", 64)
        self.fonte_input = pygame.font.SysFont("comicsansms", 24)

        self.scroll_offset = 0
        self.input_ativo = False
        self.texto_busca = ""

        self.ITEM_ALTURA = 60
        self.ITENS_VISIVEIS = 6

        self.ranking = Database.carregar_dados()

    def desenhar_texto(self, texto, fonte, cor, janela, x, y):
        texto_obj = fonte.render(texto, True, cor)
        janela.blit(texto_obj, (x, y))

    def checar_eventos(self, evento):
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
                if evento.key == pygame.K_DOWN:
                    self.scroll_offset += self.ITEM_ALTURA
                if evento.key == pygame.K_ESCAPE:
                    from menu_tela_professor import MenuTelaProfessor
                    self.gerenciador.trocar_tela(MenuTelaProfessor)

    def atualizar(self):
        ...
        # Especificar Recalculos para atualizar os botões após evento RESIZE

    def exibir(self, janela):
        janela.fill(AZUL_CLARO)
        self.desenhar_texto("Ranking", self.fonte_titulo, BRANCO, janela, config.LARGURA_JANELA // 2 - 130, 30)

        pygame.draw.rect(janela, DOURADO, (70, 130, config.LARGURA_JANELA - 140, 50))
        pygame.draw.rect(janela, BRANCO, (90, 135, 70, 40))
        self.desenhar_texto("Rank", self.fonte_input, PRETO, janela, 100, 140)

        pygame.draw.rect(janela, BRANCO, (170, 135, config.LARGURA_JANELA - 320, 40))
        cor_borda = PRETO if self.input_ativo else CINZA_CLARO
        pygame.draw.rect(janela, cor_borda, (170, 135, config.LARGURA_JANELA - 320, 40), 2)
        self.desenhar_texto(self.texto_busca or "🔍 Procurar", self.fonte_input, PRETO, janela, 180, 140)

        pygame.draw.rect(janela, BRANCO, (config.LARGURA_JANELA - 240, 135, 150, 40))
        self.desenhar_texto("Pontuação", self.fonte_input, PRETO, janela, config.LARGURA_JANELA - 230, 140)

        ranking_filtrado = [j for j in self.ranking if self.texto_busca.lower() in j.nome.lower()]
        total_itens = len(ranking_filtrado)
        max_offset = max(0, (total_itens - self.ITENS_VISIVEIS) * self.ITEM_ALTURA)
        self.scroll_offset = min(self.scroll_offset, max_offset)

        y_base = 200
        inicio = self.scroll_offset // self.ITEM_ALTURA
        fim = inicio + self.ITENS_VISIVEIS

        for i, jogador in enumerate(ranking_filtrado[inicio:fim]):
            pos_y = y_base + i * self.ITEM_ALTURA
            pygame.draw.rect(janela, PRETO, (80, pos_y, config.LARGURA_JANELA - 160, 40))
            pygame.draw.rect(janela, CINZA_CLARO, (85, pos_y + 5, 60, 30))
            pygame.draw.rect(janela, CINZA_CLARO, (155, pos_y + 5, config.LARGURA_JANELA - 460, 30))
            pygame.draw.rect(janela, CINZA_CLARO, (config.LARGURA_JANELA - 235, pos_y + 5, 140, 30))
            self.desenhar_texto(str(inicio + i + 1), self.fonte_input, PRETO, janela, 95, pos_y + 10)
            self.desenhar_texto(jogador.nome, self.fonte_input, PRETO, janela, 165, pos_y + 10)
            self.desenhar_texto(str(jogador.pontuacao), self.fonte_input, PRETO, janela, config.LARGURA_JANELA - 225, pos_y + 10)