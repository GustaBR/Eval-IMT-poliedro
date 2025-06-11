import mysql.connector
import random
from jogo_perguntas.config import CONFIGURACAO_BANCO_DADOS
from jogo_perguntas.tema.elementos_cores import Pergunta

class GerenciadorBancoPerguntas:
    def __init__(self):
        self.conexao = None
        self._conectar_banco()

    def _conectar_banco(self):
        try:
            self.conexao = mysql.connector.connect(**CONFIGURACAO_BANCO_DADOS)
            if self.conexao.is_connected():
                print("Conexão com MySQL bem-sucedida.")
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao MySQL: {err}")
            self.conexao = None

    def desconectar_banco(self):
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
            print("Desconectado do MySQL.")

    def obter_materias_disponiveis(self):
        if not self.conexao or not self.conexao.is_connected():
            self._conectar_banco()
            if not self.conexao or not self.conexao.is_connected():
                print("Impossível conectar ao banco para obter matérias.")
                return []
        
        materias = []
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute("SELECT DISTINCT nomeMateria FROM materia ORDER BY nomeMateria") 
                materias = [linha[0] for linha in cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Erro ao obter matérias: {err}")
        return materias

    def obter_perguntas_por_materia(self, nome_materia, ids_perguntas_vistas=None, limite_perguntas=15):
        if not self.conexao or not self.conexao.is_connected():
            self._conectar_banco()
            if not self.conexao or not self.conexao.is_connected():
                print(f"Falha crítica: Impossível conectar ao banco para obter perguntas de '{nome_materia}'.")
                return []

        if ids_perguntas_vistas is None:
            ids_perguntas_vistas = set()

        perguntas_carregadas = []
        try:
            with self.conexao.cursor(dictionary=True) as cursor:
                query_base = "SELECT idQuest, enuncQuest, difQuest FROM questoes WHERE nomeMateria = %s"
                params = [nome_materia]

                if ids_perguntas_vistas: 
                    placeholders = ', '.join(['%s'] * len(ids_perguntas_vistas))
                    query_base += f" AND idQuest NOT IN ({placeholders})"
                    params.extend(list(ids_perguntas_vistas))
                
                query_final = query_base + " ORDER BY CASE difQuest WHEN 'F' THEN 1 WHEN 'M' THEN 2 WHEN 'D' THEN 3 ELSE 4 END, RAND() LIMIT %s"
                params.append(limite_perguntas)

                cursor.execute(query_final, tuple(params))
                dados_questoes_db = cursor.fetchall()

                if not dados_questoes_db: 
                    print(f"Nenhuma pergunta (nova) encontrada para '{nome_materia}' com os filtros aplicados.")
                    return []

                for questao_db in dados_questoes_db:
                    id_questao_atual = questao_db['idQuest']
                    enunciado_atual = questao_db['enuncQuest']

                    cursor.execute("SELECT resposta, correta FROM alternativas WHERE idQuest = %s", (id_questao_atual,))
                    alternativas_db = cursor.fetchall()

                    if not alternativas_db or len(alternativas_db) < 2: 
                        print(f"Aviso: Pergunta ID {id_questao_atual} tem poucas alternativas ou nenhuma. Pulando.")
                        continue
                    
                    textos_alternativas = []
                    indice_correta_original = -1
                    for i, alt_db in enumerate(alternativas_db):
                        textos_alternativas.append(alt_db['resposta'])
                        if alt_db['correta']: # Assume que 'correta' é um valor booleano 
                            if indice_correta_original != -1: 
                                print(f"Aviso: Múltiplas alternativas corretas marcadas para ID {id_questao_atual}. Usando a primeira encontrada.")
                            else: 
                                indice_correta_original = i
                    
                    if indice_correta_original == -1:
                        print(f"Aviso: Nenhuma alternativa correta marcada para ID {id_questao_atual}. Pulando.")
                        continue

                    alternativas_com_indices_originais = list(enumerate(textos_alternativas))
                    random.shuffle(alternativas_com_indices_originais) # Embaralha as alternativas
                    
                    alternativas_embaralhadas = [alt_tuple[1] for alt_tuple in alternativas_com_indices_originais]
                    indice_correta_novo = next(i for i, (idx_orig, _) in enumerate(alternativas_com_indices_originais) if idx_orig == indice_correta_original)

                    cursor.execute("SELECT texto FROM dicas WHERE idQuest = %s", (id_questao_atual,))
                    dica_db = cursor.fetchone()
                    texto_dica = dica_db['texto'] if dica_db and dica_db['texto'] else ""
                    
                    perguntas_carregadas.append(
                        Pergunta(id_questao_atual, enunciado_atual, alternativas_embaralhadas, indice_correta_novo, texto_dica)
                    )
        except mysql.connector.Error as err:
            print(f"Erro SQL ao obter perguntas para '{nome_materia}': {err}")
        return perguntas_carregadas
    
    
    def atualizar_pontuacao(self, usuario, pontuacao_a_adicionar):
        if not self.conexao or not self.conexao.is_connected():
            self._conectar_banco()
            if not self.conexao or not self.conexao.is_connected():
                print("Conexão falhou")

        nova_pontuacao = usuario.pontuacao + pontuacao_a_adicionar
        id_aluno = usuario.id
            
        try:
            with self.conexao.cursor() as cursor:
                cursor.execute("UPDATE aluno SET pontuacao = %s WHERE idAluno = %s", (nova_pontuacao, id_aluno)) 
            usuario.pontuacao = nova_pontuacao
            self.conexao.commit()
        except mysql.connector.Error as err:
            print(f"say smth")