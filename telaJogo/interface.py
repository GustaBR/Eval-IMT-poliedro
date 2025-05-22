import pygame
from tema import TemaTela
from botao import BotaoTela
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
            caminho_fundo = os.path.join(os.path.dirname(__file__), 'estrela.jpg') # imagem de fundo
            imagem = pygame.image.load(caminho_fundo)
            self.fundo = pygame.transform.scale(imagem, (self.largura, self.altura))
        except:
            print("Erro ao carregar imagem de fundo. Usando cor sólida.")
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
        
        self.botao_dica = BotaoTela(
            margem_lateral, self.altura - altura_botao - 40, 
            largura_botao_acao, altura_botao,
            TemaTela.CORES['botao_dica'], TemaTela.CORES['borda'], "Dica", #botao dica
            self.fonte_media, TemaTela.CORES['texto'], 15)
        
        self.botao_eliminar = BotaoTela(
            margem_lateral + largura_botao_acao + 20, self.altura - altura_botao - 40,
            largura_botao_acao, altura_botao,
            TemaTela.CORES['botao_eliminar'], TemaTela.CORES['borda'], "Eliminar 2 opções", #botao Eliminar 2 opções
            self.fonte_media, TemaTela.CORES['texto_claro'], 15)
        
        self.botao_pular = BotaoTela(
            margem_lateral + 2*(largura_botao_acao + 20), self.altura - altura_botao - 40,
            largura_botao_acao, altura_botao,
            TemaTela.CORES['botao_pular'], TemaTela.CORES['borda'], "Pular Pergunta", # botão de pular perguntar
            self.fonte_media, TemaTela.CORES['texto'], 15)

        # Botoes de confirmação
        self.botao_confirmar = BotaoTela(
            0, 0, 0, 0, 
            TemaTela.CORES['botao_confirmar'], TemaTela.CORES['borda'], "Sim", # confirmar: SIM
            self.fonte_media, TemaTela.CORES['texto'], 10)
        
        self.botao_cancelar = BotaoTela(
            0, 0, 0, 0, 
            TemaTela.CORES['botao_cancelar'], TemaTela.CORES['borda'], "Não", # confirmar: NÃO
            self.fonte_media, TemaTela.CORES['texto'], 10)

        # Botoes de fim de jogo
        self.botao_jogar_novamente = BotaoTela(
            0, 0, 200, 60, 
            TemaTela.CORES['botao_reiniciar'], TemaTela.CORES['borda'], "Jogar de Novo", #botao Jogar de Novo
            self.fonte_media, TemaTela.CORES['texto_claro'], 15)
        
        self.botao_sair = BotaoTela(
            0, 0, 200, 60, 
            TemaTela.CORES['botao_sair'], TemaTela.CORES['borda'], "Sair", # botao Sair
            self.fonte_media, TemaTela.CORES['texto_claro'], 15)

    def desenhar_botoes_resposta(self, tela, pergunta, respostas_eliminadas):
        for i, botao in enumerate(self.botoes_resposta):
            botao.texto = f"{chr(65 + i)}) {pergunta.alternativas[i]}"
            botao.desenhar(tela)
            
            if i in respostas_eliminadas:
                s = pygame.Surface((botao.rect.width, botao.rect.height), pygame.SRCALPHA)
                s.fill(TemaTela.CORES['resposta_eliminada'])
                tela.blit(s, botao.rect.topleft)
                pygame.draw.rect(tela, TemaTela.CORES['resposta_eliminada'], botao.rect, 2, border_radius=15)
                texto_render = botao.fonte.render(botao.texto, True, (150, 150, 150))
                tela.blit(texto_render, (botao.rect.x + 10, botao.rect.y + (botao.rect.height - texto_render.get_height()) // 2))

    def desenhar_botoes_acao(self, tela, pulo_usado, eliminacao_usada):
        self.botao_dica.desenhar(tela)
        
        cor_pular = (100, 100, 100) if pulo_usado else TemaTela.CORES['botao_pular']
        self.botao_pular.cor_fundo = cor_pular
        self.botao_pular.desenhar(tela)
        
        cor_eliminar = (100, 100, 100) if eliminacao_usada else TemaTela.CORES['botao_eliminar']
        self.botao_eliminar.cor_fundo = cor_eliminar
        self.botao_eliminar.desenhar(tela)

    def desenhar_pergunta(self, tela, texto_pergunta):
        texto_render = self.fonte_grande.render(texto_pergunta, True, TemaTela.CORES['texto'])
        retangulo_texto = texto_render.get_rect(topleft=(50, 50))
        retangulo_texto.inflate_ip(200, 10)
        
        pygame.draw.rect(tela, TemaTela.CORES['caixa_pergunta'], retangulo_texto, border_radius=10)
        pygame.draw.rect(tela, TemaTela.CORES['borda'], retangulo_texto, 2, border_radius=10)
        tela.blit(texto_render, (50, 50))

    def desenhar_dica(self, tela, texto_dica):
        fonte_dica = self.fonte_pequena
        dica_texto = fonte_dica.render(texto_dica, True, TemaTela.CORES['texto'])
        x_dica = self.botao_dica.rect.x + (self.botao_dica.rect.width - dica_texto.get_width()) // 2
        y_dica = self.botao_dica.rect.y - dica_texto.get_height() - 5
        
        dica_rect = pygame.Rect(x_dica - 10, y_dica - 5, dica_texto.get_width() + 20, dica_texto.get_height() + 10)
        pygame.draw.rect(tela, (255, 255, 255), dica_rect, border_radius=10)
        pygame.draw.rect(tela, TemaTela.CORES['borda'], dica_rect, 2, border_radius=10)
        tela.blit(dica_texto, (x_dica, y_dica))

    def desenhar_confirmacao(self, tela):
        # Criar uma superfície semi-transparente para o fundo da confirmação
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Preto semi-transparente
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

        self.botao_confirmar.rect = pygame.Rect(bx, by, largura_botao, altura_botao)
        self.botao_cancelar.rect = pygame.Rect(bx + largura_botao + espacamento, by, largura_botao, altura_botao)
        
        self.botao_confirmar.desenhar(tela)
        self.botao_cancelar.desenhar(tela)

    def desenhar_tela_fim(self, tela, pontuacao, resposta_correta=None):
        # Criar uma superfície semi-transparente para o fundo
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Preto semi-transparente
        tela.blit(overlay, (0, 0))

        mensagem1 = self.fonte_extra_grande.render("Fim de jogo!", True, TemaTela.CORES['texto'])
        mensagem2 = self.fonte_extra_grande.render(f"Pontuação final: R${pontuacao}", True, TemaTela.CORES['pontuacao'])
        
        # Criar mensagem de resposta correta se existir
        mensagem3 = None
        if resposta_correta:
            mensagem3 = self.fonte_media.render(f"Resposta correta: {resposta_correta}", True, TemaTela.CORES['resposta_certa'])

        # Calcular largura máxima necessária
        largura_max = max(
            mensagem1.get_width(),
            mensagem2.get_width(),
            mensagem3.get_width() if mensagem3 else 0,
            self.botao_jogar_novamente.rect.width
        )
        largura_ret = largura_max + 40  # Adicionar padding

        padding = 20
        espacamento_textos = 10
        espacamento_botoes = 10
        altura_botoes = self.botao_jogar_novamente.rect.height + self.botao_sair.rect.height + espacamento_botoes

        # Ajustar altura do retângulo para incluir a mensagem3 se existir
        altura_ret = (
            mensagem1.get_height() +
            espacamento_textos +
            mensagem2.get_height() +
            (espacamento_textos + mensagem3.get_height() if mensagem3 else 0) +
            espacamento_textos +
            altura_botoes +
            2 * padding
        )

        x_ret = (self.largura - largura_ret) // 2
        y_ret = (self.altura - altura_ret) // 2

        retangulo = pygame.Rect(x_ret, y_ret, largura_ret, altura_ret)
        pygame.draw.rect(tela, (255, 255, 255), retangulo, border_radius=15)
        pygame.draw.rect(tela, TemaTela.CORES['borda'], retangulo, 3, border_radius=15)

        y_texto = y_ret + padding
        tela.blit(mensagem1, (x_ret + (largura_ret - mensagem1.get_width()) // 2, y_texto))
        y_texto += mensagem1.get_height() + espacamento_textos
        tela.blit(mensagem2, (x_ret + (largura_ret - mensagem2.get_width()) // 2, y_texto))
        
        # Mostrar resposta correta se existir
        if mensagem3:
            y_texto += mensagem2.get_height() + espacamento_textos
            tela.blit(mensagem3, (x_ret + (largura_ret - mensagem3.get_width()) // 2, y_texto))

        bx = x_ret + (largura_ret - self.botao_jogar_novamente.rect.width) // 2
        by = y_texto + (mensagem3.get_height() if mensagem3 else mensagem2.get_height()) + espacamento_textos + 10

        self.botao_jogar_novamente.rect.topleft = (bx, by)
        self.botao_jogar_novamente.desenhar(tela)

        bsx = bx
        bsy = by + self.botao_jogar_novamente.rect.height + espacamento_botoes
        self.botao_sair.rect.topleft = (bsx, bsy)
        self.botao_sair.desenhar(tela)