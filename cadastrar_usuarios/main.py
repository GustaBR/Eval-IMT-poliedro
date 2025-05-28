import pygame
pygame.init()  # inicializa pygame antes de importar o config, para evitar erro
from componentes.cadastrar_alunos_tela import CadastrarAlunosTela


def main():
    pygame.init()
    tela = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption("Cadastrar Usuário")

    gerenciador = None  # Se tiver um gerenciador de telas, aqui passa

    cadastro_tela = CadastrarAlunosTela(gerenciador)

    rodando = True
    clock = pygame.time.Clock()

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            else:
                cadastro_tela.gerenciar_eventos(evento)

        cadastro_tela.atualizar()
        cadastro_tela.desenhar(tela)

        clock.tick(60)
