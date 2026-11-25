from abc import ABC, abstractmethod

class Entidad(ABC):
    @abstractmethod
    def describir(self):
        pass
