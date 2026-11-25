import logging
from pathlib import Path
from cliente import Cliente
from servicios import Sala, Equipo, Asesoria
from reserva import Reserva
from excepciones import DatosInvalidos, ServicioNoDisponible, ReservaInvalida

logging.basicConfig(filename=Path(__file__).with_name('sistema.log'), level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8', filemode='w')

class Sistema:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar(self, lista, objeto):
        lista.append(objeto)
        return objeto.describir()

    def reservar(self, cliente, servicio, horas):
        if cliente not in self.clientes or servicio not in self.servicios:
            raise ReservaInvalida('Cliente o servicio no registrado')
        return self.agregar(self.reservas, Reserva(cliente, servicio, horas))

def probar(nombre, operacion, error_esperado=None):
    # Cada prueba es independiente: un error no interrumpe las siguientes.
    try:
        resultado = operacion()
    except Exception as error:
        logging.exception('%s: %s', nombre, error)
        correcto = error_esperado is not None and isinstance(error, error_esperado)
        print(f'{nombre}: {error}')
    else:
        correcto = error_esperado is None
        logging.info('%s: %s', nombre, resultado)
        print(f'{nombre}: {resultado}')
    finally:
        logging.info('Finaliza prueba: %s', nombre)
    print('Prueba superada' if correcto else 'Prueba fallida')
    return correcto

def main():
    s = Sistema()
    pruebas = [
        ('01 Cliente valido', lambda: s.agregar(s.clientes, Cliente('Cliente ficticio', 'cliente@example.com')), None),
        ('02 Nombre vacio', lambda: Cliente('', 'a@example.com'), DatosInvalidos),
        ('03 Correo invalido', lambda: Cliente('Ana', 'correo'), DatosInvalidos),
        ('04 Sala', lambda: s.agregar(s.servicios, Sala(20000)), None),
        ('05 Equipo', lambda: s.agregar(s.servicios, Equipo(15000)), None),
        ('06 Asesoria', lambda: s.agregar(s.servicios, Asesoria(40000)), None),
        ('07 Tarifa negativa', lambda: Sala(-1), DatosInvalidos),
        ('08 Reserva valida', lambda: s.reservar(s.clientes[0], s.servicios[0], 2), None),
        ('09 Duracion negativa', lambda: s.reservar(s.clientes[0], s.servicios[0], -2), DatosInvalidos),
        ('10 Servicio no disponible', lambda: Sala(10000, False).validar(2), ServicioNoDisponible),
        ('11 Confirmacion', lambda: s.reservas[0].confirmar(), None),
        ('12 Procesamiento', lambda: s.reservas[0].procesar(19, 10), None),
        ('13 Descuento invalido', lambda: s.reservas[0].procesar(0, 110), DatosInvalidos),
        ('14 Cancelacion', lambda: s.reservas[0].cancelar(), None),
        ('15 Confirmacion incorrecta', lambda: s.reservas[0].confirmar(), ReservaInvalida),
        ('16 Conversion incorrecta', lambda: Sala('texto'), DatosInvalidos),
        ('17 Costo equipo', lambda: s.servicios[1].calcular_costo(2), None),
        ('18 Costo asesoria', lambda: s.servicios[2].calcular_costo(2), None),
    ]
    resultados = [probar(*prueba) for prueba in pruebas]
    print(f'\nResultado: {sum(resultados)}/{len(resultados)} pruebas superadas')
    logging.info('Resultado: %s/%s', sum(resultados), len(resultados))

if __name__ == '__main__':
    main()
