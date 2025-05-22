import mysql.connector

# ========================================================================
# LOGIN DO BANCO DE DADOS (NAO DEIXAR VAZAR)
# ========================================================================

def conectar():
    return mysql.connector.connect(
        host="jogomilhao-pi11semestre.l.aivencloud.com",
        port=25159,
        user="avnadmin",
        password="AVNS_2oEh5hU00BYuzgIhTXP",
        database="jogomilhao"
    )

# ========================================================================
# LOGIN DO BANCO DE DADOS (NAO DEIXAR VAZAR)
# ========================================================================