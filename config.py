import pygame
import os

# Número de frames/s
frames = 60

# Tempo entre frames
cronometro = pygame.time.Clock()
dt = cronometro.tick(frames)

# Tamanho da janela
LARGURA_JANELA = 720
ALTURA_JANELA = 512

# Retorna a posição do elemento na tela com base no figma
def figma_para_tela(x_figma, y_figma):
    x = int(x_figma * LARGURA_JANELA / 1440)
    y = int(y_figma * ALTURA_JANELA / 1024)
    return x, y

# Cores
LARANJA = (250, 164, 31) # #FAA41F
AZUL_CLARO = (30, 180, 195) # #1EB4C3
BRANCO = (255, 255, 255) # #FFFFFF
BRANCO_FUNDO = (245, 235, 221) # #F5EBDD
PRETO = (0, 0, 0) # #000000
VINHO = (132, 64, 69) # #844045
SALMAO = (200, 126, 131) # #C87E83
VERMELHO = (230, 57, 70) # #E63946
AZUL_LOGIN = (0, 76, 151) # #004C97
AZUL_ESCURO_LOGIN = (0, 60, 120) # #003C78
AZUL_CLARO_LOGIN = (51, 122, 204) # #337ACC

# Tema Poliedro
Tema_Poliedro = {
    "bg": (245, 245, 250),
    "text": (25, 25, 30),
    "accent": AZUL_LOGIN,
    "accent_hover": AZUL_ESCURO_LOGIN,
    "error": (220, 50, 50),
    "input_bg": (255, 255, 255),
    "input_border": AZUL_LOGIN,
    "input_focus": AZUL_LOGIN,
    "btn_bg": AZUL_LOGIN,
    "btn_disabled": (160, 160, 160),
    "placeholder": (150, 150, 160),
    "shadow": (0, 0, 0, 25),
}

# Caminhos dos assets (imagens e sons)
imagem = os.path.join(os.path.dirname(__file__), "imagens")

icone_usuario = os.path.join(imagem, "icone_usuario.png")
icone_cadeado = os.path.join(imagem, "icone_cadeado.png")
icone_olho_on = os.path.join(imagem, "icone_olho_aberto.png")
icone_olho_off = os.path.join(imagem, "icone_olho_fechado.png")

def criar_fontes():
    # Tamanhos de fonte
    fonte_principal_tamanho_base = int(44 * ALTURA_JANELA / 1024) # Tamanho de texto de botões
    fonte_principal_tamanho_titulo = fonte_principal_tamanho_base * 5 # Tamanho do título do jogo

    # Fontes
    import pygame
    global fonte_botao, fonte_titulo
    fonte_botao = pygame.font.Font("IrishGrover-Regular.ttf", fonte_principal_tamanho_base)
    fonte_titulo = pygame.font.Font("IrishGrover-Regular.ttf", fonte_principal_tamanho_titulo)

def criar_fontes_login(size, bold=False, italic=False):
    return pygame.font.SysFont("Segoe UI", size, bold=bold, italic=italic)

fonte_regular = criar_fontes_login(20)
fonte_negrito = criar_fontes_login(26, True)
fonte_pequeno = criar_fontes_login(14)
fonte_ital = criar_fontes_login(18, italic=True)

def carregar_audio(nome):
    caminho = os.path.join(imagem, nome)
    try:
        return pygame.mixer.Sound(caminho)
    except Exception:
        return None

som_clicar = carregar_audio("click.wav") # Arquivo de áudio
som_erro = carregar_audio("error.wav") # Arquivo de áudio
som_correto = carregar_audio("success.wav") # Arquivo de áudio