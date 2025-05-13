import pygame

# Retorna a posição do elemento baseado nas telas do figma
def figma_para_tela(x_figma, y_figma):
    x = int(x_figma * largura_tela / 1440)
    y = int(y_figma * altura_tela / 1024)
    return x, y

# Inicializando o pygame
pygame.init()

# Criando a janela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))

# Tamanhos de fonte
fonte_principal_tamanho_base = int(44 * largura_tela / 1024)  # Tamanho de texto de botões
fonte_principal_tamanho_titulo = fonte_principal_tamanho_base * 5   # Tamanho do título do jogo

# Fontes
fonte_botao = pygame.font.Font("IrishGrover-Regular.ttf", fonte_principal_tamanho_base)
fonte_titulo = pygame.font.Font("IrishGrover-Regular.ttf", fonte_principal_tamanho_titulo)

# Cores
LARANJA = (250, 164, 31)
AZUL_CLARO = (30, 180, 195)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Definindo título e ícone da janela
pygame.display.set_caption("Eval")
'''As 2 linhas abaixo são temporárias e servem para prevenir que o programa
não funcione devido à inexistência do arquivo "nome_do_arquivo.extensao"'''
icone_foi_criado = False
if icone_foi_criado:
    icone = pygame.image.load("nome_do_arquivo.extensao")
    pygame.display.set_icon(icone)

# Classe Botão
class Botao():
    def __init__(self, texto, pos, tamanho, fonte, cor_padrao, cor_texto, cor_hover):
        self.rect = pygame.Rect(pos, tamanho)
        self.texto = texto
        self.fonte = fonte
        self.cor_padrao = cor_padrao
        self.cor_texto = cor_texto
        self.cor_hover = cor_hover
        self.hovered = False

    def atualizar_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, tela):
        color = self.cor_hover if self.hovered else self.cor_padrao
        pygame.draw.rect(tela, color, self.rect, border_radius=10)

        texto_surf = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)

# Instanciando botões
## Botão Jogar
texto_botao_jogar = "Jogar"
pos_botao_jogar = figma_para_tela(51, 453)
tamanho_botao_jogar = figma_para_tela(340, 74)
fonte_botao_jogar = fonte_botao
cor_padrao_botao_jogar = LARANJA
cor_texto_botao_jogar = PRETO
cor_hover_botao_jogar = BRANCO

botao_jogar = Botao(
    texto=texto_botao_jogar,
    pos=pos_botao_jogar,
    tamanho=tamanho_botao_jogar,
    fonte=fonte_botao_jogar,
    cor_padrao=cor_padrao_botao_jogar,
    cor_texto=cor_texto_botao_jogar,
    cor_hover=cor_hover_botao_jogar
)

# Eventos da janela
execucao = True
while execucao:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            execucao = False

    tela.fill((100, 0, 0))

    botao_jogar.atualizar_hover()

    botao_jogar.draw(tela)

    pygame.display.update()
