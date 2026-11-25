from abc import abstractmethod
from math import isfinite
from entidad import Entidad
from excepciones import DatosInvalidos, ServicioNoDisponible

def numero(valor):
    # Conserva la causa original cuando falla la conversion.
    if isinstance(valor, bool):
        raise DatosInvalidos("Se requiere un numero, no un booleano")
    try:
        resultado = float(valor)
    except (ValueError, TypeError, OverflowError) as error:
        raise DatosInvalidos('Se requiere un numero valido') from error
    if not isfinite(resultado):
        raise DatosInvalidos('Numero no finito')
    return resultado

# Reune las reglas compartidas por los servicios.
class Servicio(Entidad):
    def __init__(self, tarifa, disponible=True):
        self.tarifa = numero(tarifa)
        if self.tarifa <= 0:
            raise DatosInvalidos('Tarifa debe ser positiva')
        if not isinstance(disponible, bool):
            raise DatosInvalidos("Disponibilidad debe ser booleana")
        self.disponible = disponible

    # Comprueba la disponibilidad y los limites de duracion.
    def validar(self, horas):
        if not self.disponible:
            raise ServicioNoDisponible('Servicio no disponible')
        horas = numero(horas)
        if horas <= 0:
            raise DatosInvalidos('Duracion debe ser positiva')
        return horas

    # Aplica primero el descuento y luego el impuesto.
    def total(self, base, impuesto, descuento):
        impuesto, descuento = numero(impuesto), numero(descuento)
        if not 0 <= descuento <= 100 or not 0 <= impuesto <= 100:
            raise DatosInvalidos('Porcentaje invalido')
        return round(numero(base * (1-descuento/100) * (1+impuesto/100)), 2)

    @abstractmethod
    # Permite calcular el costo con porcentajes opcionales.
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        pass

# Especializa las reglas de alquiler de salas.
class Sala(Servicio):
    def describir(self):
        return 'Reserva de sala'

    # Comprueba la disponibilidad y los limites de duracion.
    def validar(self, horas):
        horas = super().validar(horas)
        if horas > 12:
            raise DatosInvalidos('Sala: maximo 12 horas')
        return horas

    # Permite calcular el costo con porcentajes opcionales.
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self.total(self.tarifa*self.validar(horas), impuesto, descuento)

# Incluye un recargo fijo por alquiler de equipos.
class Equipo(Servicio):
    def describir(self):
        return 'Alquiler de equipo'

    # Comprueba la disponibilidad y los limites de duracion.
    def validar(self, horas):
        horas = super().validar(horas)
        if horas > 24:
            raise DatosInvalidos('Equipo: maximo 24 horas')
        return horas

    # Permite calcular el costo con porcentajes opcionales.
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self.total(self.tarifa*self.validar(horas)+5000, impuesto, descuento)

# Incluye un recargo del diez por ciento.
class Asesoria(Servicio):
    def describir(self):
        return 'Asesoria especializada'

    # Comprueba la disponibilidad y los limites de duracion.
    def validar(self, horas):
        horas = super().validar(horas)
        if horas > 8:
            raise DatosInvalidos('Asesoria: maximo 8 horas')
        return horas

    # Permite calcular el costo con porcentajes opcionales.
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self.total(self.tarifa*self.validar(horas)*1.1, impuesto, descuento)
