from menu_tela_aluno import MenuTelaAluno

class GerenciadorTelas:
    def __init__(self):
        self.telas = {}
        self.tela_atual = None

    def trocar_tela(self, classe_tela):
        if classe_tela not in self.telas:
            self.telas[classe_tela] = classe_tela(self)
        self.tela_atual = self.telas[classe_tela]

    def checar_eventos(self, evento):
        if self.tela_atual:
            self.tela_atual.checar_eventos(evento)

    def atualizar(self):
        if self.tela_atual:
            self.tela_atual.atualizar()

    def exibir(self, janela):
        if self.tela_atual:
            self.tela_atual.exibir(janela)
