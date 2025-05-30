import pygame
import sys
import random
from interface import GerenciadorInterfaceTela
from bancoPergunta import BancoDePerguntasTela
from tema import TemaTela
from pergunta import PerguntaTela
from selecaoMateria import TelaSelecaoMateria

class GerenciadorJogoTela:
    def __init__(self):
        pygame.init()
        self.largura = 800
        self.altura = 600
        self.tela_cheia = False
        self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
        pygame.display.set_caption('EVAL - Jogo do Milhão!')

        self.clock = pygame.time.Clock()
        self.FPS = 60 

        self.estado_jogo = "SELECAO_MATERIA"
        self.tela_selecao_materia = TelaSelecaoMateria(self.largura, self.altura)

        self.banco_perguntas = None
        self.interface = GerenciadorInterfaceTela(self.largura, self.altura)
        self.pontuacao = 0
        self.fim_de_jogo = False
        self.dica_usada = False
        self.pulo_usado = False
        self.eliminacao_usada = False
        self.respostas_eliminadas = []
        self.resposta_correta = None
        self.confirmando = False
        self.opcao_clicada = None
        self.pergunta_atual_obj = None

    def alternar_tela_cheia(self):
        self.tela_cheia = not self.tela_cheia
        if self.tela_cheia:
            info = pygame.display.Info()
            self.largura, self.altura = info.current_w, info.current_h
            self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.FULLSCREEN)
        else:
            self.largura, self.altura = 800, 600
            self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)

        self.interface = GerenciadorInterfaceTela(self.largura, self.altura)
        self.tela_selecao_materia = TelaSelecaoMateria(self.largura, self.altura)
        if self.banco_perguntas:
            self.banco_perguntas.reiniciar()

    def verificar_cliques(self, pos):
        if self.estado_jogo == "SELECAO_MATERIA":
            materia_selecionada = self.tela_selecao_materia.verificar_cliques(pos)
            if materia_selecionada:
                self.banco_perguntas = BancoDePerguntasTela(materia_selecionada)
                if self.banco_perguntas.perguntas:
                    random.shuffle(self.banco_perguntas.perguntas)
                    self.estado_jogo = "JOGANDO"
                    self.pergunta_atual_obj = self.banco_perguntas.obter_pergunta_atual()
                else:
                    print(f"Nenhuma pergunta carregada para a matéria '{materia_selecionada}'. Por favor, tente outra matéria.")
                    self.banco_perguntas = None
            return

        if self.fim_de_jogo:
            if self.interface.botao_jogar_novamente.clicado(pos):
                self.reiniciar_jogo()
            elif self.interface.botao_sair.clicado(pos):
                pygame.quit()
                sys.exit()
            return

        # *** PRIORIDADE: Se estiver confirmando, apenas os botões de confirmação devem ser clicáveis ***
        if self.confirmando:
            if self.interface.botao_confirmar.clicado(pos):
                self.processar_resposta(self.opcao_clicada)
                self.confirmando = False
                self.opcao_clicada = None
            elif self.interface.botao_cancelar.clicado(pos):
                self.confirmando = False
                self.opcao_clicada = None
            return # Sai da função para não processar outros cliques

        # Apenas processa cliques em outras áreas se NÃO ESTIVER CONFIRMANDO
        if self.estado_jogo == "JOGANDO" and self.pergunta_atual_obj:
            for i, botao in enumerate(self.interface.botoes_resposta):
                # Só permite clique em botões de resposta se não estiver confirmando
                if botao.clicado(pos) and i not in self.respostas_eliminadas:
                    self.confirmando = True
                    self.opcao_clicada = i
                    return

            if self.interface.botao_dica.clicado(pos) and not self.dica_usada:
                self.dica_usada = True
            
            if self.interface.botao_pular.clicado(pos) and not self.pulo_usado:
                if self.banco_perguntas.pular():
                    self.pulo_usado = True
                    self.eliminacao_usada = False
                    self.respostas_eliminadas = []
                    self.pergunta_atual_obj = self.banco_perguntas.obter_pergunta_atual()
                if self.banco_perguntas.jogo_acabou():
                    self.fim_de_jogo = True
                    
            if self.interface.botao_eliminar.clicado(pos) and not self.eliminacao_usada:
                self.eliminar_respostas(self.pergunta_atual_obj)
                self.eliminacao_usada = True

    def eliminar_respostas(self, pergunta):
        if pergunta is None:
            return
            
        opcoes_erradas = [i for i in range(len(pergunta.alternativas)) 
                         if i != pergunta.indice_correto 
                         and i not in self.respostas_eliminadas]
        
        num_eliminar = min(2, len(opcoes_erradas))
        
        if num_eliminar > 0:
            self.respostas_eliminadas.extend(random.sample(opcoes_erradas, num_eliminar))

    def processar_resposta(self, indice):
        if self.pergunta_atual_obj is None:
            self.fim_de_jogo = True
            return
            
        if indice == self.pergunta_atual_obj.indice_correto:
            self.pontuacao += 1000
            self.banco_perguntas.avancar()
            self.eliminacao_usada = False
            self.respostas_eliminadas = []
            self.pergunta_atual_obj = self.banco_perguntas.obter_pergunta_atual()
            if self.banco_perguntas.jogo_acabou():
                self.fim_de_jogo = True
        else:
            self.resposta_correta = self.pergunta_atual_obj.alternativas[self.pergunta_atual_obj.indice_correto]
            self.fim_de_jogo = True

    def reiniciar_jogo(self):
        self.banco_perguntas = None
        self.estado_jogo = "SELECAO_MATERIA"
        self.pontuacao = 0
        self.fim_de_jogo = False
        self.dica_usada = False
        self.pulo_usado = False
        self.eliminacao_usada = False
        self.respostas_eliminadas = []
        self.resposta_correta = None
        self.confirmando = False # Garante que o estado de confirmação é resetado
        self.opcao_clicada = None
        self.pergunta_atual_obj = None
        self.tela_selecao_materia = TelaSelecaoMateria(self.largura, self.altura)

    def desenhar_tela(self):
        if self.interface.fundo:
            self.tela.blit(self.interface.fundo, (0, 0))
        else:
            self.tela.fill(TemaTela.CORES['fundo'])
        
        if self.estado_jogo == "SELECAO_MATERIA":
            self.tela_selecao_materia.desenhar(self.tela)
        elif self.estado_jogo == "JOGANDO":
            if not self.fim_de_jogo:
                if self.pergunta_atual_obj:
                    # Desenha a pergunta e as alternativas
                    self.interface.desenhar_pergunta(self.tela, self.pergunta_atual_obj.enunciado)
                    self.interface.desenhar_botoes_resposta(self.tela, self.pergunta_atual_obj, self.respostas_eliminadas)
                    
                    # Desenha os botões de ação e a dica APENAS SE NÃO ESTIVER CONFIRMANDO
                    if not self.confirmando:
                        self.interface.desenhar_botoes_acao(self.tela, self.pulo_usado, self.eliminacao_usada, self.dica_usada)
                        if self.dica_usada: # Desenha a dica se foi usada
                            self.interface.desenhar_dica(self.tela, self.pergunta_atual_obj.dica)
                    
                else:
                    self.fim_de_jogo = True # Se não há pergunta, considerar fim de jogo

                # *** Desenha a caixa de confirmação por cima de tudo, se estiver ativa ***
                if self.confirmando:
                    self.interface.desenhar_confirmacao(self.tela)
            else:
                self.interface.desenhar_tela_fim(self.tela, self.pontuacao, self.resposta_correta)

    def rodar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
                    self.alternar_tela_cheia()
                elif evento.type == pygame.VIDEORESIZE:
                    if not self.tela_cheia:
                        self.largura, self.altura = evento.size
                        self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
                        self.interface = GerenciadorInterfaceTela(self.largura, self.altura)
                        self.tela_selecao_materia = TelaSelecaoMateria(self.largura, self.altura)
                        if self.estado_jogo == "JOGANDO" and self.banco_perguntas:
                            self.pergunta_atual_obj = self.banco_perguntas.obter_pergunta_atual()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.estado_jogo == "SELECAO_MATERIA" and evento.button in (4, 5):
                        self.tela_selecao_materia.lidar_evento_scroll(evento)
                    else:
                        self.verificar_cliques(pygame.mouse.get_pos())

            self.desenhar_tela()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()