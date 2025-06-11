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

    @pontuacao.setter
    def pontuacao(self, nova_pontuacao):
        self.__pontuacao = nova_pontuacao    

    
    def pontuacao_formatada(self):
        unidades = {
        12: "T",
        9: "B",
        6: "M",
        3: "K",
    }

        valor = self.pontuacao

        for exp, sufixo in sorted(unidades.items(), reverse=True):
            if valor >= 10 ** exp:
                return f"{valor / 10**exp:.1f}{sufixo}"

        return str(valor)


class Professor(Usuario):
    def __init__(self, usuario, senha):
        super().__init__(usuario, senha)
        self.tipo = "Professor"

