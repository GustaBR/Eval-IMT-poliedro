import mysql.connector
from mysql.connector import Error

class Database:
    host = "jogomilhao-pi11semestre.l.aivencloud.com"
    user = "avnadmin"
    port = 25159
    password = "AVNS_2oEh5hU00BYuzgIhTXP"
    database = "jogomilhao"

    @classmethod
    def connect(cls):
        try:
            connection = mysql.connector.connect(
                host=cls.host,
                user=cls.user,
                port=cls.port,
                password=cls.password,
                database=cls.database
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Erro na conexão: {e}")
        return None

    @classmethod
    def inserir_materia(cls, nome):
        connection = cls.connect()
        if connection is None:
            return False, "Erro ao conectar ao banco de dados."
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO materia (nomeMateria) VALUES (%s)"
            cursor.execute(sql, (nome,))
            connection.commit()
            cursor.close()
            connection.close()
            return True, f"Matéria '{nome}' cadastrada com sucesso!"
        except Error as e:
            return False, f"Erro ao cadastrar: {e}"

    @classmethod
    def buscar_materias(cls):
        connection = cls.connect()
        if connection is None:
            return [], "Erro ao conectar ao banco de dados."
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT nomeMateria FROM materia ORDER BY idMateria DESC")
            resultados = cursor.fetchall()
            cursor.close()
            connection.close()
            return [row[0] for row in resultados], None
        except Error as e:
            return [], f"Erro ao buscar matérias: {e}"

    @classmethod
    def excluir_materia(cls, nome):
        connection = cls.connect()
        if connection is None:
            return False, "Erro ao conectar ao banco de dados."
        try:
            cursor = connection.cursor()
            sql = "DELETE FROM materia WHERE nomeMateria = %s LIMIT 1"
            cursor.execute(sql, (nome,))
            if cursor.rowcount == 0:
                connection.close()
                return False, f"Matéria '{nome}' não encontrada."
            connection.commit()
            cursor.close()
            connection.close()
            return True, f"Matéria '{nome}' excluída com sucesso!"
        except Error as e:
            return False, f"Erro ao excluir: {e}"