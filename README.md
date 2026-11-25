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
