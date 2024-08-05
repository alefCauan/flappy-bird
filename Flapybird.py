import tkinter as tk
from tkinter import messagebox, simpledialog
import pygame
import os
import random
import abc

TELA_LARGURA = 500
TELA_ALTURA = 800
os.chdir('/home/alef/Linguagens/Python/Testes/OOP/PrimeiroJogo/flappy-bird-')
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

class Usuario:
    def __init__(self, nome):
        self._nome = nome

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

class HistoricoPontuacao:
    def __init__(self):
        self._historico = []

    @property
    def historico(self):
        return self._historico

    def adicionar_pontuacao(self, usuario, pontuacao):
        print(pontuacao)
        self.historico.append((usuario, pontuacao))


class Desenhavel(abc.ABC):
    @abc.abstractmethod
    def desenhar(self, tela):
        pass
    @abc.abstractmethod
    def mover(self):
        pass

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

    @property
    def y(self):
        return self._y

    @property
    def imagem(self):
        return self._imagem

    @property
    def altura(self):
        return self._altura

    @property
    def angulo(self):
        return self._angulo

    def pular(self):
        self._velocidade = -8.5
        self._tempo = 0
        self._altura = self._y

    def mover(self):
        self._tempo += 1
        deslocamento = 1.5 * (self._tempo**2) + self._velocidade * self._tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self._y += deslocamento

        if deslocamento < 0 or self._y < (self._altura + 50):
            if self._angulo < self.ROTACAO_MAXIMA:
                self._angulo = self.ROTACAO_MAXIMA
        else:
            if self._angulo > -90:
                self._angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self._contagem_imagem += 1

        if self._contagem_imagem < self.TEMPO_ANIMACAO:
            self._imagem = self.IMGS[0]
        elif self._contagem_imagem < self.TEMPO_ANIMACAO*2:
            self._imagem = self.IMGS[1]
        elif self._contagem_imagem < self.TEMPO_ANIMACAO*3:
            self._imagem = self.IMGS[2]
        elif self._contagem_imagem < self.TEMPO_ANIMACAO*4:
            self._imagem = self.IMGS[1]
        elif self._contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self._imagem = self.IMGS[0]
            self._contagem_imagem = 0

        if self._angulo <= -80:
            self._imagem = self.IMGS[1]
            self._contagem_imagem = self.TEMPO_ANIMACAO*2

        imagem_rotacionada = pygame.transform.rotate(self._imagem, self._angulo)
        pos_centro_imagem = self._imagem.get_rect(topleft=(self._x, self._y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self._imagem)

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

    @property
    def passou(self):
        return self._passou

    @passou.setter
    def passou(self, value):
        self._passou = value

    def definir_altura(self):
        self._altura = random.randrange(50, 450)
        self._pos_topo = self._altura - self._CANO_TOPO.get_height()
        self._pos_base = self._altura + self.DISTANCIA

    def mover(self):
        self._x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self._CANO_TOPO, (self._x, self._pos_topo))
        tela.blit(self._CANO_BASE, (self._x, self._pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self._CANO_TOPO)
        base_mask = pygame.mask.from_surface(self._CANO_BASE)

        distancia_topo = (self._x - passaro.x, self._pos_topo - round(passaro.y))
        distancia_base = (self._x - passaro.x, self._pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

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

def desenhar_tela(tela, objetos, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for obj in objetos:
        obj.desenhar(tela)
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    pygame.display.update()

def main():
    root = tk.Tk()
    root.withdraw()

    nome_usuario = simpledialog.askstring("NEW PLAYER", "Qual é o seu nome?")

    if nome_usuario == None:
        usuario = Usuario("Player")
    else:
        usuario = Usuario(nome_usuario)

    historico = HistoricoPontuacao()
    
    while True:
        passaros = [Passaro(230, 350)]
        chao = Chao(730)
        canos = [Cano(700)]
        tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
        pontos = 0
        relogio = pygame.time.Clock()

        rodando = True
        while rodando:
            relogio.tick(30)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    root.destroy()
                    return
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

            for passaro in passaros:
                passaro.mover()
            chao.mover()

            adicionar_cano = False
            remover_canos = []
            for cano in canos:
                for i, passaro in enumerate(passaros):
                    if cano.colidir(passaro):
                        historico.adicionar_pontuacao(usuario, pontos)
                        messagebox.showinfo("Game Over", f"Game Over! Pontuação: {pontos}")
                        passaros.pop(i)
                        rodando = False
                    if not cano.passou and passaro.x > cano.x:
                        cano.passou = True
                        adicionar_cano = True
                cano.mover()
                if cano.x + cano._CANO_TOPO.get_width() < 0:
                    remover_canos.append(cano)

            if adicionar_cano:
                pontos += 1
                canos.append(Cano(600))
            for cano in remover_canos:
                canos.remove(cano)

            for i, passaro in enumerate(passaros):
                if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    historico.adicionar_pontuacao(usuario, pontos)
                    messagebox.showinfo("Game Over", f"Game Over! Pontuação: {pontos}")
                    passaros.pop(i)
                    rodando = False

            desenhar_tela(tela, [chao] + canos + passaros, pontos)

        jogar_novamente = messagebox.askyesno("Game Over", "Deseja jogar novamente?")
        if not jogar_novamente:
            break

    historico_str = "\n".join([f"{h[0].nome}: {h[1]}" for h in historico.historico])
    messagebox.showinfo("Histórico de Pontuações", historico_str)

if __name__ == '__main__':
    main()
