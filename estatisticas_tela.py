import pygame
import config

class EstatisticasTela:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador


    def carregar_estatisticas(self, usuario):
        estatisticas = {
            "Pontuação": usuario.pontuacao
        }
        return estatisticas
    

    def checar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            from menu_tela_aluno import MenuTelaAluno
            self.gerenciador.trocar_tela(MenuTelaAluno)


    def atualizar(self):
        ...


    def exibir(self, janela):
        janela.fill(config.BRANCO_FUNDO)
        
        estatisticas = self.carregar_estatisticas(self.gerenciador.usuario)
        
        # Fonte para exibição do texto
        fonte = config.fonte_botao
        
        for i, (estatistica, valor) in enumerate(estatisticas.items()):
            texto = fonte.render(f"{estatistica}: {valor}", True, config.PRETO)
            texto_rect = texto.get_rect()
            texto_rect.center = (config.LARGURA_JANELA//2, int((50 + i * (texto.get_height() + 20)) * config.ALTURA_JANELA / 768))
            janela.blit(texto, texto_rect)
                    
