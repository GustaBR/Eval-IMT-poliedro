import pygame
import mysql.connector
from mysql.connector import Error
from config import Tema_Poliedro, fonte_negrito, fonte_regular,
som_erro, som_correto, icone_usuario, icone_cadeado, imagem
from components.input_box import InputBox
from components.botao import Button
from config import 

class LoginTela:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.tema = Tema_Poliedro
        self.cor_fundo = self.tema["bg"]

    def conectar_banco(self):
        try:
            return mysql.connector.connect(
                host="jogomilhao-pi11semestre.l.aivencloud.com",
                user="avnadmin",
                port="25159",
                password="AVNS_2oEh5hU00BYuzgIhTXP",
                database="jogomilhao"
            )
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            return None

    def checar_eventos(self, evento):
        self.input_usuario.checar_eventos(event)
        self.input_senha.checar_eventos(event)
        if self.botao_login.checar_eventos(event):
            self.tentar_login()

    def tentar_login(self):
        usuario = self.input_usuario.text.strip()
        senha = self.input_senha.text.strip()

        if not usuario or not senha:
            self.definir_messagem("Preencha todos os campos.", self.tema["error"])
            if som_erro:
                som_erro.play()
            return

        conn = self.conectar_banco()
        if conn is None:
            self.definir_mensagem("Erro de conexão com o banco.", self.theme["error"])
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
                self.definir_mensagem("Login aluno bem sucedido!", self.tema["accent"])
                if som_correto:
                    som_correto.play()
                conn.close()
                return

            # Se não for aluno, tenta professor
            query_professor = "SELECT * FROM professor WHERE mailProf = %s AND senhaProf = %s"
            cursor.execute(query_professor, (usuario, senha))
            resultado = cursor.fetchone()

            if resultado:
                self.usuario_tipo = "professor"
                self.definir_mensagem("Login professor bem sucedido!", self.tema["accent"])
                if som_correto:
                    som_correto.play()
            else:
                self.usuario_tipo = None
                self.definir_mensagem("Usuário ou senha incorretos.", self.tema["error"])
                if som_erro:
                    som_erro.play()

            conn.close()
        except Error as e:
            print(f"Erro ao consultar o banco: {e}")
            self.definir_mensagem("Erro ao consultar o banco.", self.tema["error"])
            if som_erro:
                som_erro.play()

    def definir_mensagem(self, texto, cor):
        self.mensagem = texto
        self.mensagem_cor = cor
        self.mensagem_timer = 3

    def atualizar(self):
        self.input_user.update()
        self.input_pass.update()

        campos_preenchidos = bool(self.input_usuario.text.strip())
        and bool(self.input_senha.text.strip())
        self.botao_login.set_active(campos_preenchidos) # Continuar alterações daqui ## Tentar ajeitar a classe Button.
        self.botao_login.update(dt)

        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""

    def exibir(self, janela)
        # Caixas de entrada
        self.input_usuario = InputBox(
            janela, (0.2, 0.48, 0.6, 0.068), "Usuário", icone_usuario)
        self.input_senha = InputBox(
            janela, (0.2, 0.60, 0.6, 0.068), "Senha", icone_cadeado, is_password=True)
        
        # Botão login
        self.botao_login = Button(janela, (0.2, 0.72, 0.6, 0.09), "Entrar")

        # Mensagem de erro ou sucesso
        self.mensagem = ""
        self.mensagem_cor = self.tema["error"]
        self.mensagem_timer = 0

        # Tipo de usuário logado: None, "aluno" ou "professor"
        self.usuario_tipo = None

        try:
            self.header_img_original = pygame.image.load(
                f"{imagem}/poliedro.png").convert_alpha()
        except Exception:
            self.header_img_original = None
