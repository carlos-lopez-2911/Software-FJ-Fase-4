from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
from excepciones import ReservaInvalida

class Reserva(Entidad):
    def __init__(self, cliente, servicio, horas):
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalida('Cliente o servicio incorrecto')
        self.cliente = cliente
        self.servicio = servicio
        self.horas = servicio.validar(horas)
        self.__estado = 'Pendiente'

    def describir(self):
        return f'{self.cliente.nombre}: {self.servicio.describir()} - {self.__estado}'

    def confirmar(self):
        if self.__estado != 'Pendiente':
            raise ReservaInvalida('Solo se confirman reservas pendientes')
        self.servicio.validar(self.horas)
        self.__estado = 'Confirmada'
        return self.describir()

    def cancelar(self):
        if self.__estado == 'Cancelada':
            raise ReservaInvalida('Reserva ya cancelada')
        self.__estado = 'Cancelada'
        return self.describir()

    def procesar(self, impuesto=0, descuento=0):
        if self.__estado != 'Confirmada':
            raise ReservaInvalida('Reserva no confirmada')
        return self.servicio.calcular_costo(self.horas, impuesto, descuento)
