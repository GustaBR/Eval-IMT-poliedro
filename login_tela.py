import pygame
import mysql.connector
from mysql.connector import Error
from config import Tema_Poliedro, fonte_negrito, fonte_regular, icone_usuario, icone_cadeado, imagem, dt
from input_box import InputBox
from botao_login import BotaoLogin


class LoginTela:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.tema = Tema_Poliedro
        self.cor_fundo = self.tema["bg"]

        self.input_usuario = InputBox(
            (0.2, 0.48, 0.6, 0.068), "Email de Usuário", icone_usuario, is_senha=False)
        self.input_senha = InputBox(
            (0.2, 0.60, 0.6, 0.068),"Senha", icone_cadeado, is_senha=True)

        self.botao_login = BotaoLogin(
                rel_rect=(0.2, 0.72, 0.6, 0.09),
                texto="Entrar",
                tela=self
            )

        # Mensagem de erro ou sucesso
        self.mensagem = ""
        self.mensagem_cor = self.tema["error"]

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
        self.input_usuario.checar_eventos(evento, self)
        self.input_senha.checar_eventos(evento, self)

        if self.botao_login:
            self.botao_login.checar_eventos(evento, self)

    def definir_mensagem(self, texto, cor):
        self.mensagem = texto
        self.mensagem_cor = cor

    def atualizar(self):
        janela = pygame.display.get_surface()
        largura, altura = janela.get_size()

        self.input_usuario.atualizar_rect(janela)
        self.input_senha.atualizar_rect(janela)

        self.input_usuario.atualizar()
        self.input_senha.atualizar()

        campos_preenchidos = bool(self.input_usuario.text.strip()) and bool(self.input_senha.text.strip())
        if self.botao_login:
            self.botao_login.set_active(campos_preenchidos)
            self.botao_login.update(None)

    def exibir(self, janela):
        janela.fill(self.cor_fundo)
        largura, altura = janela.get_size()

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
            janela.blit(scaled_img, (x_pos, 0))
            altura_header = nova_altura
        else:
            altura_header = 0

        titulo_y = altura_header + int(altura * 0.03)
        titulo_surf = fonte_negrito.render("Entrar na Plataforma Poliedro", True, self.tema["accent"]) # Titulo da tela
        titulo_rect = titulo_surf.get_rect(center=(largura // 2, titulo_y))
        janela.blit(titulo_surf, titulo_rect)

        desc_y = titulo_y + int(altura * 0.05)
        desc_surf = fonte_regular.render("Digite seu usuário e senha para continuar.", True, self.tema["accent"]) # texto da tela
        desc_rect = desc_surf.get_rect(center=(largura // 2, desc_y))
        janela.blit(desc_surf, desc_rect)

        self.input_usuario.exibir(janela)
        self.input_senha.exibir(janela)
        self.botao_login.exibir(janela)

        if self.mensagem:  # Mensagem de status
            msg_surf = fonte_regular.render(self.mensagem, True, self.mensagem_cor)
            msg_rect = msg_surf.get_rect(center=(largura // 2, int(altura * 0.85)))
            janela.blit(msg_surf, msg_rect)
