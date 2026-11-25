class DatosInvalidos(Exception):
    """Datos que no cumplen las validaciones."""

class ServicioNoDisponible(Exception):
    """Servicio que no puede reservarse."""

class ReservaInvalida(Exception):
    """Operacion incompatible con el estado de la reserva."""
