from cadastrar_perguntas.dropdown import *

class CaixaTextoComPrefixo:
    def __init__(self, x, y, w, h, fonte, dica_texto="", prefixo=""):
        self.retangulo = pygame.Rect(x, y, w, h)
        self.fonte = fonte
        self.dica_texto = dica_texto
        self.ativo = False
        self.texto = ""
        self.cursor_pos = 0
        self.margem = 10
        self.rolagem_x = 0
        self.cursor_visivel = True
        self.cursor_timer = 0
        self.backspace_pressionado = False
        self.backspace_timer = 0
        self.atraso_inicial_backspace = 400
        self.intervalo_backspace = 30
        self.prefixo = prefixo
        self.prefixo_surf, self.prefixo_ret = fonte.render(prefixo, COR_TEXTO_NORMAL)
        self.inicio_texto_x = self.margem + self.prefixo_ret.width + 8

    def desenhar_sombra(superficie, retangulo, deslocamento=3, raio_borda=10):
        ret_sombra = pygame.Rect(retangulo.x + deslocamento, retangulo.y + deslocamento, retangulo.width, retangulo.height)
        pygame.draw.rect(superficie, COR_SOMBRA, ret_sombra, border_radius=raio_borda)

    def obter_texto(self):
        return self.texto

    def definir_texto(self, texto):
        self.texto = texto
        self.cursor_pos = len(texto)

    def _executar_backspace(self):
        if self.cursor_pos > 0:
            self.texto = self.texto[:self.cursor_pos - 1] + self.texto[self.cursor_pos:]
            self.cursor_pos -= 1

    def tratar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self.ativo = self.retangulo.collidepoint(evento.pos)
        if self.ativo and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE: self.backspace_pressionado = True; self.backspace_timer = 0; self._executar_backspace()
            elif evento.key == pygame.K_LEFT: self.cursor_pos = max(0, self.cursor_pos - 1)
            elif evento.key == pygame.K_RIGHT: self.cursor_pos = min(len(self.texto), self.cursor_pos + 1)
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER): self.ativo = False
            elif evento.unicode.isprintable():
                self.texto = self.texto[:self.cursor_pos] + evento.unicode + self.texto[self.cursor_pos:]; self.cursor_pos += len(evento.unicode)
        if evento.type == pygame.KEYUP and evento.key == pygame.K_BACKSPACE: self.backspace_pressionado = False
    def atualizar(self, dt):
        if self.ativo:
            self.cursor_timer = (self.cursor_timer + dt) % 1000; self.cursor_visivel = self.cursor_timer < 500
            if self.backspace_pressionado:
                self.backspace_timer += dt
                if self.backspace_timer > self.atraso_inicial_backspace:
                    tempo_desde = self.backspace_timer - self.atraso_inicial_backspace
                    if int(tempo_desde/self.intervalo_backspace) > int((tempo_desde-dt)/self.intervalo_backspace): self._executar_backspace()
        else: self.cursor_visivel = False
    def desenhar(self, superficie):
        desenhar_sombra(superficie, self.retangulo); pygame.draw.rect(superficie, COR_BRANCO, self.retangulo, border_radius=8)
        pygame.draw.rect(superficie, COR_BORDA_ATIVA if self.ativo else COR_BORDA, self.retangulo, 2, border_radius=8)
        largura_visivel = self.retangulo.width - self.margem - self.inicio_texto_x
        surf_texto, ret_texto = self.fonte.render(self.texto, COR_TEXTO_NORMAL)
        cursor_x_abs = self.fonte.get_rect(self.texto[:self.cursor_pos]).width
        if cursor_x_abs - self.rolagem_x > largura_visivel: self.rolagem_x = cursor_x_abs - largura_visivel
        if cursor_x_abs - self.rolagem_x < 0: self.rolagem_x = cursor_x_abs
        area_texto = self.retangulo.inflate(-self.inicio_texto_x - self.margem, -self.margem*2); area_texto.x = self.retangulo.x + self.inicio_texto_x
        if not self.texto and not self.ativo:
            self.fonte.render_to(superficie, (area_texto.x, self.retangulo.centery - self.fonte.get_sized_height()//2), self.dica_texto, COR_TEXTO_DICA)
        else:
            clip_original = superficie.get_clip(); superficie.set_clip(area_texto)
            superficie.blit(surf_texto, (area_texto.x - self.rolagem_x, self.retangulo.centery - ret_texto.height//2)); superficie.set_clip(clip_original)
        superficie.blit(self.prefixo_surf, (self.retangulo.x + self.margem, self.retangulo.centery - self.prefixo_ret.height // 2))
        if self.ativo and self.cursor_visivel:
            cursor_final_x = area_texto.x + cursor_x_abs - self.rolagem_x; h = self.fonte.get_sized_height() * 0.9; y_inicio = self.retangulo.centery - h/2
            pygame.draw.line(superficie, COR_TEXTO_NORMAL, (cursor_final_x, y_inicio), (cursor_final_x, y_inicio + h), 2)

class CaixaTextoModerna:
    def __init__(self, x, y, w, h, fonte, dica_texto=""):
        self.retangulo = pygame.Rect(x, y, w, h)
        self.fonte = fonte
        self.dica_texto = dica_texto
        self.ativo = False
        self.linhas = [""]
        self.pos_cursor = [0, 0]
        self.altura_linha = fonte.get_sized_height() * 1.5
        self.margem = 10
        pos_cursor_inicial = self._obter_pos_canvas_cursor()
        self.pos_cursor_canvas = pygame.Vector2(pos_cursor_inicial)
        self.pos_cursor_alvo_canvas = pygame.Vector2(pos_cursor_inicial)
        self.rolagem_y = 0.0
        self.rolagem_y_alvo = 0.0
        self.cursor_visivel = True
        self.cursor_timer = 0
        self.backspace_pressionado = False
        self.backspace_timer = 0
        self.atraso_inicial_backspace = 400
        self.intervalo_backspace = 30

    def obter_texto(self): return "\n".join(self.linhas)
    def definir_texto(self, texto):
        self.linhas = texto.split('\n') if texto else [""]; self.pos_cursor = [len(self.linhas) - 1, len(self.linhas[-1])]; self._atualizar_alvo_cursor()

    def _executar_backspace(self):
        linha, col = self.pos_cursor
        if col > 0: self.linhas[linha] = self.linhas[linha][:col-1] + self.linhas[linha][col:]; self.pos_cursor[1] -= 1
        elif linha > 0:
            tam_linha_ant = len(self.linhas[linha-1]); self.linhas[linha-1] += self.linhas.pop(linha); self.pos_cursor = [linha - 1, tam_linha_ant]
        self._atualizar_alvo_cursor()

    def _obter_pos_canvas_cursor(self):
        return (self.fonte.get_rect(self.linhas[self.pos_cursor[0]][:self.pos_cursor[1]]).width, self.pos_cursor[0] * self.altura_linha)

    def _atualizar_alvo_cursor(self):
        self.pos_cursor_alvo_canvas.update(self._obter_pos_canvas_cursor()); self._garantir_cursor_visivel_rolagem()

    def _garantir_cursor_visivel_rolagem(self):
        altura_area_visivel = self.retangulo.height - 2 * self.margem; y_cursor_canvas = self.pos_cursor_alvo_canvas.y
        if y_cursor_canvas < self.rolagem_y_alvo: self.rolagem_y_alvo = y_cursor_canvas
        if y_cursor_canvas + self.altura_linha > self.rolagem_y_alvo + altura_area_visivel: self.rolagem_y_alvo = y_cursor_canvas + self.altura_linha - altura_area_visivel

    def _mover_cursor_para_mouse(self, pos_mouse):
        x_canvas = pos_mouse[0] - self.retangulo.x - self.margem; y_canvas = pos_mouse[1] - self.retangulo.y - self.margem + self.rolagem_y
        linha_idx = max(0, min(len(self.linhas) - 1, int(y_canvas / self.altura_linha))); self.pos_cursor[0] = linha_idx
        texto_linha = self.linhas[linha_idx]; min_dist, melhor_col = float('inf'), 0
        for i in range(len(texto_linha) + 1):
            dist = abs(x_canvas - self.fonte.get_rect(texto_linha[:i]).width)
            if dist < min_dist: min_dist, melhor_col = dist, i
        self.pos_cursor[1] = melhor_col; self._atualizar_alvo_cursor()

    def tratar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self.ativo = self.retangulo.collidepoint(evento.pos)
            if self.ativo: self._mover_cursor_para_mouse(evento.pos)
        if not self.ativo: return
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE: self.backspace_pressionado = True; self.backspace_timer = 0; self._executar_backspace()
            elif evento.key == pygame.K_RETURN:
                linha, col = self.pos_cursor; self.linhas[linha], texto_restante = self.linhas[linha][:col], self.linhas[linha][col:]
                self.linhas.insert(linha + 1, texto_restante); self.pos_cursor = [linha + 1, 0]; self._atualizar_alvo_cursor()
            elif evento.key == pygame.K_LEFT:
                if self.pos_cursor[1]>0: self.pos_cursor[1]-=1
                elif self.pos_cursor[0]>0: self.pos_cursor=[self.pos_cursor[0]-1,len(self.linhas[self.pos_cursor[0]-1])]
                self._atualizar_alvo_cursor()
            elif evento.key == pygame.K_RIGHT:
                if self.pos_cursor[1]<len(self.linhas[self.pos_cursor[0]]):self.pos_cursor[1]+=1
                elif self.pos_cursor[0]<len(self.linhas)-1:self.pos_cursor=[self.pos_cursor[0]+1,0]
                self._atualizar_alvo_cursor()
            elif evento.key == pygame.K_UP:
                if self.pos_cursor[0]>0:self.pos_cursor[0]-=1;self.pos_cursor[1]=min(self.pos_cursor[1],len(self.linhas[self.pos_cursor[0]]))
                self._atualizar_alvo_cursor()
            elif evento.key == pygame.K_DOWN:
                if self.pos_cursor[0]<len(self.linhas)-1:self.pos_cursor[0]+=1;self.pos_cursor[1]=min(self.pos_cursor[1],len(self.linhas[self.pos_cursor[0]]))
                self._atualizar_alvo_cursor()
            elif evento.unicode.isprintable():
                linha,col=self.pos_cursor;self.linhas[linha]=self.linhas[linha][:col]+evento.unicode+self.linhas[linha][col:];self.pos_cursor[1]+=len(evento.unicode);self._atualizar_alvo_cursor()
        if evento.type==pygame.KEYUP and evento.key==pygame.K_BACKSPACE:self.backspace_pressionado=False

    def atualizar(self, dt):
        fator_interp = 1 - math.exp(-25 * dt / 1000)
        self.rolagem_y += (self.rolagem_y_alvo - self.rolagem_y) * fator_interp
        self.pos_cursor_canvas = self.pos_cursor_canvas.lerp(self.pos_cursor_alvo_canvas, fator_interp)
        if self.ativo:
            self.cursor_timer = (self.cursor_timer + dt) % 1000; self.cursor_visivel = self.cursor_timer < 500
            if self.backspace_pressionado:
                self.backspace_timer += dt
                if self.backspace_timer > self.atraso_inicial_backspace:
                    tempo_desde=self.backspace_timer-self.atraso_inicial_backspace
                    if int(tempo_desde/self.intervalo_backspace)>int((tempo_desde-dt)/self.intervalo_backspace):self._executar_backspace()
        else: self.cursor_visivel = False

    def desenhar(self, superficie):
        desenhar_sombra(superficie, self.retangulo); pygame.draw.rect(superficie, COR_BRANCO, self.retangulo, border_radius=8)
        pygame.draw.rect(superficie, COR_BORDA_ATIVA if self.ativo else COR_BORDA, self.retangulo, 2, border_radius=8)
        area_recorte=self.retangulo.inflate(-self.margem*2,-self.margem*2);clip_original=superficie.get_clip();superficie.set_clip(area_recorte)
        ponto_origem_tela=pygame.Vector2(self.retangulo.x+self.margem,self.retangulo.y+self.margem)
        if not self.obter_texto() and not self.ativo:
            y_centralizado=ponto_origem_tela.y+(self.altura_linha-self.fonte.get_sized_height())/2
            self.fonte.render_to(superficie,(ponto_origem_tela.x,y_centralizado),self.dica_texto,COR_TEXTO_DICA)
        else:
            for i,linha in enumerate(self.linhas):
                y_centralizado=(self.altura_linha-self.fonte.get_rect(linha).height)/2
                pos_tela=ponto_origem_tela+pygame.Vector2(0,i*self.altura_linha-self.rolagem_y+y_centralizado)
                self.fonte.render_to(superficie,pos_tela,linha,COR_TEXTO_NORMAL)
            if self.ativo and self.cursor_visivel:
                pos_cursor_tela=ponto_origem_tela+self.pos_cursor_canvas-pygame.Vector2(0,self.rolagem_y)
                y_inicio_cursor=pos_cursor_tela.y+(self.altura_linha-self.fonte.get_sized_height()*0.9)/2
                pygame.draw.line(superficie,COR_TEXTO_NORMAL,(pos_cursor_tela.x,y_inicio_cursor),(pos_cursor_tela.x,y_inicio_cursor+self.fonte.get_sized_height()*0.9),2)
        superficie.set_clip(clip_original)