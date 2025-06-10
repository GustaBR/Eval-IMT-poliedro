import pygame
import config
from botao_menu import BotaoMenu
from sys import exit
from jogo_perguntas.funcionamento_jogo import JogoTela
from estatisticas_tela import EstatisticasTela

class MenuTelaAluno(): 
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador

        # Botões
        ## Botão Jogar
        self.botao_jogar = BotaoMenu(
            texto="Jogar",
            pos=config.figma_para_tela(51, 453),
            cor_padrao=config.LARANJA,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO,
            fonte=config.fonte_botao,
            acao=lambda: self.gerenciador.trocar_tela(JogoTela)
            )

        ## Botão Questões
        self.botao_questoes = BotaoMenu(
            texto="Questões",
            pos=config.figma_para_tela(51, 560),
            cor_padrao=config.VINHO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO,
            fonte=config.fonte_botao
            )

        ## Botão Estatísticas
        self.botao_estatisticas = BotaoMenu(
            texto="Estatísticas",
            pos=config.figma_para_tela(51, 667),
            cor_padrao=config.AZUL_CLARO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO,
            fonte=config.fonte_botao,
            acao=lambda: self.gerenciador.trocar_tela(EstatisticasTela)
        )

        ## Botão Configurações
        self.botao_configuracoes = BotaoMenu(
            texto="Configurações",
            pos=config.figma_para_tela(51, 774),
            cor_padrao=config.SALMAO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO,
            fonte=config.fonte_botao
        )

        ## Botão Sair
        self.botao_sair = BotaoMenu(
            texto="Sair",
            pos=config.figma_para_tela(51, 881),
            cor_padrao=config.VERMELHO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO,
            fonte=config.fonte_botao,
            acao= lambda: (pygame.quit(), exit())
        )

        self.botoes = [self.botao_jogar, self.botao_questoes,
        self.botao_estatisticas, self.botao_configuracoes, self.botao_sair]

        # Logo EVAL
        self.letras_logo = [
            ("E", config.AZUL_CLARO),
            ("V", config.LARANJA),
            ("A", config.LARANJA),
            ("L", config.AZUL_CLARO)
        ]
        self.espacamentos = {
            "E": -14,
            "V": -26,
            "A": -6,
            "padrao": 0
        }
    
    def checar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for botao in self.botoes:
                if botao.hovered:
                    botao.realizar_acao()

    def atualizar(self):
        for botao in self.botoes:
            botao.atualizar_hover()
        
    def exibir(self, janela):
        janela.fill(config.BRANCO_FUNDO)
        janela.fill(config.VERMELHO, ((0, 0), config.figma_para_tela(1440, 404)))

        # Logo EVAL
        x_logo, y_logo = config.figma_para_tela(49, 55)

        for i, (letra, cor) in enumerate(self.letras_logo):
            parte = config.fonte_titulo.render(letra, True, cor)
            janela.blit(parte, (x_logo, y_logo))
            x_logo += parte.get_width()
                
            if i < len(self.letras_logo) - 1:
                x_logo += self.espacamentos.get(letra, self.espacamentos["padrao"])

        for botao in self.botoes:
            botao.exibir_botao(janela)