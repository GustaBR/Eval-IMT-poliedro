import pygame
from tema.tema_visual import Tema
from tema.elementos_cores import Botao
# Não precisa de 'config' diretamente, pois recebe LARGURA_TELA, ALTURA_TELA e gerenciador_jogo

class TelaSelecaoMateria:
    def __init__(self, largura_tela, altura_tela, gerenciador_jogo_ref): 
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.gerenciador_jogo = gerenciador_jogo_ref
        self.interface_grafica = gerenciador_jogo_ref.interface_grafica

        self.banco_perguntas = self.gerenciador_jogo.gerenciador_banco
        self.lista_materias_disponiveis = self.banco_perguntas.obter_materias_disponiveis()
        
        # Exibe notificações sobre conexão e matérias através da instância de GerenciadorInterface
        if not self.banco_perguntas.conexao or not self.banco_perguntas.conexao.is_connected():
            if not (self.interface_grafica.notificacao_ativa and "Falha ao conectar" in self.interface_grafica.notificacao_texto):
                self.interface_grafica.exibir_notificacao("Falha ao conectar ao banco de dados.", "erro", 5000)
        elif not self.lista_materias_disponiveis: # Se conexão ok, mas sem matérias
            self.interface_grafica.exibir_notificacao("Nenhuma matéria foi encontrada no banco.", "erro", 5000)

        self.lista_botoes_materia = []
        self.offset_scroll_conteudo_y = 0
        self.largura_botao_materia_item = self.largura_tela * 0.65 
        self.altura_botao_materia_item = self.altura_tela * 0.08
        self.espaco_vertical_entre_botoes = self.altura_tela * 0.025
        self.pos_x_botoes_materia = (self.largura_tela - self.largura_botao_materia_item) // 2

        self.y_inicio_area_scroll_botoes = self.altura_tela * 0.28
        self.altura_max_area_scroll_botoes = self.altura_tela * 0.65 
        self.rect_area_visivel_scroll = pygame.Rect(0, self.y_inicio_area_scroll_botoes, 
                                                self.largura_tela, self.altura_max_area_scroll_botoes)
        
        self._criar_botoes_para_materias()
        self.altura_total_conteudo_scrollavel = self._calcular_altura_total_conteudo()


    def _calcular_altura_total_conteudo(self):
        if not self.lista_botoes_materia: return 0
        num_botoes = len(self.lista_botoes_materia)
        return num_botoes * self.altura_botao_materia_item + (num_botoes - 1) * self.espaco_vertical_entre_botoes if num_botoes > 0 else 0

    def _criar_botoes_para_materias(self):
        self.lista_botoes_materia = []
        fonte_botao_item = self.interface_grafica.get_fonte_ui('media')
        y_relativo_dentro_scroll = 0

        for nome_materia in self.lista_materias_disponiveis:
            botao_item = Botao(
                self.pos_x_botoes_materia, y_relativo_dentro_scroll, 
                self.largura_botao_materia_item, self.altura_botao_materia_item,
                Tema.CORES['botao_normal'], Tema.CORES['botao_hover'], Tema.CORES['borda_botao'],
                nome_materia, fonte_botao_item, Tema.CORES['texto_botao'], 10,
                acao=lambda mat=nome_materia: self.gerenciador_jogo.iniciar_rodada_materia(mat)
            )
            self.lista_botoes_materia.append(botao_item)
            y_relativo_dentro_scroll += self.altura_botao_materia_item + self.espaco_vertical_entre_botoes
        
        self.altura_total_conteudo_scrollavel = y_relativo_dentro_scroll - self.espaco_vertical_entre_botoes if self.lista_botoes_materia else 0

    def desenhar_tela(self, tela_principal_jogo):
        if self.interface_grafica.imagem_fundo:
            tela_principal_jogo.blit(self.interface_grafica.imagem_fundo, (0,0))
        else:
            tela_principal_jogo.fill(Tema.CORES['fundo_padrao'])

        fonte_titulo_principal_jogo = self.interface_grafica.get_fonte_ui('titulo')
        fonte_subtitulo_instrucao = self.interface_grafica.get_fonte_ui('extra_grande')
        cor_texto_titulos = Tema.CORES['texto_principal'] 

        surface_titulo_jogo = fonte_titulo_principal_jogo.render("JOGO DO MILHÃO", True, cor_texto_titulos)
        tela_principal_jogo.blit(surface_titulo_jogo, ((self.largura_tela - surface_titulo_jogo.get_width()) // 2, self.altura_tela * 0.05))

        surface_subtitulo_instrucao = fonte_subtitulo_instrucao.render("Escolha uma Matéria:", True, cor_texto_titulos)
        tela_principal_jogo.blit(surface_subtitulo_instrucao, ((self.largura_tela - surface_subtitulo_instrucao.get_width()) // 2, self.altura_tela * 0.17))

        if self.lista_botoes_materia:
            tela_principal_jogo.set_clip(self.rect_area_visivel_scroll) 

            for botao_materia_item in self.lista_botoes_materia:
                y_botao_render_tela = self.rect_area_visivel_scroll.top + botao_materia_item.rect.y - self.offset_scroll_conteudo_y
                
                if y_botao_render_tela + botao_materia_item.rect.height > self.rect_area_visivel_scroll.top and \
                   y_botao_render_tela < self.rect_area_visivel_scroll.bottom:
                    botao_materia_item.desenhar(tela_principal_jogo, y_offset_absoluto_tela=y_botao_render_tela)
            
            tela_principal_jogo.set_clip(None) 

            if self.altura_total_conteudo_scrollavel > self.rect_area_visivel_scroll.height:
                altura_barra_scroll_desenho = max(20, int(self.rect_area_visivel_scroll.height * (self.rect_area_visivel_scroll.height / self.altura_total_conteudo_scrollavel)))
                offset_maximo_scroll = self.altura_total_conteudo_scrollavel - self.rect_area_visivel_scroll.height
                razao_scroll = self.offset_scroll_conteudo_y / offset_maximo_scroll if offset_maximo_scroll > 0 else 0
                y_pos_barra_scroll_desenho = self.rect_area_visivel_scroll.top + int(razao_scroll * (self.rect_area_visivel_scroll.height - altura_barra_scroll_desenho))
                largura_total_barra_scroll = 12
                x_pos_barra_scroll_desenho = self.largura_tela - largura_total_barra_scroll - 10 
                pygame.draw.rect(tela_principal_jogo, Tema.CORES['scroll_trilha'], 
                                (x_pos_barra_scroll_desenho, self.rect_area_visivel_scroll.top, largura_total_barra_scroll, self.rect_area_visivel_scroll.height), 0, border_radius=6)
                pygame.draw.rect(tela_principal_jogo, Tema.CORES['scroll_bar'], 
                                (x_pos_barra_scroll_desenho + 1, y_pos_barra_scroll_desenho + 1, largura_total_barra_scroll - 2, altura_barra_scroll_desenho - 2), 0, border_radius=5)
        
        elif not self.banco_perguntas.conexao or not self.banco_perguntas.conexao.is_connected():
            if not (self.interface_grafica.notificacao_ativa and "Falha ao conectar" in self.interface_grafica.notificacao_texto):
                fonte_aviso_conexao = self.interface_grafica.get_fonte_ui('grande')
                surface_aviso_conexao = fonte_aviso_conexao.render("Tentando conectar ao banco...", True, Tema.CORES['texto_principal'])
                tela_principal_jogo.blit(surface_aviso_conexao, ((self.largura_tela - surface_aviso_conexao.get_width()) // 2, self.altura_tela // 2))

    def atualizar_hover_botoes(self, pos_mouse_atual):
        if not self.rect_area_visivel_scroll.collidepoint(pos_mouse_atual):
            for botao_materia_item in self.lista_botoes_materia: botao_materia_item.mouse_sobre = False
            return

        for botao_materia_item in self.lista_botoes_materia:
            y_botao_render_tela = self.rect_area_visivel_scroll.top + botao_materia_item.rect.y - self.offset_scroll_conteudo_y
            botao_materia_item.verificar_hover(pos_mouse_atual, y_offset_absoluto_tela=y_botao_render_tela)

    def processar_clique(self, pos_clique_mouse):
        if not self.rect_area_visivel_scroll.collidepoint(pos_clique_mouse): return None

        for botao_materia_item in self.lista_botoes_materia:
            y_botao_render_tela = self.rect_area_visivel_scroll.top + botao_materia_item.rect.y - self.offset_scroll_conteudo_y
            rect_botao_desenhado_na_tela = pygame.Rect(botao_materia_item.rect.x, y_botao_render_tela, 
                                                    botao_materia_item.rect.width, botao_materia_item.rect.height)
            if rect_botao_desenhado_na_tela.collidepoint(pos_clique_mouse):
                if botao_materia_item.tratar_clique(): 
                    return botao_materia_item.texto 
        return None

    def tratar_evento_scroll(self, evento_pygame_mouse):
        if self.altura_total_conteudo_scrollavel <= self.rect_area_visivel_scroll.height:
            self.offset_scroll_conteudo_y = 0
            return
        offset_maximo_scroll = self.altura_total_conteudo_scrollavel - self.rect_area_visivel_scroll.height
        incremento_scroll = self.altura_botao_materia_item + self.espaco_vertical_entre_botoes 
        pos_mouse_atual = pygame.mouse.get_pos()
        if not self.rect_area_visivel_scroll.collidepoint(pos_mouse_atual): return
        if evento_pygame_mouse.button == 4: 
            self.offset_scroll_conteudo_y = max(0, self.offset_scroll_conteudo_y - incremento_scroll)
        elif evento_pygame_mouse.button == 5: 
            self.offset_scroll_conteudo_y = min(offset_maximo_scroll, self.offset_scroll_conteudo_y + incremento_scroll)