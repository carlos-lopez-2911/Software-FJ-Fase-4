import logging
from pathlib import Path
from cliente import Cliente
from servicios import Sala, Equipo, Asesoria
from reserva import Reserva
from excepciones import DatosInvalidos, ServicioNoDisponible, ReservaInvalida

# Configura el registro de eventos y errores en un archivo local.
logging.basicConfig(filename=Path(__file__).with_name('sistema.log'), level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s', encoding='utf-8', filemode='w')

# Mantiene los registros en listas, sin base de datos.
class Sistema:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    # Agrega un objeto y devuelve su descripcion.
    def agregar(self, lista, objeto):
        lista.append(objeto)
        return objeto.describir()

    # Verifica que cliente y servicio esten registrados.
    def reservar(self, cliente, servicio, horas):
        if cliente not in self.clientes or servicio not in self.servicios:
            raise ReservaInvalida('Cliente o servicio no registrado')
        return self.agregar(self.reservas, Reserva(cliente, servicio, horas))

def probar(nombre, operacion, error_esperado=None, valor_esperado=None):
    # Cada prueba es independiente: un error no interrumpe las siguientes.
    try:
        resultado = operacion()
    except Exception as error:
        logging.exception('%s: %s', nombre, error)
        correcto = error_esperado is not None and isinstance(error, error_esperado)
        print(f'{nombre}: {error}')
    else:
        correcto = error_esperado is None and (valor_esperado is None or resultado == valor_esperado)
        if not correcto:
            logging.error("Resultado inesperado: %s; esperado: %s", resultado, valor_esperado)
        logging.info('%s: %s', nombre, resultado)
        print(f'{nombre}: {resultado}')
    finally:
        logging.info('Finaliza prueba: %s', nombre)
    print('Prueba superada' if correcto else 'Prueba fallida')
    return correcto

def main():
    s = Sistema()
    servicio_no_disponible = Sala(10000, False)
    # Define casos validos e invalidos en orden de ejecucion.
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
        ('10 Servicio no disponible', lambda: (s.agregar(s.servicios, servicio_no_disponible), s.reservar(s.clientes[0], servicio_no_disponible, 2))[1], ServicioNoDisponible),
        ('11 Confirmacion', lambda: s.reservas[0].confirmar(), None),
        ('12 Procesamiento', lambda: s.reservas[0].procesar(19, 10), None, 42840.0),
        ('13 Descuento invalido', lambda: s.reservas[0].procesar(0, 110), DatosInvalidos),
        ('14 Cancelacion', lambda: s.reservas[0].cancelar(), None),
        ('15 Confirmacion incorrecta', lambda: s.reservas[0].confirmar(), ReservaInvalida),
        ('16 Conversion incorrecta', lambda: Sala('texto'), DatosInvalidos),
        ('17 Costo equipo', lambda: s.servicios[1].calcular_costo(2), None, 35000.0),
        ('18 Costo asesoria', lambda: s.servicios[2].calcular_costo(2), None, 88000.0),
    ]
    # Ejecuta todos los casos y cuenta los resultados correctos.
    resultados = [probar(*prueba) for prueba in pruebas]
    print(f'\nResultado: {sum(resultados)}/{len(resultados)} pruebas superadas')
    logging.info('Resultado: %s/%s', sum(resultados), len(resultados))

if __name__ == '__main__':
    main()
