import pygame

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Cadastro de Matérias")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
cinza_claro = (200, 200, 200)
verde = (0, 128, 0)  # Cor para o botão
verde_escuro = (0, 100, 0)  # Cor para o botão ao ser clicado

# Fontes
fonte_padrao = pygame.font.Font(None, 24)
fonte_mensagem = pygame.font.Font(None, 30)  # Fonte para a mensagem de sucesso

# Classe InputBox
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = cinza_claro
        self.text = text
        self.txt_surface = fonte_padrao.render(text, True, preto)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = branco if self.active else cinza_claro
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Você pode remover isso ou usar para debug
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = fonte_padrao.render(self.text, True, preto)

    def draw(self, tela):
        tela.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(tela, self.color, self.rect, 2)

# Função para desenhar botões
def desenhar_botao(tela, cor, x, y, largura, altura, texto, fonte, cor_texto):
    pygame.draw.rect(tela, cor, (x, y, largura, altura))
    texto_surface = fonte.render(texto, True, cor_texto)
    texto_rect = texto_surface.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(texto_surface, texto_rect)

# Criação dos elementos da interface
nome_materia_input = InputBox(150, 100, 200, 32)
codigo_materia_input = InputBox(150, 150, 200, 32)

botao_cadastrar_x = 150
botao_cadastrar_y = 250
botao_cadastrar_largura = 100
botao_cadastrar_altura = 30

# Variável para controlar a exibição da mensagem de sucesso
mensagem_sucesso = ""
mensagem_tempo = 0  
mensagem_duracao = 720  

# Loop principal do jogo
def main():
    global mensagem_sucesso, mensagem_tempo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            nome_materia_input.handle_event(event)
            codigo_materia_input.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_cadastrar_x <= event.pos[0] <= botao_cadastrar_x + botao_cadastrar_largura and \
                   botao_cadastrar_y <= event.pos[1] <= botao_cadastrar_y + botao_cadastrar_altura:
                    # Lógica de cadastro (substitua com sua lógica)
                    materia = nome_materia_input.text
                    codigo = codigo_materia_input.text
                    print(f"Matéria: {materia}, Código: {codigo}")  # Imprime no console

                    # Define a mensagem de sucesso
                    mensagem_sucesso = "Cadastro realizado com sucesso!"
                    mensagem_tempo = mensagem_duracao

                    # Limpa os campos
                    nome_materia_input.text = ''
                    codigo_materia_input.text = ''

        # Desenho na tela
        tela.fill(branco)

        # Desenho dos elementos da interface
        nome_materia_label = fonte_padrao.render("Nome:", True, preto)
        tela.blit(nome_materia_label, (50, 105))
        nome_materia_input.draw(tela)

        codigo_materia_label = fonte_padrao.render("Código:", True, preto)
        tela.blit(codigo_materia_label, (50, 155))
        codigo_materia_input.draw(tela)

        desenhar_botao(tela, verde, botao_cadastrar_x, botao_cadastrar_y, botao_cadastrar_largura, botao_cadastrar_altura, "Cadastrar", fonte_padrao, branco)

        # Exibe a mensagem de sucesso
        if mensagem_tempo > 0:
            mensagem_surface = fonte_mensagem.render(mensagem_sucesso, True, verde_escuro)
            mensagem_rect = mensagem_surface.get_rect(center=(largura // 2, 50))
            tela.blit(mensagem_surface, mensagem_rect)
            mensagem_tempo -= 1  # Decrementa o contador

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
