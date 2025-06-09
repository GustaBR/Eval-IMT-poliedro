import pygame
import os
from jogo_perguntas.config import DIRETORIO_ASSETS, NOME_ARQUIVO_FONTE_PRINCIPAL

class Tema:
    CORES = {
        'fundo_padrao': (240, 240, 240),
        'texto_principal': (51, 51, 51),
        'texto_botao': (255, 255, 255),
        'texto_claro': (255, 255, 255),
        'texto_secundario': (100, 100, 100),
        'botao_normal': (0, 74, 141),
        'botao_hover': (0, 102, 192),
        'botao_desabilitado': (180, 180, 180),
        'borda_botao': (0, 50, 100),
        'botao_dica': (0, 102, 192),
        'botao_eliminar': (255, 102, 0),
        'botao_pular': (0, 102, 192),
        'botao_confirmar': (76, 175, 80),
        'botao_cancelar': (244, 67, 54),
        'botao_reiniciar': (0, 74, 141),
        'botao_sair': (100, 100, 100),
        'caixa_pergunta': (255, 255, 255),
        'borda_caixa': (204, 204, 204),
        'borda_destaque': (0, 74, 141),
        'resposta_eliminada_overlay': (200, 200, 200, 200),
        'pontuacao': (0, 74, 141),
        'resposta_certa_texto': (76, 175, 80),
        'notificacao_sucesso_fundo': (76, 175, 80, 220),
        'notificacao_erro_fundo': (244, 67, 54, 220),
        'notificacao_info_fundo': (0, 102, 192, 220),
        'botao_selecionado_fundo': (0, 102, 192, 100),
        'scroll_bar': (0, 102, 192),
        'scroll_trilha': (220, 220, 220),
    }
    
    nome_completo_fonte_primaria = None
    try:
        caminho_base_script = os.path.dirname(os.path.abspath(__file__))
        caminho_fonte_assets_script = os.path.join(caminho_base_script, DIRETORIO_ASSETS, NOME_ARQUIVO_FONTE_PRINCIPAL)
        caminho_fonte_assets_cwd = os.path.join(os.getcwd(), DIRETORIO_ASSETS, NOME_ARQUIVO_FONTE_PRINCIPAL)

        if os.path.exists(caminho_fonte_assets_script):
            nome_completo_fonte_primaria = caminho_fonte_assets_script
        elif os.path.exists(caminho_fonte_assets_cwd):
            nome_completo_fonte_primaria = caminho_fonte_assets_cwd
        else:
            print(f"AVISO: Fonte '{NOME_ARQUIVO_FONTE_PRINCIPAL}' não encontrada em '{caminho_fonte_assets_script}' ou '{caminho_fonte_assets_cwd}'. Usando fonte padrão do Pygame.")
    except NameError:
        caminho_fonte_assets_cwd = os.path.join(os.getcwd(), DIRETORIO_ASSETS, NOME_ARQUIVO_FONTE_PRINCIPAL)
        if os.path.exists(caminho_fonte_assets_cwd):
            nome_completo_fonte_primaria = caminho_fonte_assets_cwd
        else:
            print(f"AVISO: Fonte '{NOME_ARQUIVO_FONTE_PRINCIPAL}' não encontrada (tentativa via CWD). Usando fonte padrão do Pygame.")

    TAMANHOS_FONTE_RELATIVOS = {
        'pequena': lambda altura_tela: int(altura_tela * 0.025),
        'media': lambda altura_tela: int(altura_tela * 0.035),
        'grande': lambda altura_tela: int(altura_tela * 0.045),
        'extra_grande': lambda altura_tela: int(altura_tela * 0.055),
        'titulo': lambda altura_tela: int(altura_tela * 0.08)
    }
    FONTES_CACHE = {}

    @staticmethod
    def get_fonte(tipo_tamanho_str, altura_tela_referencia):
        tamanho_calculado = Tema.TAMANHOS_FONTE_RELATIVOS[tipo_tamanho_str](altura_tela_referencia)
        chave_cache = (Tema.nome_completo_fonte_primaria, tamanho_calculado)
        
        if chave_cache in Tema.FONTES_CACHE:
            return Tema.FONTES_CACHE[chave_cache]
        
        try:
            fonte = pygame.font.Font(Tema.nome_completo_fonte_primaria, tamanho_calculado)
        except pygame.error: 
            fonte = pygame.font.Font(None, tamanho_calculado) # back para fonte padrão
        
        Tema.FONTES_CACHE[chave_cache] = fonte
        return fonte