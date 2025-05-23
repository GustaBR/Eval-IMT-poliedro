import pygame
import sys
import random
from interface import GerenciadorInterfaceTela
from bancoPergunta import BancoDePerguntasTela
from tema import TemaTela
from pergunta import PerguntaTela


class GerenciadorJogoTela:
    def __init__(self):
        pygame.init()
        self.largura = 800
        self.altura = 600
        self.tela_cheia = False
        self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
        pygame.display.set_caption('EVAL - Jogo do Milhão!') # Título da janela

        self.banco_perguntas = BancoDePerguntasTela()
        
        if not self.banco_perguntas.perguntas: # Verifica se o banco de perguntas foi carregado corretamente
            print("ERRO: Nenhuma pergunta foi carregada do banco de dados!")
            pygame.quit()
            sys.exit(1)

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

    def verificar_cliques(self, pos):
        if not hasattr(self.banco_perguntas, 'perguntas') or not self.banco_perguntas.perguntas:
            return

        if self.fim_de_jogo:
            if self.interface.botao_jogar_novamente.clicado(pos):
                self.reiniciar_jogo()
            if self.interface.botao_sair.clicado(pos):
                pygame.quit()
                sys.exit()
            return

        if self.confirmando:
            if self.interface.botao_confirmar.clicado(pos):
                self.processar_resposta(self.opcao_clicada)
                self.confirmando = False
                self.opcao_clicada = None
            elif self.interface.botao_cancelar.clicado(pos):
                self.confirmando = False
                self.opcao_clicada = None
            return

        pergunta = self.banco_perguntas.obter_pergunta_atual()
        if pergunta is None:
            self.fim_de_jogo = True
            return
        
        for i, botao in enumerate(self.interface.botoes_resposta):
            if botao.clicado(pos) and i not in self.respostas_eliminadas:
                self.confirmando = True
                self.opcao_clicada = i
                return

        if self.interface.botao_dica.clicado(pos) and not self.dica_usada:
            self.dica_usada = True
        
        if self.interface.botao_pular.clicado(pos) and not self.pulo_usado:
            if self.banco_perguntas.pular():
                self.pulo_usado = True
                self.dica_usada = False
                self.respostas_eliminadas = []
            if self.banco_perguntas.jogo_acabou():
                self.fim_de_jogo = True
                
        if self.interface.botao_eliminar.clicado(pos) and not self.eliminacao_usada and not self.confirmando:
            self.eliminar_respostas(pergunta)
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
        pergunta = self.banco_perguntas.obter_pergunta_atual()
        if pergunta is None:
            self.fim_de_jogo = True
            return
            
        if indice == pergunta.indice_correto:
            self.pontuacao += 1000
            self.banco_perguntas.avancar()
            self.dica_usada = False
            self.respostas_eliminadas = []
            if self.banco_perguntas.jogo_acabou():
                self.fim_de_jogo = True
        else:
            self.resposta_correta = pergunta.alternativas[pergunta.indice_correto]
            self.fim_de_jogo = True

    def reiniciar_jogo(self):
        self.banco_perguntas.reiniciar()
        self.pontuacao = 0
        self.fim_de_jogo = False
        self.dica_usada = False
        self.pulo_usado = False
        self.eliminacao_usada = False
        self.respostas_eliminadas = []
        self.resposta_correta = None
        self.confirmando = False
        self.opcao_clicada = None

    def desenhar_tela(self):
        if self.interface.fundo:
            self.tela.blit(self.interface.fundo, (0, 0))
        else:
            self.tela.fill(TemaTela.CORES['fundo'])
        
        if not self.fim_de_jogo:
            if self.confirmando:
                self.interface.desenhar_confirmacao(self.tela)
            else:
                pergunta = self.banco_perguntas.obter_pergunta_atual()
                if pergunta is None:
                    self.fim_de_jogo = True
                else:
                    self.interface.desenhar_pergunta(self.tela, pergunta.enunciado)
                    self.interface.desenhar_botoes_resposta(self.tela, pergunta, self.respostas_eliminadas)
                    self.interface.desenhar_botoes_acao(self.tela, self.pulo_usado, self.eliminacao_usada)
                    
                    if self.dica_usada:
                        self.interface.desenhar_dica(self.tela, pergunta.dica)
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
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.verificar_cliques(pygame.mouse.get_pos())

            self.desenhar_tela()
            pygame.display.flip()

        pygame.quit()