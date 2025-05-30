
import pygame
from interface import GerenciadorInterfaceTela
from tema import TemaTela
from botao import BotaoTela # Importar BotaoTela para criar os botões aqui
from bancoPergunta import BancoDePerguntasTela # Importar BancoDePerguntasTela para obter as matérias

class TelaSelecaoMateria:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.interface = GerenciadorInterfaceTela(largura, altura) # Usar a interface para fontes e fundo

        self.banco_perguntas_temp = BancoDePerguntasTela() # Instância temporária para buscar matérias
        self.materias_disponiveis = self.banco_perguntas_temp.obter_materias_disponiveis()
        
        self.botoes_materia = []
        self.scroll_offset = 0 # Deslocamento vertical do scroll
        self.largura_botao = 200
        self.altura_botao = 70
        self.espaco_vertical = 20
        self.x_central = (self.largura - self.largura_botao) // 2
        
        self.area_scroll_y_inicio = self.altura * 0.25 # Área onde os botões aparecerão
        self.area_scroll_y_fim = self.altura * 0.9
        self.area_scroll_altura = self.area_scroll_y_fim - self.area_scroll_y_inicio

        self.criar_botoes_materia()

    def criar_botoes_materia(self):
        self.botoes_materia = []
        for i, materia in enumerate(self.materias_disponiveis):
            # A posição Y inicial é calculada com base na área de scroll
            y = self.area_scroll_y_inicio + i * (self.altura_botao + self.espaco_vertical)
            self.botoes_materia.append(
                BotaoTela(self.x_central, y, self.largura_botao, self.altura_botao,
                          TemaTela.CORES['botao_normal'], TemaTela.CORES['borda'], materia,
                          self.interface.fonte_media, TemaTela.CORES['texto_claro'], 15)
            )

    def desenhar(self, tela):
        if self.interface.fundo:
            tela.blit(self.interface.fundo, (0, 0))
        else:
            tela.fill(TemaTela.CORES['fundo'])

        titulo = self.interface.fonte_extra_grande.render("Escolha uma matéria:", True, TemaTela.CORES['texto_claro'])
        tela.blit(titulo, ((self.largura - titulo.get_width()) // 2, self.altura * 0.1))

        # Criar uma superfície para desenhar os botões que serão "scrollados"
        # O tamanho da superfície deve ser o suficiente para conter todos os botões se eles estiverem fora da tela
        conteudo_altura = max(self.area_scroll_altura, len(self.materias_disponiveis) * (self.altura_botao + self.espaco_vertical))
        surf_conteudo = pygame.Surface((self.largura, int(conteudo_altura)), pygame.SRCALPHA)
        surf_conteudo.fill((0,0,0,0)) # Transparente

        for botao in self.botoes_materia:
            # Desenhar o botão na superfície de conteúdo, ajustando a posição Y pelo scroll_offset
            botao_y_deslocado = botao.rect.y - self.area_scroll_y_inicio - self.scroll_offset
            
            # Ajustar o rect do botão para a renderização na superfície
            temp_rect = pygame.Rect(botao.rect.x, botao_y_deslocado, botao.rect.width, botao.rect.height)
            
            # Só desenha se o botão estiver (ou parcialmente estiver) dentro da área de scroll visível
            if temp_rect.top < self.area_scroll_altura and temp_rect.bottom > 0:
                botao_para_desenhar = BotaoTela(
                    botao.rect.x, temp_rect.y, # Usa a posição X original, mas Y deslocada
                    botao.rect.width, botao.rect.height,
                    botao.cor_fundo, botao.cor_borda, botao.texto,
                    botao.fonte, botao.cor_texto, botao.raio_borda
                )
                botao_para_desenhar.desenhar(surf_conteudo)

        # Desenhar a superfície de conteúdo na tela principal
        tela.blit(surf_conteudo, (0, self.area_scroll_y_inicio))

        # Desenhar uma barra de rolagem (opcional, mas bom para feedback visual)
        if len(self.materias_disponiveis) * (self.altura_botao + self.espaco_vertical) > self.area_scroll_altura:
            total_altura_conteudo = len(self.materias_disponiveis) * (self.altura_botao + self.espaco_vertical)
            tamanho_barra_scroll = max(20, int(self.area_scroll_altura * (self.area_scroll_altura / total_altura_conteudo)))
            pos_barra_scroll = int(self.scroll_offset * (self.area_scroll_altura - tamanho_barra_scroll) / (total_altura_conteudo - self.area_scroll_altura))
            
            pygame.draw.rect(tela, TemaTela.CORES['borda'], (self.largura - 30, self.area_scroll_y_inicio, 20, self.area_scroll_altura), 2, border_radius=5)
            pygame.draw.rect(tela, TemaTela.CORES['botao_pular'], (self.largura - 28, self.area_scroll_y_inicio + pos_barra_scroll + 2, 16, tamanho_barra_scroll - 4), border_radius=5)


    def verificar_cliques(self, pos):
        # Ajustar a posição do clique para o offset do scroll
        clique_x, clique_y = pos
        
        # Verificar se o clique está dentro da área de scroll visível
        if not (self.x_central <= clique_x <= self.x_central + self.largura_botao and
                self.area_scroll_y_inicio <= clique_y <= self.area_scroll_y_fim):
            return None # Clique fora da área dos botões de matéria

        for botao in self.botoes_materia:
            # Calcular a posição Y real do botão na tela, considerando o scroll
            botao_y_real = botao.rect.y - self.scroll_offset
            
            # Criar um rect temporário para o botão na sua posição real na tela
            temp_botao_rect = pygame.Rect(botao.rect.x, botao_y_real, botao.rect.width, botao.rect.height)
            
            # Verificar se o clique colide com o botão e se o botão está visível na área de scroll
            if temp_botao_rect.collidepoint(pos) and \
               temp_botao_rect.top < self.area_scroll_y_fim and \
               temp_botao_rect.bottom > self.area_scroll_y_inicio:
                return botao.texto # Retorna o texto (nome da matéria) do botão clicado
        return None

    def lidar_evento_scroll(self, evento):
        # Calcula o limite máximo do scroll
        total_altura_conteudo = len(self.materias_disponiveis) * (self.altura_botao + self.espaco_vertical)
        max_scroll = max(0, total_altura_conteudo - self.area_scroll_altura)

        if evento.button == 4:  # Scroll para cima
            self.scroll_offset = max(0, self.scroll_offset - 30) # Ajuste a velocidade do scroll aqui
        elif evento.button == 5:  # Scroll para baixo
            self.scroll_offset = min(max_scroll, self.scroll_offset + 30) # Ajuste a velocidade do scroll aqui