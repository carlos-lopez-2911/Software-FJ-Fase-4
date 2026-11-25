# Software FJ - Fase 4
Sistema de clientes, servicios y reservas sin base de datos.

## Ejecucion
Requiere Python 3. Ejecutar `python main.py` desde la carpeta del proyecto. No requiere paquetes externos. Se ejecutan 18 pruebas y se genera sistema.log.

## Organizacion
- entidad.py: abstraccion general.
- cliente.py: encapsulacion y validacion.
- servicios.py: herencia, polimorfismo y calculos con parametros opcionales.
- reserva.py: estados y procesamiento.
- excepciones.py: errores personalizados.
- main.py: listas, simulaciones y registro de eventos.

Las tarifas, recargos y limites de horas son supuestos de simulacion, no datos suministrados por la guia. Los clientes son ficticios. Los datos se conservan en memoria durante la ejecucion. El log se reemplaza en cada ejecucion.

## Verificacion de calculos
Las pruebas 12, 17 y 18 comparan los resultados con 42840, 35000 y 88000 COP, respectivamente. La prueba 10 intenta reservar un servicio registrado pero no disponible. Las tarifas y recargos son supuestos de la simulacion.
