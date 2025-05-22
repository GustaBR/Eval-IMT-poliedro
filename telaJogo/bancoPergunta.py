import mysql.connector
from pergunta import PerguntaTela

class BancoDePerguntasTela:
    def __init__(self):
        self.perguntas = self.carregar_perguntas_do_banco()
        self.indice_atual = 0

    def carregar_perguntas_do_banco(self):
        perguntas = []
        
        try:
            with mysql.connector.connect(
                host="jogomilhao-pi11semestre.l.aivencloud.com",
                user="avnadmin",
                port="25159",
                password="AVNS_2oEh5hU00BYuzgIhTXP",
                database="jogomilhao"
            ) as conexao:
                
                with conexao.cursor(dictionary=True) as cursor:
                    # Busca todas as questões
                    cursor.execute("SELECT idQuest, enuncQuest FROM questoes")
                    questoes = cursor.fetchall()

                    for questao in questoes:
                        # Busca alternativas para a questão atual
                        cursor.execute(
                            "SELECT resposta, correta FROM alternativas WHERE idQuest = %s ORDER BY true",
                            (questao["idQuest"],)
                        )
                       
                        alternativas = []
                        indice_correto = 0
                        for i, alt in enumerate(cursor.fetchall()):
                            alternativas.append(alt["resposta"])
                            if alt["correta"]:
                                indice_correto = i
                
                        # Busca dica para a questão atual
                        cursor.execute(
                            "SELECT texto FROM dicas WHERE idQuest = %s LIMIT 1",
                            (questao["idQuest"],)
                        )
                
                        dica = cursor.fetchone()
                        texto_dica = dica["texto"] if dica else ""

                        # Cria objeto Pergunta
                        perguntas.append(PerguntaTela(
                            questao["enuncQuest"],
                            alternativas,
                            indice_correto,
                            texto_dica
                        ))

        except mysql.connector.Error as err:
            print(f"Erro de banco de dados: {err}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

        return perguntas

    def obter_pergunta_atual(self):
        if self.indice_atual < len(self.perguntas):
            return self.perguntas[self.indice_atual]
        return None

    def avancar(self):
        self.indice_atual += 1

    def pular(self):
        if self.indice_atual < len(self.perguntas) - 1:
            self.indice_atual += 1
            return True
        return False

    def jogo_acabou(self):
        return self.indice_atual >= len(self.perguntas)

    def reiniciar(self):
        self.indice_atual = 0