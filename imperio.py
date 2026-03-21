from enum import Enum
from abc import ABC, abstractmethod

class UNIDAD_COMBATE:

    def __init__(self, id_combate: str, clave: int):
        self.id_combate = id_combate
        self.__clave = clave 
    
class NAVE(UNIDAD_COMBATE):

    def __init__(self, id_combate: str, clave: int, nombre: str, catalogo_rep: list[str]):
        super().__init__(id_combate, clave)
        self.nombre = nombre
        self.catalogo_rep = catalogo_rep

class USUARIO(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def __repr__(self):
        pass
    
