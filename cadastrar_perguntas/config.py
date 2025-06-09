import pygame
import pygame.freetype
pygame.freetype.init()

# Tamanho da Tela
LARGURA, ALTURA = 1200, 800

# Cores
COR_FUNDO = (245, 245, 245)
COR_BRANCO = (255, 255, 255)
COR_TEXTO_TITULO = (30, 30, 30)
COR_TEXTO_NORMAL = (50, 50, 50)
COR_TEXTO_DICA = (160, 160, 160)
COR_BORDA = (200, 200, 200)
COR_BORDA_ATIVA = (80, 100, 160)
COR_DESTAQUE = (255, 190, 0)
COR_BOTAO_HOVER = (0, 150, 255)
COR_BOTAO_CLIQUE = (0, 100, 200)
COR_MENU_HOVER = (230, 240, 255)
COR_SOMBRA = (0, 0, 0, 30)
COR_ERRO = (220, 40, 40)
COR_SUCESSO = (40, 180, 40)

try:
    FONTE_TITULO = pygame.freetype.SysFont("Calibri", 28, bold=True)
    FONTE_NORMAL = pygame.freetype.SysFont("Calibri", 22)
    FONTE_PEQUENA = pygame.freetype.SysFont("Calibri", 18)
except FileNotFoundError:
    FONTE_TITULO = pygame.freetype.SysFont("Arial", 28, bold=True)
    FONTE_NORMAL = pygame.freetype.SysFont("Arial", 22)
    FONTE_PEQUENA = pygame.freetype.SysFont("Arial", 18)

# CONFIG BANCO DE DADOS
CONFIG_BD = {
    'host': 'jogomilhao-pi11semestre.l.aivencloud.com',
    'port': 25159,
    'user': 'avnadmin',
    'password': 'AVNS_2oEh5hU00BYuzgIhTXP',
    'database': 'jogomilhao'
}