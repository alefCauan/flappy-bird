class HistoricoPontuacao:
    def __init__(self):
        self._historico = []

    @property
    def historico(self):
        return self._historico

    def adicionar_pontuacao(self, usuario, pontuacao):
        self.historico.append((usuario, pontuacao))