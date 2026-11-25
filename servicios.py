from abc import abstractmethod
from math import isfinite
from entidad import Entidad
from excepciones import DatosInvalidos, ServicioNoDisponible

def numero(valor):
    # Conserva la causa original cuando falla la conversion.
    try:
        resultado = float(valor)
    except (ValueError, TypeError, OverflowError) as error:
        raise DatosInvalidos('Se requiere un numero valido') from error
    if not isfinite(resultado):
        raise DatosInvalidos('Numero no finito')
    return resultado

class Servicio(Entidad):
    def __init__(self, tarifa, disponible=True):
        self.tarifa = numero(tarifa)
        if self.tarifa <= 0:
            raise DatosInvalidos('Tarifa debe ser positiva')
        self.disponible = disponible

    def validar(self, horas):
        if not self.disponible:
            raise ServicioNoDisponible('Servicio no disponible')
        horas = numero(horas)
        if horas <= 0:
            raise DatosInvalidos('Duracion debe ser positiva')
        return horas

    def total(self, base, impuesto, descuento):
        impuesto, descuento = numero(impuesto), numero(descuento)
        if not 0 <= descuento <= 100 or not 0 <= impuesto <= 100:
            raise DatosInvalidos('Porcentaje invalido')
        return round(numero(base * (1-descuento/100) * (1+impuesto/100)), 2)

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        pass

class Sala(Servicio):
    def describir(self):
        return 'Reserva de sala'

    def validar(self, horas):
        horas = super().validar(horas)
        if horas > 12:
            raise DatosInvalidos('Sala: maximo 12 horas')
        return horas

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self.total(self.tarifa*self.validar(horas), impuesto, descuento)

class Equipo(Servicio):
    def describir(self):
        return 'Alquiler de equipo'

    def validar(self, horas):
        horas = super().validar(horas)
        if horas > 24:
            raise DatosInvalidos('Equipo: maximo 24 horas')
        return horas

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self.total(self.tarifa*self.validar(horas)+5000, impuesto, descuento)

class Asesoria(Servicio):
    def describir(self):
        return 'Asesoria especializada'

    def validar(self, horas):
        horas = super().validar(horas)
        if horas > 8:
            raise DatosInvalidos('Asesoria: maximo 8 horas')
        return horas

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self.total(self.tarifa*self.validar(horas)*1.1, impuesto, descuento)
