import pygame
from config import LARGURA_JANELA, ALTURA_JANELA
from mysql.connector import Error
from config import Tema_Poliedro, som_erro, som_correto
from menu_tela_aluno import MenuTelaAluno
from menu_tela_professor import MenuTelaProfessor
from usuario import Aluno, Professor

class BotaoLogin:
    def __init__(self, rel_rect, texto, tela, active=True):
        self.rel_rect = rel_rect
        self.texto = texto
        self.active = active
        self.hovered = False
        self.enter = False
        self.processar = False
        self.processar_completo = False
        self.pular_checagem = False
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

        self.color = self.colors["hover"] if self.hovered else self.colors["normal"]

        if not self.processar and self.processar_completo and self.pular_checagem:
            self.processar_completo = False
            self.pular_checagem = False

        if self.pular_checagem:
            self.processar = True

        if not self.pular_checagem:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN and pygame.K_RETURN:
                tela.mensagem = ""
                self.color = self.colors["hover"]
                self.pular_checagem = True

            if evento.type == pygame.MOUSEMOTION:
                self.hovered = self.rect.collidepoint(evento.pos)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and self.hovered:
                    tela.mensagem = ""
                    self.color = self.colors["hover"]
                    self.pular_checagem = True

        if self.pular_checagem and self.processar and not self.processar_completo:
            usuario, senha = tela.input_usuario.text.strip(), tela.input_senha.text.strip()
            self.tentar_login(usuario, senha)
            pygame.event.clear()
            self.color = self.colors["normal"]
            self.processar_completo = True
            self.processar = False

        if evento.type == pygame.VIDEORESIZE:
            pass

    def update(self, db):
        self.atualizar_rect() # Atualiza a posição e tamanho do botão 
        

    def exibir(self, janela):
        if not self.active:
            self.color = self.colors["inactive"] # Cor inativa do botão

        pygame.draw.rect(janela, self.color, self.rect, border_radius=12)  # Desenha o retângulo arredondado

        text_surf = self.font.render(self.texto, True, (255, 255, 255))  # Renderiza o texto branco no centro do botão
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
            query_aluno = "SELECT idAluno, nomeAluno, pontuacao FROM aluno WHERE mailAluno = %s AND senhaAluno = %s"
            cursor.execute(query_aluno, (usuario, senha))
            resultado = cursor.fetchone()
            print(resultado)

            if resultado:
                self.usuario_tipo = "aluno"
                if som_correto:
                    som_correto.play()
                conn.close()
                self.tela.gerenciador.usuario = Aluno(id=resultado[0], nome=resultado[1], pontuacao=resultado[2])
                self.tela.gerenciador.trocar_tela(MenuTelaAluno)

            # Se não for aluno, tenta professor
            query_professor = "SELECT * FROM professor WHERE mailProf = %s AND senhaProf = %s"
            cursor.execute(query_professor, (usuario, senha))
            resultado = cursor.fetchone()

            if resultado:
                self.usuario_tipo = "professor"
                self.tela.definir_mensagem("Login professor bem sucedido!", self.tema["accent"])
                if som_correto:
                    som_correto.play()
                self.tela.gerenciador.trocar_tela(MenuTelaProfessor)
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