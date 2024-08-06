from desenhavel import Desenhavel
from imgs import IMAGEM_CHAO
import random

class Chao(Desenhavel):
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self._y = y
        self._x1 = 0
        self._x2 = self.LARGURA

    @property
    def y(self):
        return self._y

    @property
    def x1(self):
        return self._x1

    @property
    def x2(self):
        return self._x2

    @x1.setter
    def x1(self, value: int):
        self._x1 -= value

    @x2.setter
    def x2(self, value: int):
        self._x2 -= value

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))