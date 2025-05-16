import pygame
import config
from botao import Botao

class Menu():
    def __init__(self):
        # Botões
        ## Botão Jogar
        self.botao_jogar = Botao(
            texto="Jogar",
            pos=config.figma_para_tela(51, 453),
            cor_padrao=config.LARANJA,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO
            )

        ## Botão Questões
        self.botao_questoes = Botao(
            texto="Questões",
            pos=config.figma_para_tela(51, 560),
            cor_padrao=config.VINHO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO
            )

        ## Botão Estatísticas
        self.botao_estatisticas = Botao(
            texto="Estatísticas",
            pos=config.figma_para_tela(51, 667),
            cor_padrao=config.AZUL_CLARO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO
        )

        ## Botão Configurações
        self.botao_configuracoes = Botao(
            texto="Configurações",
            pos=config.figma_para_tela(51, 774),
            cor_padrao=config.SALMAO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO
        )

        self.botao_sair = Botao(
            texto="Sair",
            pos=config.figma_para_tela(51, 881),
            cor_padrao=config.VERMELHO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO
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
            "E": -10,
            "padrao": 1
        }
    
    def atualizar(self):
            for botao in self.botoes:
                botao.atualizar_hover()
        
    def exibir(self, tela):
        tela.fill((config.BRANCO_FUNDO))
        tela.fill(config.VERMELHO, ((0, 0), config.figma_para_tela(1440, 404)))
    
        x_logo, y_logo = config.figma_para_tela(49, 55)

        for i, (letra, cor) in enumerate(self.letras_logo):
            parte = config.fonte_titulo.render(letra, True, cor)
            tela.blit(parte, (x_logo, y_logo))
            x_logo += parte.get_width()
                
            if i < len(self.letras_logo) - 1:
                x_logo += self.espacamentos.get(letra, self.espacamentos["padrao"])
                tela.fill(config.BRANCO_FUNDO)

        for botao in self.botoes:
            botao.exibir_botao(tela)
