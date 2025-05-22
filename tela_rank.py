# *** NÃO MEXER *** 
# -----------------------------------------------------------------------------------------------------------------
# IMPORTAÇÕES
# ================================================================================================================= 
import pygame # type: ignore
# pip install pygame
import sys
import mysql.connector # type: ignore
# pip install --upgrade mysql-connector-python
# =================================================================================================================
# BANCO DE DADOS
# =================================================================================================================
def carregar_dados_do_banco():
    try:
        conexao = mysql.connector.connect(
            host="jogomilhao-pi11semestre.l.aivencloud.com",
            user="avnadmin",
            port="25159",
            password="AVNS_2oEh5hU00BYuzgIhTXP",
            database="jogomilhao"
        )
        cursor = conexao.cursor()
        cursor.execute("SELECT nomeAluno, pontuacao FROM aluno ORDER BY pontuacao DESC LIMIT 100")
        dados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [{"nome": nome, "pontuacao": pontuacao} for nome, pontuacao in dados]
    except mysql.connector.Error as err:
        print("Erro ao conectar ao banco de dados:", err)
        return []
# =================================================================================================================
# -----------------------------------------------------------------------------------------------------------------
# Inicializando o Pygame
pygame.init()

# Cores
AZUL_CLARO = (30, 144, 255)
DOURADO = (218, 165, 32)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_CLARO = (220, 220, 220)
CINZA_ESCURO = (169, 169, 169)

# Tamanho inicial
LARGURA, ALTURA = 900, 600
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Ranking")

# Fontes
fonte_titulo = pygame.font.SysFont("comicsansms", 64)
fonte_input = pygame.font.SysFont("comicsansms", 24)

# Função para desenhar texto na tela
def desenhar_texto(texto, fonte, cor, superficie, x, y):
    texto_obj = fonte.render(texto, True, cor)
    superficie.blit(texto_obj, (x, y))

# Utilizar banco de dados
ranking = carregar_dados_do_banco()

# Variáveis itens
ITEM_ALTURA = 60
ITENS_VISIVEIS = 6

def main():
    global LARGURA, ALTURA, tela

    clock = pygame.time.Clock()
    scroll_offset = 0
    input_ativo = False
    texto_busca = ""

    while True:
        tela.fill(AZUL_CLARO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.VIDEORESIZE:
                # Redimensionar Tela
                LARGURA, ALTURA = evento.w, evento.h
                tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if 170 <= evento.pos[0] <= 650 and 135 <= evento.pos[1] <= 175:
                    input_ativo = True
                else:
                    input_ativo = False
                if evento.button == 4:
                    scroll_offset = max(scroll_offset - ITEM_ALTURA, 0)
                elif evento.button == 5:
                    scroll_offset += ITEM_ALTURA
            elif evento.type == pygame.KEYDOWN:
                if input_ativo:
                    if evento.key == pygame.K_BACKSPACE:
                        texto_busca = texto_busca[:-1]
                    else:
                        texto_busca += evento.unicode
                else:
                    if evento.key == pygame.K_UP:
                        scroll_offset = max(scroll_offset - ITEM_ALTURA, 0)
                    elif evento.key == pygame.K_DOWN:
                        scroll_offset += ITEM_ALTURA

        # Redimensionar Elementos
        desenhar_texto("Ranking", fonte_titulo, BRANCO, tela, LARGURA // 2 - 130, 30)

        pygame.draw.rect(tela, DOURADO, (70, 130, LARGURA - 140, 50))
        pygame.draw.rect(tela, BRANCO, (90, 135, 70, 40))
        desenhar_texto("Rank", fonte_input, PRETO, tela, 100, 140)

        pygame.draw.rect(tela, BRANCO, (170, 135, LARGURA - 320, 40))
        cor_borda = PRETO if input_ativo else CINZA_CLARO
        pygame.draw.rect(tela, cor_borda, (170, 135, LARGURA - 320, 40), 2)
        desenhar_texto(texto_busca or "🔍 Procurar", fonte_input, PRETO, tela, 180, 140)

        pygame.draw.rect(tela, BRANCO, (LARGURA - 240, 135, 150, 40))
        desenhar_texto("Pontuação", fonte_input, PRETO, tela, LARGURA - 230, 140)

        ranking_filtrado = [j for j in ranking if texto_busca.lower() in j["nome"].lower()]
        total_itens = len(ranking_filtrado)
        max_offset = max(0, (total_itens - ITENS_VISIVEIS) * ITEM_ALTURA)
        scroll_offset = min(scroll_offset, max_offset)

        y_base = 200
        inicio = scroll_offset // ITEM_ALTURA
        fim = inicio + ITENS_VISIVEIS

        for i, jogador in enumerate(ranking_filtrado[inicio:fim]):
            pos_y = y_base + i * ITEM_ALTURA
            pygame.draw.rect(tela, PRETO, (80, pos_y, LARGURA - 160, 40))
            pygame.draw.rect(tela, CINZA_CLARO, (85, pos_y + 5, 60, 30))
            pygame.draw.rect(tela, CINZA_CLARO, (155, pos_y + 5, LARGURA - 460, 30))
            pygame.draw.rect(tela, CINZA_CLARO, (LARGURA - 235, pos_y + 5, 140, 30))
            desenhar_texto(str(inicio + i + 1), fonte_input, PRETO, tela, 95, pos_y + 10)
            desenhar_texto(jogador["nome"], fonte_input, PRETO, tela, 165, pos_y + 10)
            desenhar_texto(str(jogador["pontuacao"]), fonte_input, PRETO, tela, LARGURA - 225, pos_y + 10)

        pygame.display.flip()
        clock.tick(60)

main()
