import pygame
from tema import TemaTela
from botao import BotaoTela # Importar BotaoTela para criar os botões aqui
import os

class GerenciadorInterfaceTela:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fundo = None
        self.carregar_fundo()
        self.atualizar_tema()

    def carregar_fundo(self):
        try:
            caminho_fundo = os.path.join(os.path.dirname(__file__), 'estrela.jpg')
            self.fundo = pygame.image.load(caminho_fundo)
            self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))
        except pygame.error:
            print("Erro ao carregar imagem de fundo. Usando cor sólida.")
            self.fundo = None
        except Exception as e:
            print(f"Erro inesperado ao carregar fundo: {e}")
            self.fundo = None

    def atualizar_tema(self):
        self.fonte_pequena = TemaTela.criar_fonte(TemaTela.FONTES['pequena'], self.altura)
        self.fonte_media = TemaTela.criar_fonte(TemaTela.FONTES['media'], self.altura)
        self.fonte_grande = TemaTela.criar_fonte(TemaTela.FONTES['grande'], self.altura)
        self.fonte_extra_grande = TemaTela.criar_fonte(TemaTela.FONTES['extra_grande'], self.altura)
        
        self.criar_botoes()

    def criar_botoes(self):
        margem_lateral = 50
        margem_superior = int(self.altura * 0.22)
        largura_botao = self.largura - 2 * margem_lateral
        altura_botao = int(self.altura * 0.08)
        espaco_vertical = int(self.altura * 0.02)

        self.botoes_resposta = []
        for i in range(4):
            y = margem_superior + i * (altura_botao + espaco_vertical)
            self.botoes_resposta.append(
                BotaoTela(margem_lateral, y, largura_botao, altura_botao,
                     TemaTela.CORES['botao_normal'], TemaTela.CORES['borda'], "", 
                     self.fonte_media, TemaTela.CORES['texto'], 15))

        largura_botao_acao = (self.largura - 2 * margem_lateral - 40) // 3
        
        # Os botões de ação são criados uma vez com suas cores padrão
        self.botao_dica = BotaoTela(
            margem_lateral, self.altura - altura_botao - 40, 
            largura_botao_acao, altura_botao,
            TemaTela.CORES['botao_dica'], TemaTela.CORES['borda'], "Dica", 
            self.fonte_media, TemaTela.CORES['texto'], 15)
        
        self.botao_eliminar = BotaoTela(
            margem_lateral + largura_botao_acao + 20, self.altura - altura_botao - 40,
            largura_botao_acao, altura_botao,
            TemaTela.CORES['botao_eliminar'], TemaTela.CORES['borda'], "Eliminar 2 opções", 
            self.fonte_media, TemaTela.CORES['texto_claro'], 15)
        
        self.botao_pular = BotaoTela(
            margem_lateral + 2*(largura_botao_acao + 20), self.altura - altura_botao - 40,
            largura_botao_acao, altura_botao,
            TemaTela.CORES['botao_pular'], TemaTela.CORES['borda'], "Pular Pergunta", 
            self.fonte_media, TemaTela.CORES['texto'], 15)

        # Garante que os botões de confirmação tenham suas cores corretas
        self.botao_confirmar = BotaoTela(
            0, 0, 0, 0, # Posição e tamanho são definidos em desenhar_confirmacao
            TemaTela.CORES['botao_confirmar'], TemaTela.CORES['borda'], "Sim", 
            self.fonte_media, TemaTela.CORES['texto'], 10)
        
        self.botao_cancelar = BotaoTela(
            0, 0, 0, 0, # Posição e tamanho são definidos em desenhar_confirmacao
            TemaTela.CORES['botao_cancelar'], TemaTela.CORES['borda'], "Não", 
            self.fonte_media, TemaTela.CORES['texto'], 10)

        self.botao_jogar_novamente = BotaoTela(
            0, 0, 250, 60, 
            TemaTela.CORES['botao_reiniciar'], TemaTela.CORES['borda'], "Jogar de Novo", 
            self.fonte_media, TemaTela.CORES['texto_claro'], 15)
        
        self.botao_sair = BotaoTela(
            0, 0, 250, 60, 
            TemaTela.CORES['botao_sair'], TemaTela.CORES['borda'], "Sair", 
            self.fonte_media, TemaTela.CORES['texto_claro'], 15)

    def desenhar_botoes_resposta(self, tela, pergunta, respostas_eliminadas):
        for i, botao in enumerate(self.botoes_resposta):
            # Restaura a cor padrão antes de desenhar, caso tenha sido mudada por alguma flag anterior
            botao.cor_fundo = TemaTela.CORES['botao_normal'] 
            botao.cor_texto = TemaTela.CORES['texto'] # Garante a cor do texto padrão

            botao.texto = f"{chr(65 + i)}) {pergunta.alternativas[i]}"
            
            if i in respostas_eliminadas:
                # Se eliminada, altera a cor e texto para cinza
                botao.cor_fundo = TemaTela.CORES['resposta_eliminada']
                botao.cor_texto = (150, 150, 150) # Cor de texto cinza para eliminadas
            
            botao.desenhar(tela)
            
            # Desenha a camada de opacidade e borda para respostas eliminadas
            if i in respostas_eliminadas:
                s = pygame.Surface((botao.rect.width, botao.rect.height), pygame.SRCALPHA)
                # s.fill(TemaTela.CORES['resposta_eliminada']) # Isso já é feito na cor_fundo agora
                tela.blit(s, botao.rect.topleft) # Blita uma surface transparente para manter o efeito
                pygame.draw.rect(tela, TemaTela.CORES['borda'], botao.rect, 2, border_radius=15)
                # O texto já está cinza devido à mudança de botao.cor_texto

    # Adicionada a flag 'dica_usada', 'pulo_usado', 'eliminacao_usada' para controlar a cor
    def desenhar_botoes_acao(self, tela, pulo_usado, eliminacao_usada, dica_usada):
        # AQUI É ONDE AJUSTAMOS AS CORES DOS BOTÕES DE AÇÃO
        self.botao_dica.cor_fundo = TemaTela.CORES['botao_desabilitado'] if dica_usada else TemaTela.CORES['botao_dica']
        self.botao_dica.desenhar(tela)
        
        self.botao_pular.cor_fundo = TemaTela.CORES['botao_desabilitado'] if pulo_usado else TemaTela.CORES['botao_pular']
        self.botao_pular.desenhar(tela)
        
        self.botao_eliminar.cor_fundo = TemaTela.CORES['botao_desabilitado'] if eliminacao_usada else TemaTela.CORES['botao_eliminar']
        self.botao_eliminar.desenhar(tela)

    def desenhar_pergunta(self, tela, texto_pergunta):
        texto_render = self.fonte_grande.render(texto_pergunta, True, TemaTela.CORES['texto'])
        
        padding_x = 30
        padding_y = 20
        
        retangulo_texto = texto_render.get_rect(topleft=(50, 50))
        retangulo_caixa = retangulo_texto.inflate(padding_x * 2, padding_y * 2) 
        
        pygame.draw.rect(tela, TemaTela.CORES['caixa_pergunta'], retangulo_caixa, border_radius=10)
        pygame.draw.rect(tela, TemaTela.CORES['borda'], retangulo_caixa, 2, border_radius=10)
        tela.blit(texto_render, (retangulo_caixa.x + padding_x, retangulo_caixa.y + padding_y))


    def desenhar_dica(self, tela, texto_dica):
        fonte_dica = self.fonte_pequena
        dica_texto_surface = fonte_dica.render(texto_dica, True, TemaTela.CORES['texto'])

        padding_x = 10
        padding_y = 5

        # Posição do balão da dica acima do botão de dica
        x_dica = self.botao_dica.rect.x
        y_dica = self.botao_dica.rect.y - (dica_texto_surface.get_height() + 2 * padding_y) - 5

        largura_balao = dica_texto_surface.get_width() + 2 * padding_x
        altura_balao = dica_texto_surface.get_height() + 2 * padding_y

        dica_rect = pygame.Rect(x_dica, y_dica, largura_balao, altura_balao)

        pygame.draw.rect(tela, (255, 255, 255), dica_rect, border_radius=10)
        pygame.draw.rect(tela, TemaTela.CORES['borda'], dica_rect, 2, border_radius=10)

        tela.blit(dica_texto_surface, (dica_rect.x + padding_x, dica_rect.y + padding_y))

    def desenhar_confirmacao(self, tela):
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        tela.blit(overlay, (0, 0))

        largura_caixa = 400
        altura_caixa = 180
        x = (self.largura - largura_caixa) // 2
        y = (self.altura - altura_caixa) // 2

        caixa = pygame.Rect(x, y, largura_caixa, altura_caixa)
        pygame.draw.rect(tela, (255, 255, 255), caixa, border_radius=15)
        pygame.draw.rect(tela, TemaTela.CORES['borda'], caixa, 3, border_radius=15)

        texto = self.fonte_media.render("Confirmar resposta?", True, TemaTela.CORES['texto'])
        tela.blit(texto, (x + (largura_caixa - texto.get_width()) // 2, y + 20))

        largura_botao = 120
        altura_botao = 50
        espacamento = 40
        bx = x + (largura_caixa - 2 * largura_botao - espacamento) // 2
        by = y + 80

        # Define a posição e o tamanho dos botões de confirmação aqui
        self.botao_confirmar.rect = pygame.Rect(bx, by, largura_botao, altura_botao)
        self.botao_cancelar.rect = pygame.Rect(bx + largura_botao + espacamento, by, largura_botao, altura_botao)
        
        self.botao_confirmar.desenhar(tela)
        self.botao_cancelar.desenhar(tela)

    def desenhar_tela_fim(self, tela, pontuacao, resposta_correta=None):
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))

        mensagem1 = self.fonte_extra_grande.render("Fim de jogo!", True, TemaTela.CORES['texto'])
        mensagem2 = self.fonte_extra_grande.render(f"Pontuação final: R${pontuacao}", True, TemaTela.CORES['pontuacao'])
        
        mensagem3 = None
        if resposta_correta:
            mensagem3 = self.fonte_media.render(f"Resposta correta: {resposta_correta}", True, TemaTela.CORES['resposta_certa'])

        text_surfaces = [mensagem1, mensagem2]
        if mensagem3:
            text_surfaces.append(mensagem3)
        
        max_text_width = max(s.get_width() for s in text_surfaces)
        
        largura_ret = max(max_text_width, self.botao_jogar_novamente.rect.width) + 40 

        padding = 20
        espacamento_textos = 10
        espacamento_botoes = 10
        
        altura_textos = sum(s.get_height() for s in text_surfaces) + espacamento_textos * (len(text_surfaces) - 1)
        
        altura_botoes_total = self.botao_jogar_novamente.rect.height + self.botao_sair.rect.height + espacamento_botoes

        altura_ret = altura_textos + altura_botoes_total + 2 * padding + espacamento_textos

        x_ret = (self.largura - largura_ret) // 2
        y_ret = (self.altura - altura_ret) // 2

        retangulo = pygame.Rect(x_ret, y_ret, largura_ret, altura_ret)
        pygame.draw.rect(tela, (255, 255, 255), retangulo, border_radius=15)
        pygame.draw.rect(tela, TemaTela.CORES['borda'], retangulo, 3, border_radius=15)

        y_offset = y_ret + padding
        for msg_surface in text_surfaces:
            tela.blit(msg_surface, (x_ret + (largura_ret - msg_surface.get_width()) // 2, y_offset))
            y_offset += msg_surface.get_height() + espacamento_textos

        bx = x_ret + (largura_ret - self.botao_jogar_novamente.rect.width) // 2
        by = y_offset + espacamento_textos

        self.botao_jogar_novamente.rect.topleft = (bx, by)
        self.botao_jogar_novamente.desenhar(tela)

        bsx = bx
        bsy = by + self.botao_jogar_novamente.rect.height + espacamento_botoes
        self.botao_sair.rect.topleft = (bsx, bsy)
        self.botao_sair.desenhar(tela)