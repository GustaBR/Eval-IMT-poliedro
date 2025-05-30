import pygame
import os
import traceback
from config import DIRETORIO_ASSETS, NOME_ARQUIVO_FONTE_PRINCIPAL
from funcionamento_jogo import GerenciadorJogo 

if __name__ == "__main__":
    if not os.path.exists(DIRETORIO_ASSETS):
        try:
            os.makedirs(DIRETORIO_ASSETS)
            print(f"Pasta '{DIRETORIO_ASSETS}' criada. ")
            print(f"Se for usar uma fonte personalizada, coloque '{NOME_ARQUIVO_FONTE_PRINCIPAL}' nela.")
            print(f"Se for usar uma imagem de fundo, defina CAMINHO_IMAGEM_FUNDO_PERSONALIZADA em config.py e coloque a imagem em '{DIRETORIO_ASSETS}'.")
        except OSError as e:
            print(f"Falha ao criar a pasta '{DIRETORIO_ASSETS}': {e}. Verifique as permissões do diretório.")

    jogo_instancia = None
    try:
        jogo_instancia = GerenciadorJogo()
        jogo_instancia.executar_loop_principal()
    except Exception as erro_fatal:
        print(f"ERRO FATAL E INESPERADO NO JOGO: {erro_fatal}")
        traceback.print_exc()
    finally:
       
        if pygame.get_init():
            pygame.quit()
        print("Jogo finalizado.")