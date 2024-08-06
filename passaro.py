from desenhavel import Desenhavel
from imgs import IMAGENS_PASSARO
import pygame

class Passaro(Desenhavel):
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._angulo = 0
        self._velocidade = 0
        self._altura = self._y
        self._tempo = 0
        self._contagem_imagem = 0
        self._imagem = self.IMGS[0]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def imagem(self):
        return self._imagem

    @imagem.setter
    def imagem(self, value):
        self._imagem = value

    @property
    def altura(self):
        return self._altura

    @altura.setter
    def altura(self, value):
        self._altura = value

    @property
    def angulo(self):
        return self._angulo

    @angulo.setter
    def angulo(self, value):
        self._angulo = value

    @property
    def tempo(self):
        return self._tempo

    @tempo.setter
    def tempo(self, value):
        self._tempo = value

    @property
    def contagem_imagem(self):
        return self._contagem_imagem

    @contagem_imagem.setter
    def contagem_imagem(self, value):
        self._contagem_imagem = value

    def pular(self):
        self._velocidade = -8.5
        self.tempo = 0
        self.altura = self._y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self._tempo**2) + self._velocidade * self.tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self._y < (self._altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self._imagem)