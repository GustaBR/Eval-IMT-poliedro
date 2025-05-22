import pygame

class TipoUsuarioTela:
    def __init__(self, aluno_rect, prof_rect, fonte, cores):
        self.tipo = "aluno"
        self.rect_aluno = aluno_rect
        self.rect_prof = prof_rect
        self.fonte = fonte
        self.cores = cores

    def desenhar(self, surface):
        cor_aluno = self.cores['selecao'] if self.tipo == "aluno" else self.cores['botao']
        cor_prof = self.cores['selecao'] if self.tipo == "professor" else self.cores['botao']

        pygame.draw.rect(surface, cor_aluno, self.rect_aluno, border_radius=15)
        pygame.draw.rect(surface, cor_prof, self.rect_prof, border_radius=15)

        aluno_text = self.fonte.render("Aluno", True, (255,255,255))
        prof_text = self.fonte.render("Professor", True, (255,255,255))

        surface.blit(aluno_text, aluno_text.get_rect(center=self.rect_aluno.center))
        surface.blit(prof_text, prof_text.get_rect(center=self.rect_prof.center))

    def selecionar(self, pos):
        if self.rect_aluno.collidepoint(pos):
            self.tipo = "aluno"
            return True
        elif self.rect_prof.collidepoint(pos):
            self.tipo = "professor"
            return True
        return False
