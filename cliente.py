from entidad import Entidad
from excepciones import DatosInvalidos

class Cliente(Entidad):
    def __init__(self, nombre, correo):
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidos('Nombre obligatorio')
        if not isinstance(correo, str) or correo.count('@') != 1 or not all(correo.split('@')) or '.' not in correo.split('@')[1] or any(c.isspace() for c in correo):
            raise DatosInvalidos('Correo invalido')
        self.__nombre = nombre.strip()
        self.__correo = correo

    @property
    def nombre(self):
        return self.__nombre

    def describir(self):
        return self.__nombre
