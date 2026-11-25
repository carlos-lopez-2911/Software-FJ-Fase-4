from abc import ABC, abstractmethod

# Define el contrato comun para las entidades del sistema.
class Entidad(ABC):
    # Obliga a las clases concretas a implementar una descripcion.
    @abstractmethod
    def describir(self):
        pass
