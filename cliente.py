from entidad import Entidad
from excepciones import DatosInvalidos

# Representa al cliente y protege sus datos mediante atributos privados.
class Cliente(Entidad):
    def __init__(self, nombre, correo):
        # Comprueba que el nombre sea texto y no este vacio.
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidos('Nombre obligatorio')
        # Verifica la estructura basica del correo, sin comprobar su existencia.
        if not isinstance(correo, str) or correo.count('@') != 1 or not all(correo.split('@')) or '.' not in correo.split('@')[1] or any(c.isspace() for c in correo):
            raise DatosInvalidos('Correo invalido')
        # Guarda los datos validados.
        self.__nombre = nombre.strip()
        self.__correo = correo

    # Permite consultar el nombre sin modificarlo directamente.
    @property
    def nombre(self):
        return self.__nombre

    def describir(self):
        return self.__nombre
