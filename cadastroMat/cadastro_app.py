import pygame
import sys
from input_box import InputBox
from database import Database

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

class CadastroMateriasApp:
    def __init__(self):
        self.width = 600
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Cadastro de Matérias")

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

        self.bg_image = pygame.image.load("fundo.jpg").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))

        self.atualizar_lista_materias()
        self.atualizar_layout()

    def atualizar_layout(self):
        self.input_box.rect.topleft = (self.width * 0.25, self.height * 0.375)
        self.input_box.rect.width = self.width * 0.5
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
        self.max_scroll = max(0, len(self.materias) * 25 - int(self.height * 0.3))

    def desenhar_confirmacao(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0,0))

        msg = f"Excluir matéria '{self.materia_para_excluir}'?"
        texto = FONT.render(msg, True, BRANCO)
        caixa = texto.get_rect(center=(self.width // 2, self.height // 2 - 20))
        self.screen.blit(texto, caixa)

        btn_sim = pygame.Rect(self.width // 2 - 80, self.height // 2 + 20, 70, 40)
        btn_nao = pygame.Rect(self.width // 2 + 10, self.height // 2 + 20, 70, 40)
        pygame.draw.rect(self.screen, VERDE, btn_sim)
        pygame.draw.rect(self.screen, VERMELHO, btn_nao)

        sim_text = FONT_SMALL.render("Sim", True, BRANCO)
        nao_text = FONT_SMALL.render("Não", True, BRANCO)
        self.screen.blit(sim_text, sim_text.get_rect(center=btn_sim.center))
        self.screen.blit(nao_text, nao_text.get_rect(center=btn_nao.center))

        return btn_sim, btn_nao

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.w, event.h
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                    self.bg_image = pygame.transform.scale(pygame.image.load("fundo.jpg").convert(), (self.width, self.height))
                    self.atualizar_layout()
                    self.atualizar_lista_materias()
                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll_offset -= event.y * self.scroll_speed
                    self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.confirm_excluir:
                        btn_sim, btn_nao = self.desenhar_confirmacao()
                        if btn_sim.collidepoint(event.pos):
                            sucesso, msg = Database.excluir_materia(self.materia_para_excluir)
                            self.message = msg
                            self.message_color = DOURADO if sucesso else VERMELHO
                            if sucesso:
                                self.materia_selecionada = None
                                self.input_box.clear_text()
                                self.atualizar_lista_materias()
                            self.confirm_excluir = False
                            self.materia_para_excluir = None
                        elif btn_nao.collidepoint(event.pos):
                            self.confirm_excluir = False
                            self.materia_para_excluir = None
                        continue
                    if event.button == 1:
                        lista_y = int(self.height * 0.55 + 40) - self.scroll_offset
                        for i, materia in enumerate(self.materias):
                            y = lista_y + i * 25
                            item_rect = pygame.Rect(self.width * 0.1, y, self.width * 0.8, 25)
                            if item_rect.collidepoint(event.pos):
                                self.materia_selecionada = materia
                                self.input_box.set_text(materia)
                                break
                    elif event.button == 3:
                        lista_y = int(self.height * 0.55 + 40) - self.scroll_offset
                        for i, materia in enumerate(self.materias):
                            y = lista_y + i * 25
                            item_rect = pygame.Rect(self.width * 0.1, y, self.width * 0.8, 25)
                            if item_rect.collidepoint(event.pos):
                                self.materia_para_excluir = materia
                                self.confirm_excluir = True
                                break

                self.input_box.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
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

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.input_box.active:
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

            self.screen.blit(self.bg_image, (0, 0))

            instr_text = FONT_SMALL.render("Digite o nome da matéria:", True, PRETO)
            self.screen.blit(instr_text, (self.input_box.rect.left, self.input_box.rect.top - 25))
            self.input_box.draw(self.screen)

            pygame.draw.rect(self.screen, VERDE, self.button_rect)
            btn_text = FONT.render("Cadastrar", True, BRANCO)
            self.screen.blit(btn_text, (self.button_rect.x + 15, self.button_rect.y + 5))

            lista_y = int(self.height * 0.55 + 40) - self.scroll_offset
            for i, materia in enumerate(self.materias):
                y = lista_y + i * 25
                item_rect = pygame.Rect(self.width * 0.1, y, self.width * 0.8, 25)
                cor_fundo = (220, 220, 220) if materia == self.materia_selecionada else BRANCO
                pygame.draw.rect(self.screen, cor_fundo, item_rect)
                txt = FONT_SMALL.render(materia, True, PRETO)
                self.screen.blit(txt, (item_rect.x + 5, item_rect.y + 5))

            if self.message:
                msg_surface = FONT_SMALL.render(self.message, True, self.message_color)
                self.screen.blit(msg_surface, (self.input_box.rect.left, self.input_box.rect.bottom + 60))

            if self.confirm_excluir:
                self.desenhar_confirmacao()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = CadastroMateriasApp()
    app.run()
