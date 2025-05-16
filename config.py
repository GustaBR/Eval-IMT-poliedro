import pygame

# Tamanho da tela
LARGURA_TELA = 720
ALTURA_TELA = 512

# Retorna a posição do elemento na tela com base no figma
def figma_para_tela(x_figma, y_figma):
    x = int(x_figma * LARGURA_TELA / 1440)
    y = int(y_figma * ALTURA_TELA / 1024)
    return x, y

# Tamanhos de fonte
fonte_principal_tamanho_base = int(44 * ALTURA_TELA / 1024) # Tamanho de texto de botões
fonte_principal_tamanho_titulo = fonte_principal_tamanho_base * 5 # Tamanho do título do jogo

# Fontes
fonte_botao = pygame.font.Font("IrishGrover-Regular.ttf", fonte_principal_tamanho_base)
fonte_titulo = pygame.font.Font("IrishGrover-Regular.ttf", fonte_principal_tamanho_titulo)

# Cores
LARANJA = (250, 164, 31) # FAA41F
AZUL_CLARO = (30, 180, 195) # 1EB4C3
BRANCO = (255, 255, 255) # FFFFFF
BRANCO_FUNDO = (245, 235, 221) # F5EBDD
PRETO = (0, 0, 0) # 000000
VINHO = (132, 64, 69) # 844045
SALMAO = (200, 126, 131) # C87E83
VERMELHO = (230, 57, 70) # E63946
