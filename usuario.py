class Usuario:
    def __init__(self,  usuario, senha):
        self.usuario = usuario
        self.senha = senha


class Aluno(Usuario):
    def __init__(self, usuario, senha):
        super().__init__(senha, usuario)
        self.tipo = "Aluno"
        

class Professor(Usuario):
    def __init__(self, usuario, senha):
        super().__init__(usuario, senha)
        self.tipo = "Professor"

