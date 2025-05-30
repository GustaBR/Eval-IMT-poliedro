import pygame
import os
from config import CAMINHO_IMAGEM_FUNDO_PERSONALIZADA, LARGURA_TELA, ALTURA_TELA # Adicionado LARGURA_TELA, ALTURA_TELA caso for necessário
from tema.tema_visual import Tema

class GerenciadorInterface:
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.imagem_fundo = None 
        self._carregar_imagem_fundo()

        self.notificacao_ativa = False
        self.notificacao_texto = ""
        self.notificacao_cor_fundo = Tema.CORES['notificacao_info_fundo']
        self.notificacao_tempo_final = 0
        
    def _carregar_imagem_fundo(self):
        if CAMINHO_IMAGEM_FUNDO_PERSONALIZADA and os.path.exists(CAMINHO_IMAGEM_FUNDO_PERSONALIZADA):
            try:
                imagem_original = pygame.image.load(CAMINHO_IMAGEM_FUNDO_PERSONALIZADA).convert()
                self.imagem_fundo = pygame.transform.scale(imagem_original, (self.largura_tela, self.altura_tela))
                print(f"Imagem de fundo '{CAMINHO_IMAGEM_FUNDO_PERSONALIZADA}' carregada.")
            except pygame.error as e:
                print(f"Erro ao carregar imagem de fundo '{CAMINHO_IMAGEM_FUNDO_PERSONALIZADA}': {e}")
                self.imagem_fundo = None
        elif CAMINHO_IMAGEM_FUNDO_PERSONALIZADA: 
            print(f"Aviso: Imagem de fundo '{CAMINHO_IMAGEM_FUNDO_PERSONALIZADA}' não encontrada.")
            self.imagem_fundo = None
        else:
            # print("Nenhuma imagem de fundo personalizada. Usando cor de fundo padrão.") # Comentado para reduzir logs
            self.imagem_fundo = None

    def get_fonte_ui(self, tipo_tamanho_str):
        return Tema.get_fonte(tipo_tamanho_str, self.altura_tela)

    def desenhar_texto_multilinha(self, tela, texto, pos_inicial, fonte, cor, largura_maxima, 
                                  espacamento_linhas=5, centralizar_horizontal=False, 
                                  centralizar_vertical=False, rect_referencia_centralizacao=None):
        palavras = texto.split(' ')
        linhas_surface_texto = []
        linha_atual_palavras_str = ""

        for palavra in palavras:
            linha_teste_str = linha_atual_palavras_str + palavra + " "
            if fonte.render(linha_teste_str, True, cor).get_width() <= largura_maxima:
                linha_atual_palavras_str = linha_teste_str
            else:
                linhas_surface_texto.append(fonte.render(linha_atual_palavras_str.strip(), True, cor))
                linha_atual_palavras_str = palavra + " "
        linhas_surface_texto.append(fonte.render(linha_atual_palavras_str.strip(), True, cor))

        altura_total_render_texto = sum(surf.get_height() for surf in linhas_surface_texto) + \
                                 (len(linhas_surface_texto) - 1) * espacamento_linhas
        
        y_desenho_atual = pos_inicial[1]
        if centralizar_vertical:
            if rect_referencia_centralizacao:
                y_desenho_atual = rect_referencia_centralizacao.y + (rect_referencia_centralizacao.height - altura_total_render_texto) // 2
            else: 
                y_desenho_atual = pos_inicial[1] - altura_total_render_texto // 2

        for linha_surface in linhas_surface_texto:
            x_desenho_atual = pos_inicial[0]
            if centralizar_horizontal:
                if rect_referencia_centralizacao:
                    x_desenho_atual = rect_referencia_centralizacao.x + (rect_referencia_centralizacao.width - linha_surface.get_width()) // 2
                else: 
                    x_desenho_atual = pos_inicial[0] - linha_surface.get_width() // 2
            
            tela.blit(linha_surface, (x_desenho_atual, y_desenho_atual))
            y_desenho_atual += linha_surface.get_height() + espacamento_linhas
        return y_desenho_atual

    def desenhar_caixa_pergunta(self, tela, texto_pergunta):
        fonte_pergunta = self.get_fonte_ui('grande')
        cor_texto = Tema.CORES['texto_principal']
        cor_caixa = Tema.CORES['caixa_pergunta']
        cor_borda = Tema.CORES['borda_caixa']
        margem_externa_caixa = 40
        padding_interno_caixa = 20
        altura_caixa = self.altura_tela * 0.25
        rect_caixa = pygame.Rect(margem_externa_caixa, margem_externa_caixa * 0.8, 
                                 self.largura_tela - 2 * margem_externa_caixa, altura_caixa)
        pygame.draw.rect(tela, cor_caixa, rect_caixa, border_radius=10)
        pygame.draw.rect(tela, cor_borda, rect_caixa, 2, border_radius=10)
        largura_max_texto_pergunta = rect_caixa.width - 2 * padding_interno_caixa
        self.desenhar_texto_multilinha(
            tela, texto_pergunta,
            (rect_caixa.x + padding_interno_caixa, rect_caixa.y + padding_interno_caixa),
            fonte_pergunta, cor_texto, largura_max_texto_pergunta,
            centralizar_vertical=True, rect_referencia_centralizacao=rect_caixa
        )

    def desenhar_balao_dica(self, tela, texto_dica, rect_botao_dica_referencia):
        if not texto_dica: return
        fonte_dica = self.get_fonte_ui('pequena')
        cor_texto = Tema.CORES['texto_principal']
        cor_fundo_balao = Tema.CORES['caixa_pergunta']
        cor_borda_balao = Tema.CORES['borda_destaque']
        padding_balao = 10
        largura_max_texto_dica = self.largura_tela * 0.55
        palavras_dica = texto_dica.split(' ')
        surfaces_linhas_dica = []
        linha_atual_str = ""
        maior_largura_linha_dica = 0
        altura_total_texto_dica = 0
        espacamento_entre_linhas_dica = 3
        for palavra in palavras_dica:
            linha_teste_str = linha_atual_str + palavra + " "
            surface_teste = fonte_dica.render(linha_teste_str, True, cor_texto)
            if surface_teste.get_width() <= largura_max_texto_dica:
                linha_atual_str = linha_teste_str
            else:
                surface_linha_final = fonte_dica.render(linha_atual_str.strip(), True, cor_texto)
                surfaces_linhas_dica.append(surface_linha_final)
                maior_largura_linha_dica = max(maior_largura_linha_dica, surface_linha_final.get_width())
                altura_total_texto_dica += surface_linha_final.get_height() + espacamento_entre_linhas_dica
                linha_atual_str = palavra + " "
        if linha_atual_str.strip():
            surface_linha_final = fonte_dica.render(linha_atual_str.strip(), True, cor_texto)
            surfaces_linhas_dica.append(surface_linha_final)
            maior_largura_linha_dica = max(maior_largura_linha_dica, surface_linha_final.get_width())
            altura_total_texto_dica += surface_linha_final.get_height()
        elif surfaces_linhas_dica:
             altura_total_texto_dica -= espacamento_entre_linhas_dica
        largura_total_balao = maior_largura_linha_dica + 2 * padding_balao
        altura_total_balao = altura_total_texto_dica + 2 * padding_balao
        x_balao = rect_botao_dica_referencia.centerx - largura_total_balao // 2
        x_balao = max(10, min(x_balao, self.largura_tela - largura_total_balao - 10)) 
        y_balao = rect_botao_dica_referencia.top - altura_total_balao - 10 
        rect_balao_dica = pygame.Rect(x_balao, y_balao, largura_total_balao, altura_total_balao)
        pygame.draw.rect(tela, cor_fundo_balao, rect_balao_dica, border_radius=8)
        pygame.draw.rect(tela, cor_borda_balao, rect_balao_dica, 2, border_radius=8)
        y_texto_dica_atual = rect_balao_dica.y + padding_balao
        for i, surface_linha in enumerate(surfaces_linhas_dica):
            tela.blit(surface_linha, (rect_balao_dica.x + padding_balao, y_texto_dica_atual))
            y_texto_dica_atual += surface_linha.get_height()
            if i < len(surfaces_linhas_dica) -1:
                y_texto_dica_atual += espacamento_entre_linhas_dica

    def desenhar_popup_confirmacao(self, tela, lista_botoes_popup, texto_principal_popup="Confirmar?"):
        overlay_surface = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 180)) 
        tela.blit(overlay_surface, (0, 0))
        fonte_titulo_popup = self.get_fonte_ui('media')
        fonte_detalhes_popup = self.get_fonte_ui('pequena')
        cor_texto_popup = Tema.CORES['texto_principal']
        cor_fundo_caixa_popup = Tema.CORES['caixa_pergunta']
        cor_borda_caixa_popup = Tema.CORES['borda_destaque']
        textos_informativos_popup = [texto_principal_popup, "Atenção! Você só possui uma chance, se errar o jogo acaba!", "Confirme sua resposta!"]
        padding_caixa_popup = 25
        espaco_linhas_texto_popup = 8
        altura_botao_no_popup = lista_botoes_popup[0].rect.height if lista_botoes_popup else 50
        largura_botao_no_popup = lista_botoes_popup[0].rect.width if lista_botoes_popup else 150
        espaco_entre_botoes_horizontal = 20
        max_largura_texto_popup = 0
        altura_total_textos_popup = 0
        surface_texto_principal_popup = fonte_titulo_popup.render(textos_informativos_popup[0], True, cor_texto_popup)
        max_largura_texto_popup = max(max_largura_texto_popup, surface_texto_principal_popup.get_width())
        altura_total_textos_popup += surface_texto_principal_popup.get_height() + espaco_linhas_texto_popup
        for i in range(1, len(textos_informativos_popup)):
            texto_linha = textos_informativos_popup[i]
            if texto_linha.strip():
                surface_linha_popup = fonte_detalhes_popup.render(texto_linha, True, cor_texto_popup)
                max_largura_texto_popup = max(max_largura_texto_popup, surface_linha_popup.get_width())
                altura_total_textos_popup += surface_linha_popup.get_height() + espaco_linhas_texto_popup
            else: 
                altura_total_textos_popup += fonte_detalhes_popup.get_height() // 2 + espaco_linhas_texto_popup
        largura_total_botoes_popup = (len(lista_botoes_popup) * largura_botao_no_popup) + \
                                  ((len(lista_botoes_popup) -1) * espaco_entre_botoes_horizontal if len(lista_botoes_popup)>1 else 0)
        largura_caixa_popup = max(max_largura_texto_popup + 2 * padding_caixa_popup, 
                                  largura_total_botoes_popup + 2 * padding_caixa_popup, 
                                  self.largura_tela * 0.6)
        altura_caixa_popup = altura_total_textos_popup + altura_botao_no_popup + espaco_entre_botoes_horizontal + 2 * padding_caixa_popup
        x_caixa_popup = (self.largura_tela - largura_caixa_popup) // 2
        y_caixa_popup = (self.altura_tela - altura_caixa_popup) // 2
        rect_caixa_popup = pygame.Rect(x_caixa_popup, y_caixa_popup, largura_caixa_popup, altura_caixa_popup)
        pygame.draw.rect(tela, cor_fundo_caixa_popup, rect_caixa_popup, border_radius=12)
        pygame.draw.rect(tela, cor_borda_caixa_popup, rect_caixa_popup, 2, border_radius=12)
        y_texto_popup_atual = y_caixa_popup + padding_caixa_popup
        tela.blit(surface_texto_principal_popup, (x_caixa_popup + (largura_caixa_popup - surface_texto_principal_popup.get_width()) // 2, y_texto_popup_atual))
        y_texto_popup_atual += surface_texto_principal_popup.get_height() + espaco_linhas_texto_popup
        for i in range(1, len(textos_informativos_popup)):
            texto_linha = textos_informativos_popup[i]
            if texto_linha.strip():
                surface_linha_popup = fonte_detalhes_popup.render(texto_linha, True, cor_texto_popup)
                tela.blit(surface_linha_popup, (x_caixa_popup + (largura_caixa_popup - surface_linha_popup.get_width()) // 2, y_texto_popup_atual))
                y_texto_popup_atual += surface_linha_popup.get_height() + espaco_linhas_texto_popup
            else:
                y_texto_popup_atual += fonte_detalhes_popup.get_height() // 2 + espaco_linhas_texto_popup
        y_pos_botoes_popup = y_caixa_popup + altura_caixa_popup - padding_caixa_popup - altura_botao_no_popup
        x_inicio_botoes_popup = x_caixa_popup + (largura_caixa_popup - largura_total_botoes_popup) // 2
        for i, botao_popup in enumerate(lista_botoes_popup):
            botao_popup.rect.x = x_inicio_botoes_popup + i * (largura_botao_no_popup + espaco_entre_botoes_horizontal)
            botao_popup.rect.y = y_pos_botoes_popup
            botao_popup.desenhar(tela)

    def desenhar_tela_final(self, tela, pontuacao_final, lista_botoes_tela_final, texto_info_resposta_correta=None):
        overlay_surface = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 190))
        tela.blit(overlay_surface, (0, 0))
        fonte_titulo_final = self.get_fonte_ui('extra_grande')
        fonte_pontuacao = self.get_fonte_ui('grande')
        fonte_info_final = self.get_fonte_ui('media')
        cor_texto_geral = Tema.CORES['texto_claro']
        cor_texto_pontuacao_final = Tema.CORES['pontuacao']
        cor_texto_info_resposta = Tema.CORES['resposta_certa_texto']
        cor_fundo_caixa_final = Tema.CORES['caixa_pergunta']
        cor_borda_caixa_final = Tema.CORES['borda_destaque']
        surface_titulo_final = fonte_titulo_final.render("Fim de Jogo!", True, cor_texto_geral)
        surface_texto_pontuacao = fonte_pontuacao.render(f"Pontuação Final: R$ {pontuacao_final}", True, cor_texto_pontuacao_final)
        surfaces_info_resposta = []
        if texto_info_resposta_correta:
            texto_formatado_info = texto_info_resposta_correta
            if not texto_info_resposta_correta.startswith("Parabéns") and not texto_info_resposta_correta.startswith("Fim da rodada"):
                 texto_formatado_info = f"A resposta correta era: {texto_info_resposta_correta}"
            palavras_info_final = texto_formatado_info.split(' ')
            linha_atual_str = ""
            largura_max_info_final = self.largura_tela * 0.75
            for palavra in palavras_info_final:
                linha_teste_str = linha_atual_str + palavra + " "
                if fonte_info_final.render(linha_teste_str, True, cor_texto_info_resposta).get_width() <= largura_max_info_final:
                    linha_atual_str = linha_teste_str
                else:
                    surfaces_info_resposta.append(fonte_info_final.render(linha_atual_str.strip(), True, cor_texto_info_resposta))
                    linha_atual_str = palavra + " "
            if linha_atual_str.strip():
                surfaces_info_resposta.append(fonte_info_final.render(linha_atual_str.strip(), True, cor_texto_info_resposta))
        padding_caixa_final = 30
        espacamento_elementos_vertical = 20
        altura_total_botoes_finais = sum(b.rect.height for b in lista_botoes_tela_final) + \
                                  (len(lista_botoes_tela_final)-1)*espacamento_elementos_vertical if lista_botoes_tela_final else 0
        larguras_conteudo = [surface_titulo_final.get_width(), surface_texto_pontuacao.get_width()]
        if surfaces_info_resposta: larguras_conteudo.extend(s.get_width() for s in surfaces_info_resposta)
        if lista_botoes_tela_final: larguras_conteudo.extend(b.rect.width for b in lista_botoes_tela_final)
        largura_max_conteudo_interno = max(larguras_conteudo) if larguras_conteudo else self.largura_tela * 0.5
        altura_total_textos_internos = surface_titulo_final.get_height() + espacamento_elementos_vertical + \
                                      surface_texto_pontuacao.get_height()
        if surfaces_info_resposta:
            altura_total_textos_internos += espacamento_elementos_vertical + \
                                            sum(s.get_height() for s in surfaces_info_resposta) + \
                                            (len(surfaces_info_resposta)-1)*5
        largura_caixa_final = max(largura_max_conteudo_interno + 2 * padding_caixa_final, self.largura_tela * 0.6)
        altura_caixa_final = altura_total_textos_internos + espacamento_elementos_vertical + altura_total_botoes_finais + 2 * padding_caixa_final
        x_caixa_final = (self.largura_tela - largura_caixa_final) // 2
        y_caixa_final = (self.altura_tela - altura_caixa_final) // 2
        rect_caixa_final = pygame.Rect(x_caixa_final, y_caixa_final, largura_caixa_final, altura_caixa_final)
        pygame.draw.rect(tela, cor_fundo_caixa_final, rect_caixa_final, border_radius=15)
        pygame.draw.rect(tela, cor_borda_caixa_final, rect_caixa_final, 3, border_radius=15)
        y_elemento_atual = y_caixa_final + padding_caixa_final
        tela.blit(surface_titulo_final, (x_caixa_final + (largura_caixa_final - surface_titulo_final.get_width()) // 2, y_elemento_atual))
        y_elemento_atual += surface_titulo_final.get_height() + espacamento_elementos_vertical
        tela.blit(surface_texto_pontuacao, (x_caixa_final + (largura_caixa_final - surface_texto_pontuacao.get_width()) // 2, y_elemento_atual))
        y_elemento_atual += surface_texto_pontuacao.get_height() + espacamento_elementos_vertical
        if surfaces_info_resposta:
            for surface_info in surfaces_info_resposta:
                tela.blit(surface_info, (x_caixa_final + (largura_caixa_final - surface_info.get_width()) // 2, y_elemento_atual))
                y_elemento_atual += surface_info.get_height() + 5 
            y_elemento_atual += espacamento_elementos_vertical - 5 
        y_inicio_botoes_finais = y_caixa_final + altura_caixa_final - padding_caixa_final - altura_total_botoes_finais
        for i, botao_final in enumerate(lista_botoes_tela_final):
            botao_final.rect.centerx = rect_caixa_final.centerx
            if i == 0:
                botao_final.rect.y = y_inicio_botoes_finais
            else:
                botao_final.rect.y = lista_botoes_tela_final[i-1].rect.bottom + espacamento_elementos_vertical
            botao_final.desenhar(tela)

    def desenhar_notificacao_flutuante(self, tela):
        if not self.notificacao_ativa: return
        tempo_agora = pygame.time.get_ticks()
        if tempo_agora > self.notificacao_tempo_final:
            self.notificacao_ativa = False
            return
        tempo_restante = self.notificacao_tempo_final - tempo_agora
        tempo_decorrido = 2000 - tempo_restante 
        opacidade = 0
        duracao_fade_anim = 500 
        if tempo_decorrido < duracao_fade_anim: 
             opacidade = int(255 * (tempo_decorrido / duracao_fade_anim))
        elif tempo_restante < duracao_fade_anim: 
            opacidade = int(255 * (tempo_restante / duracao_fade_anim))
        else: 
            opacidade = 255
        opacidade = max(0, min(255, opacidade))
        fonte_notif = self.get_fonte_ui('media')
        surface_texto_notif = fonte_notif.render(self.notificacao_texto, True, Tema.CORES['texto_claro'])
        
        padding_notif = 15
        largura_notif = surface_texto_notif.get_width() + 2 * padding_notif
        altura_notif = surface_texto_notif.get_height() + 2 * padding_notif
        surface_fundo_notif = pygame.Surface((largura_notif, altura_notif), pygame.SRCALPHA)
        
        cor_rgb_base_fundo = self.notificacao_cor_fundo[:3] 
        alfa_cor_base = self.notificacao_cor_fundo[3] if len(self.notificacao_cor_fundo) > 3 else 220
        alfa_final_com_fade = int(alfa_cor_base * (opacidade / 255.0))

        surface_fundo_notif.fill(cor_rgb_base_fundo + (alfa_final_com_fade,))
        surface_texto_notif.set_alpha(opacidade)
        surface_fundo_notif.blit(surface_texto_notif, (padding_notif, padding_notif))

        x_pos_notif = (self.largura_tela - largura_notif) // 2
        y_pos_notif = 20 
        tela.blit(surface_fundo_notif, (x_pos_notif, y_pos_notif))

    def exibir_notificacao(self, texto, tipo_notificacao="info", duracao_ms=2000):
        self.notificacao_texto = texto
        if tipo_notificacao == "sucesso": self.notificacao_cor_fundo = Tema.CORES['notificacao_sucesso_fundo']
        elif tipo_notificacao == "erro": self.notificacao_cor_fundo = Tema.CORES['notificacao_erro_fundo']
        else: self.notificacao_cor_fundo = Tema.CORES['notificacao_info_fundo']
        self.notificacao_tempo_final = pygame.time.get_ticks() + duracao_ms
        self.notificacao_ativa = True

    def desenhar_info_pontuacao(self, tela, valor_pontuacao):
        fonte_pontuacao = self.get_fonte_ui('media')
        surface_texto_pontuacao = fonte_pontuacao.render(f"Sua pontuação: R$ {valor_pontuacao}", True, Tema.CORES['pontuacao'])
        nova_pos_x = 270
        nova_pos_y = 10
        tela.blit(surface_texto_pontuacao, (self.largura_tela -  nova_pos_x, nova_pos_y))