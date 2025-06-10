class Usuario:
    def __init__(self, id, nome):
        self.__id = id
        self.__nome = nome

    @property
    def id(self):
        return self.__id
    
    @property
    def nome(self):
        return self.__nome


class Aluno(Usuario):
    def __init__(self, id, nome, pontuacao):
        super().__init__(id, nome)
        self.__pontuacao = pontuacao
        
    @property
    def pontuacao(self):
        return self.__pontuacao
    

class Professor(Usuario):
    def __init__(self, usuario, senha):
        super().__init__(usuario, senha)
        self.tipo = "Professor"

