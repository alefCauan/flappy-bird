from desenhavel import Desenhavel
from imgs import IMAGEM_CANO
import pygame
import random

class Cano(Desenhavel):
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self._x = x
        self._altura = 0
        self._pos_topo = 0
        self._pos_base = 0
        self._CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self._CANO_BASE = IMAGEM_CANO
        self._passou = False
        self.definir_altura()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def altura(self):
        return self._altura

    @altura.setter
    def altura(self, value):
        self._altura = value

    @property
    def pos_topo(self):
        return self._pos_topo

    @pos_topo.setter
    def pos_topo(self, value):
        self._pos_topo = value

    @property
    def pos_base(self):
        return self._pos_base

    @pos_base.setter
    def pos_base(self, value):
        self._pos_base = value

    @property
    def CANO_TOPO(self):
        return self._CANO_TOPO

    @CANO_TOPO.setter
    def CANO_TOPO(self, value):
        self._CANO_TOPO = value

    @property
    def CANO_BASE(self):
        return self._CANO_BASE

    @CANO_BASE.setter
    def CANO_BASE(self, value):
        self._CANO_BASE = value

    @property
    def passou(self):
        return self._passou

    @passou.setter
    def passou(self, value):
        self._passou = value

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False