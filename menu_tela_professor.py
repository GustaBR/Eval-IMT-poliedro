import pygame
import config
from botao_menu import BotaoMenu
from sys import exit
from cadastrar_usuarios.componentes.cadastrar_usuarios_tela import CadastrarUsuariosTela
from cadastrar_materias.cadastrar_materias_tela import CadastrarMateriasTela
from rank.ranking_tela import RankingTela
from cadastrar_perguntas.cadastrar_perguntas_tela import CadastrarPerguntasTela

class MenuTelaProfessor():
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador

        # Botões
        ## Botão Ranking
        self.botao_ranking = BotaoMenu(
            texto="Ranking",
            pos=config.figma_para_tela(51, 453),
            cor_padrao=config.LARANJA,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO,
            fonte=config.fonte_botao,
            acao=lambda: self.gerenciador.trocar_tela(RankingTela)
            )

        ## Botão Questões
        self.botao_questoes = BotaoMenu(
            texto="Questões",
            pos=config.figma_para_tela(51, 560),
            cor_padrao=config.VINHO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO,
            fonte=config.fonte_botao,
            acao= lambda: self.gerenciador.trocar_tela(CadastrarPerguntasTela)
            )

        ## Botão Usuários
        self.botao_alunos = BotaoMenu(
            texto="Usuários",
            pos=config.figma_para_tela(51, 667),
            cor_padrao=config.AZUL_CLARO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO,
            fonte=config.fonte_botao,
            acao=lambda: self.gerenciador.trocar_tela(CadastrarUsuariosTela)
        )

        ## Botão Matérias
        self.botao_materias = BotaoMenu(
            texto="Matérias",
            pos=config.figma_para_tela(51, 774),
            cor_padrao=config.SALMAO,
            cor_texto=config.PRETO,
            cor_hover=config.BRANCO,
            fonte=config.fonte_botao,
            acao=lambda: self.gerenciador.trocar_tela(CadastrarMateriasTela)
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

        self.botoes = [self.botao_ranking, self.botao_questoes,
            self.botao_alunos, self.botao_materias, self.botao_sair]

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
