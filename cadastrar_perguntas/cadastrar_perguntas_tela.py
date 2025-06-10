from cadastrar_perguntas.config import *
from cadastrar_perguntas.database.database import obter_conexao_bd, buscar_materias_bd
from cadastrar_perguntas.dropdown import *
from cadastrar_perguntas.botao import Botao
from cadastrar_perguntas.caixas_texto import CaixaTextoComPrefixo, CaixaTextoModerna
from config import *

class CadastrarPerguntasTela:
    DURACAO_MENSAGEM = 4000
    
    def __init__(self, gerenciador):
        try:
            self.materias = buscar_materias_bd()
            print(self.materias)
        except Exception as e:
            self.materias = {}
            self.mostrar_mensagem(f"Falha ao carregar matérias: {e}", COR_ERRO, 10000)

        self.dificuldades = {'Fácil': 'F', 'Médio': 'M', 'Difícil': 'D'}

        self.gerenciador = gerenciador
        self.mensagem_texto = ""
        self.mensagem_cor = COR_ERRO
        self.mensagem_inicio_tempo = 0
        self.caixa_pergunta = CaixaTextoModerna(50, 160, int(1100 * LARGURA_JANELA / 1200), 150, FONTE_NORMAL, "Digite o enunciado aqui…")
        self.caixas_alternativas = [CaixaTextoComPrefixo(50, 350 + i * 60, int(1100 * LARGURA_JANELA / 1200), 50, FONTE_NORMAL, "Alternativa", prefixo=f"{rotulo}) ") for i, rotulo in enumerate("ABCD")]
        self.grupo_radio_respostas = GrupoRadio(50, 350 + 4 * 60 + 40, ["A", "B", "C", "D"], FONTE_NORMAL)
        self.menu_materias = MenuSuspenso(50, 80, 400, 50, FONTE_NORMAL, self.materias, "Selecionar Matéria")
        self.menu_dificuldade = MenuSuspenso(500, 80, 300, 50, FONTE_NORMAL, self.dificuldades, "Selecionar Dificuldade")
        self.botao_cadastrar = Botao("Cadastrar Questão", 850, 80, int(300 * LARGURA_JANELA / 1200), 50, lambda: self.cadastrar_questao())

        self.componentes = [self.caixa_pergunta] + self.caixas_alternativas + [self.grupo_radio_respostas, self.menu_materias, self.menu_dificuldade, self.botao_cadastrar]

    def mostrar_mensagem(self, texto, cor, duracao=None):
        self.mensagem_texto = texto
        self.mensagem_cor = cor
        self.mensagem_inicio_tempo = pygame.time.get_ticks()


    def limpar_campos(self):
        self.caixa_pergunta.definir_texto("")
        for caixa in self.caixas_alternativas:
            caixa.definir_texto("")
        self.grupo_radio_respostas.selecionado_idx = None
        self.menu_materias.selecionada = None
        self.menu_dificuldade.selecionada = None


    def cadastrar_questao(self):
        pergunta = self.caixa_pergunta.obter_texto().strip()
        alternativas = [caixa.obter_texto().strip() for caixa in self.caixas_alternativas]
        indice_correto = self.grupo_radio_respostas.selecionado_idx
        dificuldade_str = self.menu_dificuldade.selecionada
        materia_str = self.menu_materias.selecionada
        print(materia_str)

        if not all([pergunta, all(alternativas), indice_correto is not None, dificuldade_str, materia_str]):
            self.mostrar_mensagem("ERRO: Preencha todos os campos!", COR_ERRO)
            return
        
        conexao = None
        try:
            conexao = obter_conexao_bd()
            cursor = conexao.cursor()
            mapa_dificuldade = {'Fácil': 'F', 'Médio': 'M', 'Difícil': 'D'}
            materia = materia_str

            sql_q = "INSERT INTO questoes (difQuest, enuncQuest, nomeMateria) VALUES (%s, %s, %s)"
            cursor.execute(sql_q, (mapa_dificuldade[dificuldade_str], pergunta, materia))
            id_questao = cursor.lastrowid

            sql_a = "INSERT INTO alternativas (resposta, correta, idQuest) VALUES (%s, %s, %s)"
            for i, alt in enumerate(alternativas):
                cursor.execute(sql_a, (alt, (i == indice_correto), id_questao))
                
            conexao.commit()
            self.mostrar_mensagem(f"SUCESSO: Questão (ID: {id_questao}) cadastrada!", COR_SUCESSO)
            self.limpar_campos()
            
        except Exception as e:
            if conexao: conexao.rollback()
            self.mostrar_mensagem(f"ERRO DE BANCO DE DADOS: {e}", COR_ERRO)
        finally:
            if conexao and conexao.is_connected():
                conexao.close()

    
    def checar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            from menu_tela_professor import MenuTelaProfessor
            self.gerenciador.trocar_tela(MenuTelaProfessor)
        for componente in self.componentes:
            componente.tratar_evento(evento)
    

    def atualizar(self):
        for componente in self.componentes:
            componente.atualizar(dt)
        

    def exibir(self, janela):
        janela.fill(COR_FUNDO)
        FONTE_TITULO.render_to(janela, (50, 20), "Criador de Questões", COR_TEXTO_TITULO)
        FONTE_NORMAL.render_to(janela, (50, 135), "Enunciado da Pergunta:", COR_TEXTO_TITULO)
        FONTE_NORMAL.render_to(janela, (50, 325), "Alternativas:", COR_TEXTO_TITULO)
        FONTE_NORMAL.render_to(janela, (50, 585), "Resposta Correta:", COR_TEXTO_TITULO)
        
        for componente in self.componentes:
            componente.desenhar(janela)
        
        if self.mensagem_texto and pygame.time.get_ticks() - self.mensagem_inicio_tempo < self.DURACAO_MENSAGEM:
            surf_texto, ret_texto = FONTE_NORMAL.render(self.mensagem_texto, self.mensagem_cor)
            janela.blit(surf_texto, ((LARGURA - ret_texto.width) // 2, ALTURA - ret_texto.height - 20))
        else:
            self.mensagem_texto = ""
