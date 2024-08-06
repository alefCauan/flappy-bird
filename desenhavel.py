import abc

class Desenhavel(abc.ABC):
    @abc.abstractmethod
    def desenhar(self, tela):
        pass
    @abc.abstractmethod
    def mover(self):
        pass

    