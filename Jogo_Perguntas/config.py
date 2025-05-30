import os

# --- Dados de Acesso ao Banco de Dados ---
CONFIGURACAO_BANCO_DADOS = {
    'host': 'jogomilhao-pi11semestre.l.aivencloud.com',
    'port': 25159,
    'user': 'avnadmin',
    'password': 'AVNS_2oEh5hU00BYuzgIhTXP',
    'database': 'jogomilhao',
}

QUADROS_POR_SEGUNDO = 60
LARGURA_TELA = 800
ALTURA_TELA = 600
DIRETORIO_ASSETS = "assets" # Pasta para fontes, imagens, etc.
NOME_ARQUIVO_FONTE_PRINCIPAL = 'Roboto-Regular.ttf'
CAMINHO_IMAGEM_FUNDO_PERSONALIZADA = os.path.join(DIRETORIO_ASSETS, "fundo.jpg")
