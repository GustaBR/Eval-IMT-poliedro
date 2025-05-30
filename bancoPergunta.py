
import mysql.connector
import random
from pergunta import PerguntaTela

class BancoDePerguntasTela:
    def __init__(self, materia=None):
        self.perguntas = self.carregar_perguntas_do_banco(materia)
        self.indice_atual = 0

    def carregar_perguntas_do_banco(self, materia=None):
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
                    if materia:
                        cursor.execute("""
                            SELECT idQuest, enuncQuest, difQuest
                            FROM questoes
                            WHERE nomeMateria = %s
                            ORDER BY FIELD(difQuest, 'F', 'M', 'D')
                        """, (materia,))
                    else:
                        cursor.execute("""
                            SELECT idQuest, enuncQuest, difQuest
                            FROM questoes
                            ORDER BY FIELD(difQuest, 'F', 'M', 'D')
                        """)
                    questoes = cursor.fetchall()

                    for questao in questoes:
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

                        cursor.execute(
                            "SELECT texto FROM dicas WHERE idQuest = %s LIMIT 1",
                            (questao["idQuest"],)
                        )
                        dica = cursor.fetchone()
                        texto_dica = dica["texto"] if dica else ""

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

    # NOVO MÉTODO
    def obter_materias_disponiveis(self):
        materias = []
        try:
            with mysql.connector.connect(
                host="jogomilhao-pi11semestre.l.aivencloud.com",
                user="avnadmin",
                port="25159",
                password="AVNS_2oEh5hU00BYuzgIhTXP",
                database="jogomilhao"
            ) as conexao:
                with conexao.cursor(dictionary=True) as cursor:
                    # Seleciona todas as matérias distintas da tabela questoes
                    cursor.execute("SELECT nomeMateria FROM questoes ORDER BY nomeMateria")
                    for row in cursor.fetchall():
                        materias.append(row["nomeMateria"])
        except mysql.connector.Error as err:
            print(f"Erro ao obter matérias do banco de dados: {err}")
        except Exception as e:
            print(f"Erro inesperado ao obter matérias: {e}")
        return materias

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
        random.shuffle(self.perguntas)
        self.indice_atual = 0