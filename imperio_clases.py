from enum import Enum
from abc import ABC, abstractmethod

class UBICACION(Enum):
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cúmulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

class CLASE(Enum):
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"

# JERARQUIA DE NAVES

class UNIDAD_COMBATE:
    def __init__(self, id_combate: str, clave: int):
        self.id_combate = id_combate
        self.__clave = clave 
    
class NAVE(UNIDAD_COMBATE):
    def __init__(self, id_combate: str, clave: int, nombre: str, catalogo_rep: list[str]):
        super().__init__(id_combate, clave)
        self.nombre = nombre
        self.catalogo_rep = catalogo_rep

class ESTACION_ESPACIAL(NAVE):
    def __init__(self, id_combate: str, clave: int, nombre: str, catalogo_rep: list[str],  tripulacion: int, pasaje: int, ubicacion: UBICACION):
        super().__init__(id_combate, clave, nombre, catalogo_rep)
        self.ubicacion = ubicacion
        self.tripulacion = tripulacion
        self.pasaje = pasaje

class NAVE_ESTELAR(NAVE):
    def __init__(self, id_combate: str, clave: int, nombre: str, catalogo_rep: list[str],  tripulacion: int, pasaje: int, clase: CLASE):
        super().__init__(id_combate, clave, nombre, catalogo_rep)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

class CAZA(NAVE):
    def __init__(self, id_combate: str, clave: int, nombre: str, catalogo_rep: list[str],  dotacion: int):
        super().__init__(id_combate, clave, nombre, catalogo_rep)
        self.dotacion = dotacion

# REPUESTOS Y ALMACENES

class REPUESTOS:
    def __init__(self, nombre: str, proveedor: str, cantidad: int, precio: int):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio

class ALMACEN():
    def __init__(self,nombre: str, ubicacion: str, catalogo_rep: list[REPUESTOS]):
        self.nombre = nombre
        self.catalogo_rep = catalogo_rep
        self.ubicacion = ubicacion

# USUARIOS

class USUARIO(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def salida(self):
        pass

class COMANDANTE(USUARIO):
    def __init__(self, nombre: str, naveAsignada: NAVE):
        super().__init__(nombre)
        self.naveAsignada = naveAsignada

class OPERARIO(USUARIO):
    def __init__(self, nombre: str, almacenAsignado: ALMACEN):
        super().__init__(nombre)
        self.almacenAsignado = almacenAsignado
    
