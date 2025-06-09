import pygame
import pygame.freetype
import math
from config import *
from caixas_texto import CaixaTextoComPrefixo, CaixaTextoModerna

def desenhar_sombra(superficie, retangulo, deslocamento=3, raio_borda=10):
    ret_sombra = pygame.Rect(retangulo.x + deslocamento, retangulo.y + deslocamento, retangulo.width, retangulo.height)
    pygame.draw.rect(superficie, COR_SOMBRA, ret_sombra, border_radius=raio_borda)

class MenuSuspenso:
    def __init__(self, x, y, w, h, fonte, opcoes, texto_padrao):
        self.retangulo = pygame.Rect(x, y, w, h); self.fonte = fonte; self.opcoes = opcoes if opcoes else {}
        self.texto_padrao = texto_padrao; self.aberto = False; self.selecionada = None
        self.margem = 10; self.opcao_hover = -1
        self.retangulos_opcoes = [pygame.Rect(x, y + (i+1)*h, w, h) for i in range(len(self.opcoes))]
    def tratar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.retangulo.collidepoint(evento.pos): self.aberto = not self.aberto
            elif self.aberto:
                for i, r in enumerate(self.retangulos_opcoes):
                    if r.collidepoint(evento.pos): self.selecionada = list(self.opcoes.keys())[i]; self.aberto = False; break
                else: self.aberto = False
            else: self.aberto = False
        if evento.type == pygame.MOUSEMOTION and self.aberto:
            self.opcao_hover = -1
            for i, r in enumerate(self.retangulos_opcoes):
                if r.collidepoint(evento.pos): self.opcao_hover = i; break
    def desenhar(self, superficie):
        desenhar_sombra(superficie, self.retangulo); pygame.draw.rect(superficie, COR_BRANCO, self.retangulo, border_radius=10)
        pygame.draw.rect(superficie, COR_BORDA_ATIVA if self.aberto else COR_BORDA, self.retangulo, 2, border_radius=10)
        texto = self.selecionada if self.selecionada else self.texto_padrao
        cor = COR_TEXTO_NORMAL if self.selecionada else COR_TEXTO_DICA
        ts, tr = self.fonte.render(texto, cor)
        superficie.blit(ts, (self.retangulo.x + self.margem, self.retangulo.y + (self.retangulo.height - tr.height)//2))
        pontos_seta = [(self.retangulo.right - 20, self.retangulo.centery - 4), (self.retangulo.right - 10, self.retangulo.centery - 4), (self.retangulo.right - 15, self.retangulo.centery + 2)]
        pygame.draw.polygon(superficie, COR_TEXTO_NORMAL, pontos_seta)
        if self.aberto:
            for i, r in enumerate(self.retangulos_opcoes):
                desenhar_sombra(superficie, r, deslocamento=2); fundo = COR_MENU_HOVER if i == self.opcao_hover else COR_BRANCO
                pygame.draw.rect(superficie, fundo, r, border_radius=10); pygame.draw.rect(superficie, COR_BORDA, r, 1, border_radius=10)
                chave = list(self.opcoes.keys())[i]; ts, tr = self.fonte.render(chave, COR_TEXTO_NORMAL)
                superficie.blit(ts, (r.x + self.margem, r.y + (r.height - tr.height)//2))
    def atualizar(self, dt): pass

class GrupoRadio:
    def __init__(self, x, y, rotulos, fonte):
        self.rotulos, self.fonte, self.selecionado_idx, self.raio = rotulos, fonte, None, 10
        self.botoes = []
        deslocamento = x
        for indice, rotulo in enumerate(rotulos):
            surf_texto, ret_texto = fonte.render(rotulo, COR_TEXTO_NORMAL)
            retangulo = pygame.Rect(deslocamento, y - self.raio, self.raio*2 + 8 + ret_texto.width, self.raio*2)
            self.botoes.append({'cx': deslocamento + self.raio, 'cy': y, 'rotulo': rotulo, 'retangulo': retangulo, 'indice': indice})
            deslocamento += retangulo.width + 15
    def tratar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for botao in self.botoes:
                if botao['retangulo'].collidepoint(evento.pos): self.selecionado_idx = botao['indice']; break
    def desenhar(self, superficie):
        for botao in self.botoes:
            pygame.draw.circle(superficie, COR_BORDA, (botao['cx'], botao['cy']), self.raio, 2)
            if self.selecionado_idx == botao['indice']: pygame.draw.circle(superficie, COR_DESTAQUE, (botao['cx'], botao['cy']), self.raio - 4)
            self.fonte.render_to(superficie, (botao['cx'] + self.raio + 8, botao['cy'] - self.fonte.get_sized_height()//2), botao['rotulo'], COR_TEXTO_NORMAL)
    def atualizar(self, dt): pass

