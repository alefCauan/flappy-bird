import tkinter as tk
from tkinter import messagebox, simpledialog
import pygame
import os
import random
import abc
from usuario import Usuario
from historico import HistoricoPontuacao
from desenhavel import Desenhavel
from passaro import Passaro
from chao import Chao
from cano import Cano
from imgs import IMAGEM_BACKGROUND

TELA_LARGURA = 500
TELA_ALTURA = 800


pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('times new roman', 30)

def desenhar_tela(tela, objetos, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for obj in objetos:
        obj.desenhar(tela)
    texto = FONTE_PONTOS.render(f"PONTUAÇÃO: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 135 - texto.get_width(), 10))
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
  