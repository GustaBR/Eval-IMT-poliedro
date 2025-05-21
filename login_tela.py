import pygame
import mysql.connector
from mysql.connector import Error
from config import Tema_Poliedro, fonte_negrito, fonte_regular, som_erro, som_correto, icone_usuario, icone_cadeado, imagem
from input_box import InputBox
from botao_login import BotaoLogin

class LoginTela:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.tema = Tema_Poliedro
        self.cor_fundo = self.tema["bg"]

        self.input_usuario = InputBox(
            (0, 0), (0.2, 0.48, 0.6, 0.068), "Usuário", icone_usuario)
        self.input_senha = InputBox(
            (0, 0), (0.2, 0.60, 0.6, 0.068), "Senha", icone_cadeado, is_password=True)
        
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
        self.input_usuario.checar_eventos(evento)
        self.input_senha.checar_eventos(evento)
        if self.botao_login.checar_eventos(evento):
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

        campos_preenchidos = bool(self.input_usuario.text.strip()) and bool(self.input_senha.text.strip())
        self.botao_login.set_active(campos_preenchidos) # Continuar alterações daqui ## Tentar ajeitar a classe Button.
        self.botao_login.atualizar()

        '''if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""
                '''

    def exibir(self, janela):
        
        # Botão login
        self.botao_login = BotaoLogin(janela, (0.2, 0.72, 0.6, 0.09), "Entrar")

        # Caixas de entrada
        self.janela.fill(self.cor_fundo)
        largura, altura = self.janela.get_size()
        if self.header_img_original:
            img_w, img_h = self.header_img_original.get_size()
            escala = largura / img_w
            nova_largura = int(img_w * escala)
            nova_altura = int(img_h * escala)

            altura_maxima = int(altura * 0.35)
            if nova_altura > altura_maxima:
                scale = altura_maxima / img_h
                nova_largura = int(img_w * scale)
                nova_altura = altura_maxima

            scaled_img = pygame.transform.smoothscale(self.header_img_original, (nova_largura, nova_altura))
            x_pos = (largura - nova_largura) // 2 
            self.surface.blit(scaled_img, (x_pos, 0))
            altura_header = nova_altura
        else:
            altura_header = 0

        titulo_y = altura_header + int(altura * 0.03)
        titulo_surf = fonte_negrito.render("Entrar na Plataforma Poliedro", True, self.tema["accent"])
        titulo_rect = titulo_surf.get_rect(center=(largura // 2, titulo_y))
        self.janela.blit(titulo_surf, titulo_rect)

        desc_y = titulo_y + int(altura * 0.05)
        desc_surf = fonte_regular.render("Digite seu usuário e senha para continuar.", True, self.tema["accent"])
        desc_rect = desc_surf.get_rect(center=(largura // 2, desc_y))
        self.janela.blit(desc_surf, desc_rect)

        self.input_usuario.draw()
        self.input_senha.draw()
        self.botao_login.exibir_botao()

        if self.mensagem:
            msg_surf = fonte_regular.render(self.message, True, self.mensagem_cor)
            msg_rect = msg_surf.get_rect(center=(largura // 2, int(altura * 0.85)))
            self.janela.blit(msg_surf, msg_rect)

        