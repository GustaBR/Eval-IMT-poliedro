import pygame
from config import LARGURA_JANELA, ALTURA_JANELA
from mysql.connector import Error
from config import Tema_Poliedro, som_erro, som_correto
from menu_tela import MenuTela

class BotaoLogin:
    def __init__(self, rel_rect, text, tela, active=True):
        self.rel_rect = rel_rect
        self.text = text
        self.active = active
        self.hovered = False
        self.enter = False
        self.processar_proximo = False
        self.tela = tela
        self.tema = Tema_Poliedro

        self.colors = { # Cores do botão para cada estado
            "normal": (0, 102, 204),
            "hover": (0, 80, 160),
            "inactive": (180, 180, 180)
        }

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.font = pygame.font.Font(None, 24) # Fonte para o texto do botão 

    def atualizar_rect(self):
        largura, altura = LARGURA_JANELA, ALTURA_JANELA
        x = int(self.rel_rect[0] * largura)
        y = int(self.rel_rect[1] * altura)
        w = int(self.rel_rect[2] * largura)
        h = int(self.rel_rect[3] * altura)
        self.rect = pygame.Rect(x, y, w, h)

        font_size = max(int(h * 0.5), 12)  # Atualiza o tamanho da fonte para se ajustar à altura do botão
        self.font = pygame.font.Font(None, font_size)

    def set_active(self, state: bool):
        self.active = state

    def checar_eventos(self, evento, tela):
        if not self.active:
            return False

        if self.processar_proximo:
            usuario, senha = tela.input_usuario.text.strip(), tela.input_senha.text.strip()
            self.tentar_login(usuario, senha)

        self.processar_proximo = False

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN and not self.processar_proximo:
            tela.mensagem = ""
            self.color = self.colors["hover"]
            self.processar_proximo = True

        if evento.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(evento.pos)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.hovered:
                tela.mensagem = ""
                self.processar_proximo = True


    def update(self, db):
        self.atualizar_rect() # Atualiza a posição e tamanho do botão 
        

    def exibir(self, janela):
        if not self.active:
            self.color = self.colors["inactive"] # Escolhe a cor de acordo com o estado do botão
        else:
            self.color = self.colors["hover"] if (self.hovered or self.processar_proximo) else self.colors["normal"]

        pygame.draw.rect(janela, self.color, self.rect, border_radius=12)  # Desenha o retângulo arredondado

        text_surf = self.font.render(self.text, True, (255, 255, 255))  # Renderiza o texto branco no centro do botão
        text_rect = text_surf.get_rect(center=self.rect.center)
        janela.blit(text_surf, text_rect)

    def tentar_login(self, usuario, senha):
        if not usuario or not senha:
            self.tela.definir_mensagem("Preencha todos os campos.", self.tema["error"])
            if som_erro:
                som_erro.play()
            return

        conn = self.tela.conectar_banco()
        if conn is None:
            self.tela.definir_mensagem("Erro de conexão com o banco.", self.tema["error"])
            if som_erro:
                som_erro.play()
            return

        try:
            cursor = conn.cursor()

            # Tenta logar como aluno
            query_aluno = "SELECT * FROM aluno WHERE mailAluno = %s AND senhaAluno = %s"
            cursor.execute(query_aluno, (usuario, senha))
            resultado = cursor.fetchone()

            if resultado:
                self.usuario_tipo = "aluno"
                if som_correto:
                    som_correto.play()
                conn.close()
                self.tela.gerenciador.trocar_tela(MenuTela)

            # Se não for aluno, tenta professor
            query_professor = "SELECT * FROM professor WHERE mailProf = %s AND senhaProf = %s"
            cursor.execute(query_professor, (usuario, senha))
            resultado = cursor.fetchone()

            if resultado:
                self.usuario_tipo = "professor"
                self.tela.definir_mensagem("Login professor bem sucedido!", self.tema["accent"])
                if som_correto:
                    som_correto.play()
            else:
                self.usuario_tipo = None
                self.tela.definir_mensagem("Usuário ou senha incorretos.", self.tema["error"])
                if som_erro:
                    som_erro.play()

            conn.close()
        except Error as e:
            print(f"Erro ao consultar o banco: {e}")
            self.tela.definir_mensagem("Erro ao consultar o banco.", self.tema["error"])
            if som_erro:
                som_erro.play()