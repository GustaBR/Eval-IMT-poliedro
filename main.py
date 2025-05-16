import pygame
pygame.init()

import config
from menu import Menu


# Criando a janela
tela = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))

# Definindo título e ícone da janela
pygame.display.set_caption("Eval")
'''As 2 linhas abaixo são temporárias e servem para prevenir que o programa
não funcione devido à inexistência do arquivo "nome_do_arquivo.extensao"'''
icone_foi_criado = False
if icone_foi_criado:
    icone = pygame.image.load("nome_do_arquivo.extensao")
    pygame.display.set_icon(icone)

config.criar_fontes()
menu = Menu()
cronometro = pygame.time.Clock()


# Eventos da janela
execucao = True
while execucao:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            execucao = False
    
    menu.atualizar()
    menu.exibir(tela)

    pygame.display.flip()
    cronometro.tick(60)