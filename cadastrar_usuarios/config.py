import pygame

class ConfigTela:
    LARGURA_JANELA = 1200
    ALTURA_JANELA = 900
    LARGURA_CAMPO = 700
    ALTURA_CAMPO = 70
    ESPACO_ENTRE = 130

    COR_ATIVO = (30, 30, 30)
    COR_INATIVO = (160, 160, 160)
    COR_BORDA_ATIVO = (100, 180, 255)
    COR_BORDA_INATIVO = (200, 200, 200)
    COR_BOTAO = (70, 150, 230)
    COR_BOTAO_HOVER = (100, 180, 255)
    COR_MSG = (200, 50, 50)
    COR_SELECAO = (70, 130, 220)
    COR_PLACEHOLDER = (180, 180, 180)

    FONTE_PADRAO = pygame.font.Font(None, 42)
    FONTE_MSG = pygame.font.Font(None, 32)
