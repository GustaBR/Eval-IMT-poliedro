import mysql.connector  # type: ignore
from rank.jogador import Jogador

class Database:
    @staticmethod
    def carregar_dados():
        try:
            conexao = mysql.connector.connect(
                host="jogomilhao-pi11semestre.l.aivencloud.com",
                user="avnadmin",
                port="25159",
                password="AVNS_2oEh5hU00BYuzgIhTXP",
                database="jogomilhao"
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT nomeAluno, pontuacao FROM aluno ORDER BY pontuacao DESC LIMIT 100")
            dados = cursor.fetchall()
            cursor.close()
            conexao.close()
            return [Jogador(nome, pontuacao) for nome, pontuacao in dados]
        except mysql.connector.Error as err:
            print("Erro ao conectar ao banco de dados:", err)
            return []