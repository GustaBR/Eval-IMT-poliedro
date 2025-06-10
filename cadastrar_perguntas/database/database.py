import mysql.connector
from cadastrar_perguntas.config import CONFIG_BD

def obter_conexao_bd():
    """Tenta criar e retornar uma conexão com o banco. Lança exceção em caso de erro."""
    try:
        conexao = mysql.connector.connect(**CONFIG_BD)
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro de Conexão com o Banco de Dados: {erro}")
        raise # Lança a exceção para ser tratada para quem chamou ela

def buscar_materias_bd():
    """Busca e retorna um dicionário de matérias. Lança exceção em caso de erro."""
    conexao = None
    try:
        conexao = obter_conexao_bd()
        materias = {}
        cursor = conexao.cursor()
        cursor.execute("SELECT idMateria, nomeMateria FROM materia ORDER BY nomeMateria")
        resultado = cursor.fetchall()
        materias = {linha[1]: linha[0] for linha in resultado}
        return materias
    except mysql.connector.Error as erro:
        print(f"Erro de SQL ao buscar matérias: {erro}")
        raise
    finally:
        if conexao and conexao.is_connected():
            conexao.close()