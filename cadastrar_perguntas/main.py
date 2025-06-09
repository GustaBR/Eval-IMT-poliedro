import pygame
import sys
from config import *
from database.database import obter_conexao_bd, buscar_materias_bd
from dropdown import *
from botao import Botao

FPS = 60

pygame.init()
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Criador de Questões - Poliedro")
relogio = pygame.time.Clock()

mensagem_texto = ""
mensagem_cor = COR_ERRO
mensagem_inicio_tempo = 0
DURACAO_MENSAGEM = 4000 

def mostrar_mensagem(texto, cor, duracao=DURACAO_MENSAGEM):
    global mensagem_texto, mensagem_cor, mensagem_inicio_tempo
    mensagem_texto = texto
    mensagem_cor = cor
    mensagem_inicio_tempo = pygame.time.get_ticks()


def limpar_campos():
    caixa_pergunta.definir_texto("")
    for caixa in caixas_alternativas:
        caixa.definir_texto("")
    grupo_radio_respostas.selecionado_idx = None
    menu_materias.selecionada = None
    menu_dificuldade.selecionada = None

def cadastrar_questao():
    pergunta = caixa_pergunta.obter_texto().strip()
    alternativas = [caixa.obter_texto().strip() for caixa in caixas_alternativas]
    indice_correto = grupo_radio_respostas.selecionado_idx
    dificuldade_str = menu_dificuldade.selecionada
    materia_str = menu_materias.selecionada

    if not all([pergunta, all(alternativas), indice_correto is not None, dificuldade_str, materia_str]):
        mostrar_mensagem("ERRO: Preencha todos os campos!", COR_ERRO)
        return
    
    conexao = None
    try:
        conexao = obter_conexao_bd()
        cursor = conexao.cursor()
        mapa_dificuldade = {'Fácil': 'F', 'Médio': 'M', 'Difícil': 'D'}
        id_materia = materias[materia_str]
        
        sql_q = "INSERT INTO questoes (difQuest, enuncQuest, idMateria) VALUES (%s, %s, %s)"
        cursor.execute(sql_q, (mapa_dificuldade[dificuldade_str], pergunta, id_materia))
        id_questao = cursor.lastrowid
        
        sql_a = "INSERT INTO alternativas (resposta, correta, idQuest) VALUES (%s, %s, %s)"
        for i, alt in enumerate(alternativas):
            cursor.execute(sql_a, (alt, (i == indice_correto), id_questao))
        
        conexao.commit()
        mostrar_mensagem(f"SUCESSO: Questão (ID: {id_questao}) cadastrada!", COR_SUCESSO)
        limpar_campos()
    except Exception as e:
        if conexao: conexao.rollback()
        mostrar_mensagem(f"ERRO DE BANCO DE DADOS: {e}", COR_ERRO)
    finally:
        if conexao and conexao.is_connected():
            conexao.close()

try:
    materias = buscar_materias_bd()
except Exception as e:
    materias = {}
    mostrar_mensagem(f"Falha ao carregar matérias: {e}", COR_ERRO, 10000)

dificuldades = {'Fácil': 'F', 'Médio': 'M', 'Difícil': 'D'}

caixa_pergunta = CaixaTextoModerna(50, 160, 1100, 150, FONTE_NORMAL, "Digite o enunciado aqui…")
caixas_alternativas = [CaixaTextoComPrefixo(50, 350 + i * 60, 1100, 50, FONTE_NORMAL, "Alternativa", prefixo=f"{rotulo}) ") for i, rotulo in enumerate("ABCD")]
grupo_radio_respostas = GrupoRadio(50, 350 + 4 * 60 + 40, ["A", "B", "C", "D"], FONTE_NORMAL)
menu_materias = MenuSuspenso(50, 80, 400, 50, FONTE_NORMAL, materias, "Selecionar Matéria")
menu_dificuldade = MenuSuspenso(500, 80, 300, 50, FONTE_NORMAL, dificuldades, "Selecionar Dificuldade")
botao_cadastrar = Botao("Cadastrar Questão", 850, 80, 300, 50, cadastrar_questao)

componentes = [caixa_pergunta] + caixas_alternativas + [grupo_radio_respostas, menu_materias, menu_dificuldade, botao_cadastrar]

def rodar_aplicacao():
    global mensagem_texto
    executando = True
    while executando:
        dt = relogio.tick(FPS)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            for componente in componentes:
                componente.tratar_evento(evento)
        
        for componente in componentes:
            componente.atualizar(dt)
        
        TELA.fill(COR_FUNDO)
        FONTE_TITULO.render_to(TELA, (50, 20), "Criador de Questões", COR_TEXTO_TITULO)
        FONTE_NORMAL.render_to(TELA, (50, 135), "Enunciado da Pergunta:", COR_TEXTO_TITULO)
        FONTE_NORMAL.render_to(TELA, (50, 325), "Alternativas:", COR_TEXTO_TITULO)
        FONTE_NORMAL.render_to(TELA, (50, 585), "Resposta Correta:", COR_TEXTO_TITULO)
        
        for componente in componentes:
            componente.desenhar(TELA)
        
        if mensagem_texto and pygame.time.get_ticks() - mensagem_inicio_tempo < DURACAO_MENSAGEM:
            surf_texto, ret_texto = FONTE_NORMAL.render(mensagem_texto, mensagem_cor)
            TELA.blit(surf_texto, ((LARGURA - ret_texto.width) // 2, ALTURA - ret_texto.height - 20))
        else:
            mensagem_texto = ""

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    rodar_aplicacao()