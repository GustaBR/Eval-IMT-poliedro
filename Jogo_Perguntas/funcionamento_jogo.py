import pygame
import os 
import random
import time
from config import LARGURA_JANELA, ALTURA_JANELA
from jogo_perguntas.config import CAMINHO_IMAGEM_FUNDO_PERSONALIZADA, DIRETORIO_ASSETS
from jogo_perguntas.tema.tema_visual import Tema
from jogo_perguntas.interface.interface_grafica import GerenciadorInterface
from jogo_perguntas.interface.selecao_materia_tela import TelaSelecaoMateria
from jogo_perguntas.database.gerenciador_banco_dados import GerenciadorBancoPerguntas
from jogo_perguntas.tema.elementos_cores import Botao

class JogoTela:
    def __init__(self, gerenciador):
        # pygame.font.init() 

        self.gerenciador = gerenciador
        self.gerenciador_banco = GerenciadorBancoPerguntas()
        self.interface_grafica = GerenciadorInterface(LARGURA_JANELA, ALTURA_JANELA) 
        self.ids_perguntas_vistas_por_materia = {}

        self._inicializar_botoes_comuns_jogo()
        
        self.tela_ativa_selecao_materia = TelaSelecaoMateria(LARGURA_JANELA, ALTURA_JANELA, self) 

        self.estado_jogo_atual = "SELECAO_MATERIA"
        self.nome_materia_atual = None
        self.lista_perguntas_rodada_atual = []
        self.indice_pergunta_rodada = 0
        self.pontuacao_rodada = 0
        self.objeto_pergunta_atual = None
        self.indices_respostas_eliminadas_na_pergunta = []
        self.dica_pergunta_ativa = False
        self.tipo_confirmacao_pendente = None
        self.ajuda_pulo_usada_rodada = False
        self.ajuda_50_50_usada_rodada = False
        self.indice_resposta_selecionada_para_confirmacao = -1
        self.texto_final_resposta_correta = None
        self.jogo_rodando = False
        self.valor_questoes = {
            0: 1000,
            5: 5000,
            6: 10000,
            10: 50000,
            11: 100000,
            14: 600000
        }

    def _inicializar_botoes_comuns_jogo(self):
        self.botoes_alternativas = []
        margem_lateral_resp = LARGURA_JANELA * 0.1
        largura_botao_resp = LARGURA_JANELA - 2 * margem_lateral_resp
        altura_botao_resp = ALTURA_JANELA * 0.07
        espaco_vertical_resp = ALTURA_JANELA * 0.02
        y_inicio_respostas = ALTURA_JANELA * 0.38 
        
        fonte_botoes_jogo = self.interface_grafica.get_fonte_ui('media')
        for i in range(4):
            pos_y = y_inicio_respostas + i * (altura_botao_resp + espaco_vertical_resp)
            botao_alt = Botao(
                margem_lateral_resp, pos_y, largura_botao_resp, altura_botao_resp,
                Tema.CORES['botao_normal'], Tema.CORES['botao_hover'], Tema.CORES['borda_botao'],
                f"Alternativa {chr(65+i)}", fonte_botoes_jogo, Tema.CORES['texto_botao'], 10,
                acao=lambda idx=i: self._iniciar_confirmacao_de_resposta(idx)
            )
            self.botoes_alternativas.append(botao_alt)

        num_botoes_acao_jogo = 3
        largura_area_botoes_acao = LARGURA_JANELA - 2 * margem_lateral_resp
        espaco_entre_botoes_acao_jogo = 20 
        largura_botao_acao_jogo = (largura_area_botoes_acao - (num_botoes_acao_jogo - 1) * espaco_entre_botoes_acao_jogo) / num_botoes_acao_jogo
        altura_botao_acao_jogo = ALTURA_JANELA * 0.075
        y_pos_botoes_acao_jogo = ALTURA_JANELA - altura_botao_acao_jogo - ALTURA_JANELA * 0.05

        self.botao_dica = Botao(
            margem_lateral_resp, y_pos_botoes_acao_jogo, largura_botao_acao_jogo, altura_botao_acao_jogo,
            Tema.CORES['botao_dica'], Tema.CORES['botao_hover'], Tema.CORES['borda_botao'],
            "Dica", fonte_botoes_jogo, Tema.CORES['texto_botao'], 10,
            acao=self.ativar_ou_desativar_dica
        )
        self.botao_50_50 = Botao(
            margem_lateral_resp + largura_botao_acao_jogo + espaco_entre_botoes_acao_jogo, 
            y_pos_botoes_acao_jogo, largura_botao_acao_jogo, altura_botao_acao_jogo,
            Tema.CORES['botao_eliminar'], Tema.CORES['botao_hover'], Tema.CORES['borda_botao'],
            "50/50", fonte_botoes_jogo, Tema.CORES['texto_botao'], 10,
            acao=self.usar_ajuda_50_50
        )
        self.botao_pular = Botao(
            margem_lateral_resp + 2 * (largura_botao_acao_jogo + espaco_entre_botoes_acao_jogo), 
            y_pos_botoes_acao_jogo, largura_botao_acao_jogo, altura_botao_acao_jogo,
            Tema.CORES['botao_pular'], Tema.CORES['botao_hover'], Tema.CORES['borda_botao'],
            "Pular", fonte_botoes_jogo, Tema.CORES['texto_botao'], 10,
            acao=self._iniciar_confirmacao_pular_pergunta
        )

        self.botao_popup_confirmar = Botao(
            0,0, 150, 50, 
            Tema.CORES['botao_confirmar'], Tema.CORES['botao_hover'], Tema.CORES['borda_botao'],
            "Confirmar", fonte_botoes_jogo, Tema.CORES['texto_botao'], 8,
            acao=self._processar_acao_confirmada
        )
        self.botao_popup_cancelar = Botao(
            0,0, 150, 50,
            Tema.CORES['botao_cancelar'], Tema.CORES['botao_hover'], Tema.CORES['borda_botao'],
            "Cancelar", fonte_botoes_jogo, Tema.CORES['texto_botao'], 8,
            acao=self._cancelar_acao_pendente
        )
        
        larg_botao_final = LARGURA_JANELA * 0.4
        alt_botao_final = ALTURA_JANELA * 0.08
        self.botao_final_jogar_novamente = Botao(
            0,0, larg_botao_final, alt_botao_final,
            Tema.CORES['botao_reiniciar'], Tema.CORES['botao_hover'], Tema.CORES['borda_botao'],
            "Jogar Novamente", fonte_botoes_jogo, Tema.CORES['texto_botao'], 10,
            acao=self.reiniciar_para_selecao_materia
        )
        self.botao_final_sair = Botao(
            0,0, larg_botao_final, alt_botao_final,
            Tema.CORES['botao_sair'], Tema.CORES['botao_hover'], None, 
            "Sair do Jogo", fonte_botoes_jogo, Tema.CORES['texto_botao'], 10,
            acao=lambda:self.retornar()
        )

    def retornar(self):
        from menu_tela_aluno import MenuTelaAluno
        self.gerenciador.trocar_tela(MenuTelaAluno)

    def iniciar_rodada_materia(self, nome_materia_escolhida):
        self.nome_materia_atual = nome_materia_escolhida
        ids_vistos_nesta_materia = self.ids_perguntas_vistas_por_materia.get(nome_materia_escolhida, set())
        
        self.lista_perguntas_rodada_atual = self.gerenciador_banco.obter_perguntas_por_materia(
            self.nome_materia_atual,
            ids_vistos_nesta_materia,
            limite_perguntas=15
        )
        
        if self.lista_perguntas_rodada_atual:
            ids_carregados_nesta_rodada = {p.id_questao for p in self.lista_perguntas_rodada_atual}
            self.ids_perguntas_vistas_por_materia.setdefault(nome_materia_escolhida, set()).update(ids_carregados_nesta_rodada)

            self.indice_pergunta_rodada = 0
            self.pontuacao_rodada = 0
            self.ajuda_pulo_usada_rodada = False
            self.ajuda_50_50_usada_rodada = False
            self.botao_50_50.habilitado = True 
            self.botao_pular.habilitado = True
            self.indices_respostas_eliminadas_na_pergunta = []
            self.dica_pergunta_ativa = False
            self.tipo_confirmacao_pendente = None
            self.indice_resposta_selecionada_para_confirmacao = -1
            
            self._carregar_proxima_pergunta_rodada() 
            self.estado_jogo_atual = "JOGANDO"
        else:
            msg_sem_perguntas = f"Nenhuma pergunta encontrada para '{self.nome_materia_atual}'."
            if ids_vistos_nesta_materia:
                 msg_sem_perguntas = f"Não há mais perguntas inéditas para '{self.nome_materia_atual}'."
            self.interface_grafica.exibir_notificacao(msg_sem_perguntas, "info", 4000)
            self.nome_materia_atual = None


    def _carregar_proxima_pergunta_rodada(self):
        if self.indice_pergunta_rodada < len(self.lista_perguntas_rodada_atual):
            print(self.indice_pergunta_rodada, len(self.lista_perguntas_rodada_atual))
            self.objeto_pergunta_atual = self.lista_perguntas_rodada_atual[self.indice_pergunta_rodada]
            self.indices_respostas_eliminadas_na_pergunta = []
            self.dica_pergunta_ativa = False
            self.tipo_confirmacao_pendente = None 
            self.indice_resposta_selecionada_para_confirmacao = -1
            
            for i, botao_alt in enumerate(self.botoes_alternativas):
                if i < len(self.objeto_pergunta_atual.alternativas):
                    botao_alt.texto = f"{chr(65 + i)}) {self.objeto_pergunta_atual.alternativas[i]}"
                    botao_alt.habilitado = True 
                    botao_alt.cor_normal = Tema.CORES['botao_normal']
                else:
                    botao_alt.texto = ""
                    botao_alt.habilitado = False
            self.interface_grafica.exibir_notificacao(f"Pergunta {self.indice_pergunta_rodada + 1} de {len(self.lista_perguntas_rodada_atual)}", "info")
        else: 
            self.estado_jogo_atual = "FIM_DE_JOGO"
            msg_fim_rodada = "Fim da rodada de perguntas!"
            if self.indice_pergunta_rodada == len(self.lista_perguntas_rodada_atual) and len(self.lista_perguntas_rodada_atual) > 0:
                msg_fim_rodada = f"Parabéns! Acertou todas as {len(self.lista_perguntas_rodada_atual)} perguntas!"
                self.interface_grafica.exibir_notificacao("Rodada perfeita!", "sucesso", 3000)
                self.gerenciador_banco.atualizar_pontuacao(self.gerenciador.usuario, self.pontuacao_rodada)
            else:
                self.interface_grafica.exibir_notificacao("Rodada concluída!", "info", 3000)
                self.gerenciador_banco.atualizar_pontuacao(self.gerenciador.usuario, self.pontuacao_rodada)
            self.texto_final_resposta_correta = msg_fim_rodada


    def _iniciar_confirmacao_de_resposta(self, indice_alternativa_clicada):
        if indice_alternativa_clicada in self.indices_respostas_eliminadas_na_pergunta: return
        
        self.indice_resposta_selecionada_para_confirmacao = indice_alternativa_clicada
        self.tipo_confirmacao_pendente = "resposta"
        for i, botao_alt in enumerate(self.botoes_alternativas):
            if i == indice_alternativa_clicada:
                botao_alt.cor_normal = Tema.CORES['botao_hover'] 
            else:
                botao_alt.cor_normal = Tema.CORES['botao_normal']

    def _iniciar_confirmacao_pular_pergunta(self):
        if not self.ajuda_pulo_usada_rodada and self.objeto_pergunta_atual:
            self.tipo_confirmacao_pendente = "pular"
        elif self.ajuda_pulo_usada_rodada:
            self.interface_grafica.exibir_notificacao("Pulo já utilizado nesta rodada.", "info")

    def _processar_acao_confirmada(self):
        if self.tipo_confirmacao_pendente == "resposta":
            self._validar_resposta_escolhida(self.indice_resposta_selecionada_para_confirmacao)
        elif self.tipo_confirmacao_pendente == "pular":
            self._executar_pulo_confirmado()
        
        self.tipo_confirmacao_pendente = None
        self.indice_resposta_selecionada_para_confirmacao = -1
        for botao_alt in self.botoes_alternativas:
            botao_alt.cor_normal = Tema.CORES['botao_normal']

    def _cancelar_acao_pendente(self):
        self.interface_grafica.exibir_notificacao("Ação cancelada.", "info")
        self.tipo_confirmacao_pendente = None
        self.indice_resposta_selecionada_para_confirmacao = -1
        for botao_alt in self.botoes_alternativas:
            botao_alt.cor_normal = Tema.CORES['botao_normal']

    def _validar_resposta_escolhida(self, indice_resposta_jogador):
        if self.objeto_pergunta_atual and indice_resposta_jogador == self.objeto_pergunta_atual.indice_correta:
            for rodada, valor in sorted(self.valor_questoes.items(), reverse=True):
                if self.indice_pergunta_rodada >= rodada:
                    valor_ganho = valor
                    break
            self.pontuacao_rodada += valor_ganho
            self.interface_grafica.exibir_notificacao("Resposta Correta!", "sucesso")
            self.indice_pergunta_rodada += 1
            pygame.time.wait(1200) 
            self._carregar_proxima_pergunta_rodada()
        else: 
            self.interface_grafica.exibir_notificacao("Resposta Incorreta!", "erro")
            self.pontuacao_rodada = self.pontuacao_rodada//2
            self.gerenciador_banco.atualizar_pontuacao(self.gerenciador.usuario, self.pontuacao_rodada)
            print("teste maluco")
            if self.objeto_pergunta_atual:
                self.texto_final_resposta_correta = self.objeto_pergunta_atual.alternativas[self.objeto_pergunta_atual.indice_correta]
            else:
                 self.texto_final_resposta_correta = "N/A (Erro ao obter pergunta)"
            self.estado_jogo_atual = "FIM_DE_JOGO"
            pygame.time.wait(1000)
        
    def ativar_ou_desativar_dica(self):
        if self.tipo_confirmacao_pendente: return

        if self.objeto_pergunta_atual and self.objeto_pergunta_atual.dica:
            self.dica_pergunta_ativa = not self.dica_pergunta_ativa
            msg = "Dica ativada!" if self.dica_pergunta_ativa else "Dica desativada."
            self.interface_grafica.exibir_notificacao(msg, "info")
        elif self.objeto_pergunta_atual and not self.objeto_pergunta_atual.dica:
                self.interface_grafica.exibir_notificacao("Sem dica para esta pergunta.", "info")

    def usar_ajuda_50_50(self):
        if self.tipo_confirmacao_pendente: return
        if self.ajuda_50_50_usada_rodada:
            self.interface_grafica.exibir_notificacao("50/50 já utilizado nesta rodada.", "info")
            return
        if not self.objeto_pergunta_atual: return

        indices_incorretas_disponiveis = [
            i for i in range(len(self.objeto_pergunta_atual.alternativas))
            if i != self.objeto_pergunta_atual.indice_correta and i not in self.indices_respostas_eliminadas_na_pergunta
        ]

        if len(indices_incorretas_disponiveis) >= 2 : # Garante que há pelo menos 2 incorretas para eliminar 1
            num_para_eliminar = len(indices_incorretas_disponiveis) - 1 # Deixa 1 incorreta + a correta
            
            alternativas_a_eliminar_agora = random.sample(indices_incorretas_disponiveis, num_para_eliminar)
            self.indices_respostas_eliminadas_na_pergunta.extend(alternativas_a_eliminar_agora)
            self.ajuda_50_50_usada_rodada = True
            self.botao_50_50.habilitado = False 
            self.interface_grafica.exibir_notificacao("50/50: Duas alternativas eliminadas!", "info")
            
            for idx in self.indices_respostas_eliminadas_na_pergunta:
                if idx < len(self.botoes_alternativas):
                    self.botoes_alternativas[idx].habilitado = False
        else:
            self.interface_grafica.exibir_notificacao("Não há alternativas suficientes para usar o 50/50.", "info")

    def _executar_pulo_confirmado(self): 
        if self.ajuda_pulo_usada_rodada: return
        if not self.objeto_pergunta_atual: return

        self.ajuda_pulo_usada_rodada = True
        self.botao_pular.habilitado = False 
        self.indice_pergunta_rodada += 1
        self.interface_grafica.exibir_notificacao("Pergunta Pulada!", "info")
        pygame.time.wait(1200)
        self._carregar_proxima_pergunta_rodada()
    
    def reiniciar_para_selecao_materia(self):
        self.estado_jogo_atual = "SELECAO_MATERIA"
        self.nome_materia_atual = None
        self.lista_perguntas_rodada_atual = []
        self.indice_pergunta_rodada = 0
        self.objeto_pergunta_atual = None
        self.texto_final_resposta_correta = None
        self.tipo_confirmacao_pendente = None
        
        self.botao_pular.habilitado = True 
        self.botao_50_50.habilitado = True

        self.tela_ativa_selecao_materia = TelaSelecaoMateria(LARGURA_JANELA, ALTURA_JANELA, self)
        self.interface_grafica.exibir_notificacao("Escolha uma matéria!", "info")
    
    def encerrar_jogo(self):
        self.jogo_rodando = False

    def checar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: 
                if self.estado_jogo_atual == "SELECAO_MATERIA" and self.tela_ativa_selecao_materia:
                    self.tela_ativa_selecao_materia.processar_clique(evento.pos) 
                
                elif self.estado_jogo_atual == "JOGANDO":
                    if self.tipo_confirmacao_pendente:
                        self.botao_popup_confirmar.tratar_clique()
                        self.botao_popup_cancelar.tratar_clique()
                    elif self.objeto_pergunta_atual:
                        if self.botao_dica.tratar_clique(): pass
                        elif self.botao_50_50.tratar_clique(): pass
                        elif self.botao_pular.tratar_clique(): pass
                        else: 
                            for botao_alt in self.botoes_alternativas:
                                if botao_alt.tratar_clique(): break 
                
                elif self.estado_jogo_atual == "FIM_DE_JOGO":
                    self.botao_final_jogar_novamente.tratar_clique()
                    self.botao_final_sair.tratar_clique()
            
            if self.estado_jogo_atual == "SELECAO_MATERIA" and self.tela_ativa_selecao_materia and (evento.button == 4 or evento.button == 5):
                self.tela_ativa_selecao_materia.tratar_evento_scroll(evento)
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            from menu_tela_aluno import MenuTelaAluno 
            self.gerenciador.trocar_tela(MenuTelaAluno)
    def atualizar(self):
        pos_mouse_atual = pygame.mouse.get_pos()

        if self.estado_jogo_atual == "SELECAO_MATERIA":
            if self.tela_ativa_selecao_materia:
                self.tela_ativa_selecao_materia.atualizar_hover_botoes(pos_mouse_atual)
        elif self.estado_jogo_atual == "JOGANDO":
            if self.tipo_confirmacao_pendente: 
                self.botao_popup_confirmar.verificar_hover(pos_mouse_atual)
                self.botao_popup_cancelar.verificar_hover(pos_mouse_atual)
            elif self.objeto_pergunta_atual: 
                for botao_alt in self.botoes_alternativas: botao_alt.verificar_hover(pos_mouse_atual)
                self.botao_dica.verificar_hover(pos_mouse_atual)
                self.botao_50_50.verificar_hover(pos_mouse_atual)
                self.botao_pular.verificar_hover(pos_mouse_atual)
        elif self.estado_jogo_atual == "FIM_DE_JOGO":
            self.botao_final_jogar_novamente.verificar_hover(pos_mouse_atual)
            self.botao_final_sair.verificar_hover(pos_mouse_atual)

    def exibir(self, janela):
        if self.interface_grafica.imagem_fundo:
            janela.blit(self.interface_grafica.imagem_fundo, (0,0))
        else:
            janela.fill(Tema.CORES['fundo_padrao'])


        if self.estado_jogo_atual == "SELECAO_MATERIA" and self.tela_ativa_selecao_materia:
            self.tela_ativa_selecao_materia.desenhar_tela(janela)
        elif self.estado_jogo_atual == "JOGANDO":
            if self.objeto_pergunta_atual:
                self.interface_grafica.desenhar_caixa_pergunta(janela, self.objeto_pergunta_atual.enunciado)
                for i, botao_alt in enumerate(self.botoes_alternativas):
                    botao_alt.desenhar(janela)
                    if i in self.indices_respostas_eliminadas_na_pergunta and not botao_alt.habilitado:
                        overlay_eliminada_surf = pygame.Surface((botao_alt.rect.width, botao_alt.rect.height), pygame.SRCALPHA)
                        overlay_eliminada_surf.fill(Tema.CORES['resposta_eliminada_overlay'])
                        janela.blit(overlay_eliminada_surf, botao_alt.rect.topleft)
                self.botao_dica.desenhar(janela)
                self.botao_50_50.desenhar(janela)
                self.botao_pular.desenhar(janela)
                self.interface_grafica.desenhar_info_pontuacao(janela, self.pontuacao_rodada)
                if self.dica_pergunta_ativa and self.objeto_pergunta_atual.dica:
                    self.interface_grafica.desenhar_balao_dica(janela, self.objeto_pergunta_atual.dica, self.botao_dica.rect)
                if self.tipo_confirmacao_pendente:
                    texto_popup_principal = "Tem certeza?"
                    if self.tipo_confirmacao_pendente == "resposta" and self.indice_resposta_selecionada_para_confirmacao != -1:
                        try:
                            alt_txt_selecionado = self.objeto_pergunta_atual.alternativas[self.indice_resposta_selecionada_para_confirmacao]
                            max_len_alt_popup = 35
                            if len(alt_txt_selecionado) > max_len_alt_popup: alt_txt_selecionado = alt_txt_selecionado[:max_len_alt_popup-3] + "..."
                            texto_popup_principal = f"Confirma: '{alt_txt_selecionado}'?"
                        except IndexError: texto_popup_principal = "Confirmar esta resposta?"
                    elif self.tipo_confirmacao_pendente == "pular":
                        texto_popup_principal = "Deseja realmente pular esta pergunta?"
                    self.interface_grafica.desenhar_popup_confirmacao(janela, [self.botao_popup_confirmar, self.botao_popup_cancelar], texto_popup_principal)
            else: 
                fonte_carregando_jogo = self.interface_grafica.get_fonte_ui('grande')
                surface_carregando_jogo = fonte_carregando_jogo.render("Carregando Pergunta...", True, Tema.CORES['texto_principal'])
                janela.blit(surface_carregando_jogo, ((LARGURA_JANELA - surface_carregando_jogo.get_width())//2, ALTURA_JANELA//2))
        elif self.estado_jogo_atual == "FIM_DE_JOGO":
            self.interface_grafica.desenhar_tela_final(janela, self.pontuacao_rodada, [self.botao_final_jogar_novamente, self.botao_final_sair], self.texto_final_resposta_correta)

        self.interface_grafica.desenhar_notificacao_flutuante(janela)

        self.gerenciador_banco.desconectar_banco()