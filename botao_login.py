import pygame

class BotaoLogin:
    def __init__(self, rel_rect, texto, acao_clicar=None, ativo=True):
        self.rel_rect = rel_rect  # Retângulo relativo
        self.texto = texto
        self.acao_click = acao_clicar
        self.ativo = ativo
        self.hovered = False

        # Cores do botão para cada estado
        self.cores = {
            "normal": (0, 102, 204),
            "hover": (0, 80, 160),
            "inativo": (180, 180, 180)
        }

        self.rect = pygame.Rect(0, 0, 0, 0)

        # Fonte para o texto do botão (ajusta automaticamente na altura do botão)
        self.fonte = pygame.font.Font(None, 24)

    """def atualizar_rect(self, janela):
        largura, altura = self.janela.get_size()
        x = int(self.rel_rect[0] * largura)
        y = int(self.rel_rect[1] * altura)
        w = int(self.rel_rect[2] * largura)
        h = int(self.rel_rect[3] * altura)
        self.rect = pygame.Rect(x, y, w, h)

        # Atualiza o tamanho da fonte para se ajustar à altura do botão
        tamanho_fonte = max(int(h * 0.5), 12)
        self.fonte = pygame.font.Font(None, tamanho_fonte)"""

    def definir_ativo(self, estado: bool):
        self.ativo = estado

    def checar_eventos(self, evento):
        if not self.ativo:
            return False

        if evento.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(evento.pos)

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.rect.collidepoint(evento.pos):
                # Opcional: chamar callback, se existir
                if self.acao_clicar:
                    self.acao_clicar()
                return True

    def atualizar(self):
        # Atualiza posição e tamanho do botão no resize da tela
        #self.update_rect()
        ...

    def exibir(self, janela):
        # Escolhe a cor de acordo com o estado do botão
        if not self.ativo:
            self.cor = self.cores["inativo"]
        else:
            self.cor = self.cores["hover"] if self.hovered else self.cores["normal"]

        # Desenha o retângulo arredondado
        pygame.draw.rect(janela, self.cor, self.rect, border_radius=12)

        # Renderiza o texto branco no centro do botão
        texto_surf = self.fonte.render(self.texto, True, (255, 255, 255))
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        janela.blit(texto_surf, texto_rect)