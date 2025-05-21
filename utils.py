import pygame
import os

def lerp(a, b, t):
    return a + (b - a) * t

def mesclar_cores(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

def carregar_icone(caminho, tamanho):
    if os.path.isfile(caminho):
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.smoothscale(img, (tamanho, tamanho))
    return None