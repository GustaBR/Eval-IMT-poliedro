import pygame

# Retorna a posição do elemento na tela com base no figma
def figma_para_tela(x_figma, y_figma):
    x = int(x_figma * largura_tela / 1440)
    y = int(y_figma * altura_tela / 1024)
    return x, y

# Inicializando o pygame
pygame.init()

# Criando a janela
largura_tela = 720
altura_tela = 512
tela = pygame.display.set_mode((largura_tela, altura_tela))

# Tamanhos de fonte
fonte_principal_tamanho_base = int(44 * altura_tela / 1024) # Tamanho de texto de botões
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
    def __init__(self, texto, pos, cor_padrao, cor_texto, cor_hover):
        self.fonte = fonte_botao
        self.tamanho = figma_para_tela(340, 74)
        self.rect = pygame.Rect(pos, self.tamanho)
        self.texto = texto
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

# Botões
## Botão Jogar
botao_jogar = Botao(
    texto="Jogar",
    pos=figma_para_tela(51, 453),
    cor_padrao=LARANJA,
    cor_texto=PRETO,
    cor_hover=BRANCO
    )

## Botão Questões
botao_questoes = Botao(
    texto="Questões",
    pos=figma_para_tela(51, 560),
    cor_padrao=VINHO,
    cor_texto=PRETO,
    cor_hover=BRANCO
    )

## Botão Estatísticas
botao_estatisticas = Botao(
    texto="Estatísticas",
    pos=figma_para_tela(51, 667),
    cor_padrao=AZUL_CLARO,
    cor_texto=PRETO,
    cor_hover=BRANCO
)

## Botão Configurações
botao_configuracoes = Botao(
    texto="Configurações",
    pos=figma_para_tela(51, 774),
    cor_padrao=SALMAO,
    cor_texto=PRETO,
    cor_hover=BRANCO
)

botao_sair = Botao(
    texto="Sair",
    pos=figma_para_tela(51, 881),
    cor_padrao=VERMELHO,
    cor_texto=PRETO,
    cor_hover=BRANCO
)

botoes = [botao_jogar, botao_questoes, botao_estatisticas,
botao_configuracoes, botao_sair]

# Logo EVAL
letras_logo = [
    ("E", AZUL_CLARO),
    ("V", LARANJA),
    ("A", LARANJA),
    ("L", AZUL_CLARO)
]
espacamentos = {
    "E": -10,
    "padrao": 1

}

# Eventos da janela
execucao = True
while execucao:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            execucao = False

    tela.fill((BRANCO_FUNDO))
    tela.fill(VERMELHO, ((0, 0), figma_para_tela(1440, 404)))
    
    x_logo, y_logo = figma_para_tela(49, 55)

    for i, (letra, cor) in enumerate(letras_logo):
        parte = fonte_titulo.render(letra, True, cor)
        tela.blit(parte, (x_logo, y_logo))
        x_logo += parte.get_width()
        
        if i < len(letras_logo) - 1:
            x_logo += espacamentos.get(letra, espacamentos["padrao"])

    for botao in botoes:
        botao.atualizar_hover()
        botao.draw(tela)

    pygame.display.update()