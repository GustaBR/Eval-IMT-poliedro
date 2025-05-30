import pygame

class TemaTela:
    CORES = {
        'fundo': (46, 154, 166),
        'texto': (0, 0, 0),
        'botao_normal': (0, 128, 255),
        'botao_dica': (255, 165, 0),
        'botao_eliminar': (238, 30, 83),
        'botao_pular': (82, 205, 201),
        'botao_confirmar': (0, 255, 0),
        'botao_cancelar': (255, 0, 0),
        'botao_reiniciar': (0, 200, 0),
        'botao_sair': (200, 0, 0),
        'texto_claro': (255, 255, 255),
        'caixa_pergunta': (195, 63, 63),
        'resposta_eliminada': (100, 100, 100, 180),
        'borda': (0, 0, 0),
        'pontuacao': (0, 180, 0),
        'resposta_certa': (0, 100, 0),
        'botao_desabilitado': (150, 150, 150) # NOVA COR ADICIONADA
    }

    FONTES = {
        'pequena': lambda a: int(a * 0.03),
        'media': lambda a: int(a * 0.04),
        'grande': lambda a: int(a * 0.05),
        'extra_grande': lambda a: int(a * 0.08)
    }

    @staticmethod
    def criar_fonte(tamanho_func, altura_tela):
        return pygame.font.Font(None, tamanho_func(altura_tela))