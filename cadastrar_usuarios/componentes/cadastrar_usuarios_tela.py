import pygame
import config
from cadastrar_usuarios.componentes.campo_texto import CampoTexto
from cadastrar_usuarios.componentes.botao import BotaoTela
from cadastrar_usuarios.componentes.tipo_usuario import TipoUsuario
from cadastrar_usuarios.database.database import conectar

class CadastrarUsuariosTela:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador

        self.campos = {
            "nome": CampoTexto(
                pygame.Rect((config.LARGURA_JANELA - config.LARGURA_CAMPO)//2, 100, config.LARGURA_CAMPO, config.ALTURA_CAMPO),
                "Digite o nome para cadastro" # Dentro do placeholder nome
            ),
            "email": CampoTexto(
                pygame.Rect((config.LARGURA_JANELA - config.LARGURA_CAMPO)//2, 100 + config.ESPACO_ENTRE, config.LARGURA_CAMPO, config.ALTURA_CAMPO),
                "Ex: JoaoV1" # Dentro do placeholder email
            ),
            "senha": CampoTexto(
                pygame.Rect((config.LARGURA_JANELA - config.LARGURA_CAMPO)//2, 100 + 2*config.ESPACO_ENTRE, config.LARGURA_CAMPO, config.ALTURA_CAMPO),
                "Insira a senha para cadastro" # Dentro do placeholder senha
            )
        }

        self.campo_materia = CampoTexto(
            pygame.Rect((config.LARGURA_JANELA - config.LARGURA_CAMPO)//2, 100 + 4*config.ESPACO_ENTRE + 20, config.LARGURA_CAMPO, config.ALTURA_CAMPO),
            "Ex: Matemática" # Dentro do placeholder materia
        )

        largura_botao_tipo = 180
        espacamento_botao_tipo = 40
        total_largura_tipos = largura_botao_tipo * 2 + espacamento_botao_tipo
        x_inicial_tipos = (config.LARGURA_JANELA - total_largura_tipos) // 2
        y_botao_tipo = 100 + 3 * config.ESPACO_ENTRE + 10

        self.tipo_usuario = TipoUsuario(
            pygame.Rect(x_inicial_tipos, y_botao_tipo, largura_botao_tipo, 50),
            pygame.Rect(x_inicial_tipos + largura_botao_tipo + espacamento_botao_tipo, y_botao_tipo, largura_botao_tipo, 50),
            config.FONTE_PADRAO,
            {'botao': config.COR_BOTAO, 'selecao': config.COR_SELECAO}
        )

        self.botao_cadastrar = BotaoTela(
            pygame.Rect((config.LARGURA_JANELA - config.LARGURA_CAMPO)//2, 50 + 5*config.ESPACO_ENTRE + 60, config.LARGURA_CAMPO, 70), # botao de cadastrar
            "Cadastrar",
            config.FONTE_PADRAO,
            config.COR_BOTAO,
            config.COR_BOTAO_HOVER,
            (255, 255, 255),
            20
        )

        self.campo_atual = "nome"
        self.msg = ""
        self.msg_mostra_tempo = 0
        self.backspace_segurar = False
        self.ultimo_backspace = 0
        self.delay_backspace = 100

    def cadastrar_usuario(self):
        nome = self.campos["nome"].texto.strip()
        email_prefixo = self.campos["email"].texto.strip()
        senha = self.campos["senha"].texto.strip()
        materia = self.campo_materia.texto.strip()
        tipo = self.tipo_usuario.tipo

        if not (nome and email_prefixo and senha):
            self.msg = "Preencha todos os campos obrigatórios!" #Forçar a preencher todos os campos
            self.msg_mostra_tempo = pygame.time.get_ticks()
            return

        if tipo == "professor" and not materia:
            self.msg = "Professores devem informar a matéria." # Caso nao informar a materia
            self.msg_mostra_tempo = pygame.time.get_ticks()
            return

        email_completo = email_prefixo + ("@p4ed.com" if tipo == "aluno" else "@sistemapoliedro.com") #Caso for aluno @p4ed.com, senao professor @sistemapoliedro.com

        conexao = conectar()
        if conexao is None:
            self.msg = "Falha na conexão com o banco."
            self.msg_mostra_tempo = pygame.time.get_ticks()
            return

        try:
            cursor = conexao.cursor()
            if tipo == "aluno":
                sql = "INSERT INTO aluno (nomeAluno, mailAluno, senhaAluno, pontuacao) VALUES (%s, %s, %s, 0)"
                cursor.execute(sql, (nome, email_completo, senha))
            else:
                sql = "INSERT INTO professor (nomeProf, mailProf, senhaProf, materia) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (nome, email_completo, senha, materia))
            conexao.commit()
            self.msg = f"{tipo.capitalize()} cadastrado com sucesso!"
            for c in self.campos.values():
                c.texto = ""
            self.campo_materia.texto = ""
            self.tipo_usuario.tipo = "aluno"
        except Exception as e:
            self.msg = f"Erro ao cadastrar: {e}"
        finally:
            cursor.close()
            conexao.close()
            self.msg_mostra_tempo = pygame.time.get_ticks()

    def checar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos
            for nome_campo, campo in self.campos.items():
                if campo.rect.collidepoint(pos):
                    self.campo_atual = nome_campo
                    return
            if self.campo_materia.rect.collidepoint(pos) and self.tipo_usuario.tipo == "professor":
                self.campo_atual = "materia"
                return
            if self.tipo_usuario.selecionar(pos):
                self.campo_atual = None
                return
            if self.botao_cadastrar.clicado(pos):
                self.cadastrar_usuario()
                return
            self.campo_atual = None

        if evento.type == pygame.KEYDOWN:
            if self.campo_atual:
                if evento.key == pygame.K_TAB:
                    ordem = ["nome", "email", "senha"]
                    if self.tipo_usuario.tipo == "professor":
                        ordem.append("materia")
                    try:
                        idx = ordem.index(self.campo_atual)
                        self.campo_atual = ordem[(idx + 1) % len(ordem)]
                    except ValueError:
                        self.campo_atual = ordem[0]
                if evento.key == pygame.K_BACKSPACE:
                    self.backspace_segurar = True
                    self.ultimo_backspace = pygame.time.get_ticks()
                    self._apagar_caractere()
                if evento.key == pygame.K_RETURN:
                    self.cadastrar_usuario()
                else:
                    self._inserir_caractere(evento.unicode)
            if evento.key == pygame.K_ESCAPE:
                from menu_tela_professor import MenuTelaProfessor
                self.gerenciador.trocar_tela(MenuTelaProfessor)

        if evento.type == pygame.KEYUP and evento.key == pygame.K_BACKSPACE:
            self.backspace_segurar = False

    def _apagar_caractere(self):
        if self.campo_atual == "materia" and self.tipo_usuario.tipo == "professor":
            self.campo_materia.apagar_caractere()
        elif self.campo_atual in self.campos:
            self.campos[self.campo_atual].apagar_caractere()

    def _inserir_caractere(self, char):
        if self.campo_atual == "email":
            if char.isalnum() or char in ['.', '_', '-']:
                self.campos["email"].inserir_caractere(char)
        elif self.campo_atual == "materia" and self.tipo_usuario.tipo == "professor":
            self.campo_materia.inserir_caractere(char)
        elif self.campo_atual in self.campos:
            self.campos[self.campo_atual].inserir_caractere(char)

    def atualizar(self):
        if self.backspace_segurar:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.ultimo_backspace > self.delay_backspace:
                self._apagar_caractere()
                self.ultimo_backspace = tempo_atual

    def exibir(self, janela):
        altura = config.ALTURA_JANELA
        largura = config.LARGURA_JANELA
        for y in range(altura):
            cor = (
                180 + (255-180) * y // altura,
                210 + (255-210) * y // altura,
                255
            )
            pygame.draw.line(janela, cor, (0, y), (largura, y))

        fonte_titulo = pygame.font.SysFont("Segoe UI", 42, bold=True) # Título centralizado no topo
        titulo_surf = fonte_titulo.render("Cadastro de Aluno ou Professor", True, (30, 40, 80)) 
        janela.blit(titulo_surf, titulo_surf.get_rect(center=(largura//2, 50)))

        cores_campos = { # Labels e campos com sombras e bordas arredondadas
            'ativo': (70, 130, 180),
            'inativo': (170, 170, 190),
            'placeholder': (140, 140, 160)
        }
        fonte_label = pygame.font.SysFont('Segoe UI', 24, bold=False)
        for nome_campo, campo in self.campos.items():
            label_texto = {
                "nome": "Nome completo:",
                "email": "Email (sem domínio):",
                "senha": "Senha:"
            }.get(nome_campo, "")
            if label_texto:
                label_surf = fonte_label.render(label_texto, True, (30, 40, 80))
                janela.blit(label_surf, (campo.rect.x + 10, campo.rect.y - 30))

            ativo = (self.campo_atual == nome_campo)
            campo.renderizar(janela, config.FONTE_PADRAO, cores_campos, ativo)

        if self.tipo_usuario.tipo == "professor": # Campo matéria (apenas se for professor)
            label_surf = fonte_label.render("Matéria do professor:", True, (30, 40, 80))
            janela.blit(label_surf, (self.campo_materia.rect.x + 10, self.campo_materia.rect.y - 30))
            ativo = (self.campo_atual == "materia")
            self.campo_materia.renderizar(janela, config.FONTE_PADRAO, cores_campos, ativo)

        self.botao_cadastrar.desenhar(janela)

        self.tipo_usuario.desenhar(janela)   # Tipo de usuário com botões maiores

        if self.msg and pygame.time.get_ticks() - self.msg_mostra_tempo < 5000:
            fonte_msg = pygame.font.SysFont("Segoe UI", 26, bold=True)
            msg_surf = fonte_msg.render(self.msg, True, (255, 255, 255))
            caixa_msg = pygame.Surface((msg_surf.get_width() + 30, msg_surf.get_height() + 20), pygame.SRCALPHA)
            caixa_msg.fill((0, 0, 0, 180))
            caixa_msg.blit(msg_surf, (15, 10))
            janela.blit(caixa_msg, ((largura - caixa_msg.get_width())//2, config.ALTURA_JANELA - caixa_msg.get_height() - 20))

        pygame.display.update()
