import pygame

class CampoTexto:
    def __init__(self, rect, placeholder, max_len=50, aceita_caracteres=None):
        self.rect = rect
        self.texto = ""
        self.placeholder = placeholder
        self.max_len = max_len
        self.aceita_caracteres = aceita_caracteres
        self.ativo = False

    def inserir_caractere(self, char):
        if self.max_len and len(self.texto) >= self.max_len:
            return
        if self.aceita_caracteres is not None:
            if char.isalnum() or char in self.aceita_caracteres:
                self.texto += char
        else:
            if char.isalnum():
                self.texto += char


    def apagar_caractere(self):
        self.texto = self.texto[:-1]

    def renderizar(self, surface, font, cores, ativo):
        cor_borda = cores['ativo'] if ativo else cores['inativo']
        pygame.draw.rect(surface, (240, 240, 240), self.rect, border_radius=15)
        pygame.draw.rect(surface, cor_borda, self.rect, 3, border_radius=15)

        if self.texto:
            display_text = self.texto
        else:
            display_text = self.placeholder

        cor_texto = cores['ativo'] if self.texto else cores['placeholder']
        txt_surf = font.render(display_text, True, cor_texto)
        surface.blit(txt_surf, (self.rect.x + 15, self.rect.y + 15))