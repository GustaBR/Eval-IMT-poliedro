import pygame
from cadastrar_materias.input_box import InputBox
from cadastrar_materias.database import Database
import config
from botao_menu import BotaoMenu

# Cores
AZUL_CLARO = (30, 144, 255)
DOURADO = (218, 165, 32)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_ESCURO = (169, 169, 169)
VERDE = (34, 139, 34)
VERMELHO = (220, 20, 60)

# Fontes
pygame.init()
FONT = pygame.font.Font(None, 32)
FONT_SMALL = pygame.font.Font(None, 24)

class CadastrarMateriasTela:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        
        self.input_box = InputBox(0, 0, 300, 40, FONT)
        self.button_rect = pygame.Rect(0, 0, 130, 40)

        self.message = ''
        self.message_color = DOURADO

        self.materias = []
        self.materia_selecionada = None

        self.scroll_offset = 0
        self.scroll_speed = 20
        self.max_scroll = 0

        self.confirm_excluir = False
        self.materia_para_excluir = None

        self.clock = pygame.time.Clock()

        self.bg_image = pygame.image.load("cadastrar_materias/fundo.jpg").convert()

        self.atualizar_lista_materias()
        self.atualizar_layout()

    def atualizar_layout(self):
        self.input_box.rect.topleft = (config.LARGURA_JANELA * 0.25, config.ALTURA_JANELA * 0.375)
        self.input_box.rect.width = config.LARGURA_JANELA * 0.5
        self.input_box.rect.height = 40

        self.button_rect.topleft = (self.input_box.rect.left, self.input_box.rect.bottom + 10)
        self.button_rect.width = 130
        self.button_rect.height = 40

    def atualizar_lista_materias(self):
        materias, erro = Database.buscar_materias()
        if erro:
            self.message = erro
            self.message_color = VERMELHO
            self.materias = []
        else:
            self.materias = materias
            self.message = ''
        self.max_scroll = max(0, len(self.materias) * 25 - int(config.ALTURA_JANELA * 0.3))

    def desenhar_confirmacao(self, janela):
        overlay = pygame.Surface((config.LARGURA_JANELA, config.ALTURA_JANELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        janela.blit(overlay, (0,0))

        msg = f"Excluir matéria '{self.materia_para_excluir}'?"
        texto = FONT.render(msg, True, BRANCO)
        caixa = texto.get_rect(center=(config.LARGURA_JANELA // 2, config.ALTURA_JANELA // 2 - 20))
        janela.blit(texto, caixa)

        self.botao_sim = pygame.Rect(config.LARGURA_JANELA // 2 - 80, config.ALTURA_JANELA // 2 + 20, 70, 40)
        btn_nao = pygame.Rect(config.LARGURA_JANELA // 2 + 10, config.ALTURA_JANELA // 2 + 20, 70, 40)
        pygame.draw.rect(janela, VERDE, self.botao_sim)
        pygame.draw.rect(janela, VERMELHO, btn_nao)

        sim_text = FONT_SMALL.render("Sim", True, BRANCO)
        nao_text = FONT_SMALL.render("Não", True, BRANCO)
        janela.blit(sim_text, sim_text.get_rect(center=self.botao_sim.center))
        janela.blit(nao_text, nao_text.get_rect(center=btn_nao.center))

        return self.botao_sim, btn_nao

    def checar_eventos(self, evento):
        if evento.type == pygame.VIDEORESIZE:
            config.LARGURA_JANELA, config.ALTURA_JANELA = evento.w, evento.h
            self.bg_image = pygame.transform.scale(pygame.image.load("cadastrar_materias/fundo.jpg").convert(), (config.LARGURA_JANELA, config.ALTURA_JANELA))
            self.atualizar_layout()
            self.atualizar_lista_materias()
        elif evento.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= evento.y * self.scroll_speed
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if self.confirm_excluir:
                if self.botao_sim.collidepoint(evento.pos):
                    sucesso, msg = Database.excluir_materia(self.materia_para_excluir)
                    self.message = msg
                    self.message_color = DOURADO if sucesso else VERMELHO
                    if sucesso:
                        self.materia_selecionada = None
                        self.input_box.clear_text()
                        self.atualizar_lista_materias()
                    self.confirm_excluir = False
                    self.materia_para_excluir = None
                elif self.botao_nao.collidepoint(evento.pos):
                    self.confirm_excluir = False
                    self.materia_para_excluir = None
                return
            if evento.button == 1:
                lista_y = int(config.ALTURA_JANELA * 0.55 + 40) - self.scroll_offset
                for i, materia in enumerate(self.materias):
                    y = lista_y + i * 25
                    item_rect = pygame.Rect(config.LARGURA_JANELA * 0.1, y, config.LARGURA_JANELA * 0.8, 25)
                    if item_rect.collidepoint(evento.pos):
                        self.materia_selecionada = materia
                        self.input_box.set_text(materia)
                        break
            elif evento.button == 3:
                lista_y = int(config.ALTURA_JANELA * 0.55 + 40) - self.scroll_offset
                for i, materia in enumerate(self.materias):
                    y = lista_y + i * 25
                    item_rect = pygame.Rect(config.LARGURA_JANELA * 0.1, y, config.LARGURA_JANELA * 0.8, 25)
                    if item_rect.collidepoint(evento.pos):
                        self.materia_para_excluir = materia
                        self.confirm_excluir = True
                        break

        self.input_box.handle_event(evento)

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.button_rect.collidepoint(evento.pos):
                nome = self.input_box.get_text()
                if nome:
                    sucesso, msg = Database.inserir_materia(nome)
                    self.message = msg
                    self.message_color = DOURADO if sucesso else VERMELHO
                    if sucesso:
                        self.input_box.clear_text()
                        self.atualizar_lista_materias()
                else:
                    self.message = "Digite o nome da matéria antes de cadastrar."
                    self.message_color = VERMELHO

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN and self.input_box.active:
            nome = self.input_box.get_text()
            if nome:
                sucesso, msg = Database.inserir_materia(nome)
                self.message = msg
                self.message_color = DOURADO if sucesso else VERMELHO
                if sucesso:
                    self.input_box.clear_text()
                    self.atualizar_lista_materias()
            else:
                self.message = "Digite o nome da matéria antes de cadastrar."
                self.message_color = VERMELHO

    def atualizar(self):
        ...
        # Definir atualizações nos cálculos de redimensionamento de tela

    
    def exibir(self, janela):
        #self.bg_image = pygame.transform.scale(self.bg_image, (config.LARGURA_JANELA, config.ALTURA_JANELA))
        #janela.blit(self.bg_image, (0, 0))
        janela.fill(config.BRANCO)

        instr_text = FONT_SMALL.render("Digite o nome da matéria:", True, PRETO)
        janela.blit(instr_text, (self.input_box.rect.left, self.input_box.rect.top - 25))
        self.input_box.draw(janela)

        pygame.draw.rect(janela, VERDE, self.button_rect)
        btn_text = FONT.render("Cadastrar", True, BRANCO)
        janela.blit(btn_text, (self.button_rect.x + 15, self.button_rect.y + 5))

        lista_y = int(config.ALTURA_JANELA * 0.55 + 40) - self.scroll_offset
        for i, materia in enumerate(self.materias):
            y = lista_y + i * 25
            item_rect = pygame.Rect(config.LARGURA_JANELA * 0.1, y, config.LARGURA_JANELA * 0.8, 25)
            cor_fundo = (220, 220, 220) if materia == self.materia_selecionada else BRANCO
            pygame.draw.rect(janela, cor_fundo, item_rect)
            txt = FONT_SMALL.render(materia, True, PRETO)
            janela.blit(txt, (item_rect.x + 5, item_rect.y + 5))

        if self.message:
            msg_surface = FONT_SMALL.render(self.message, True, self.message_color)
            janela.blit(msg_surface, (self.input_box.rect.left, self.input_box.rect.bottom + 60))

        if self.confirm_excluir:
            self.botao_sim, self.botao_nao = self.desenhar_confirmacao(janela)