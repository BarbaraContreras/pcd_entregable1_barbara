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
    
    def salida(self):
        return f"NAVE({self.nombre})"

class ESTACION_ESPACIAL(NAVE):
    def __init__(self, id_combate: str, clave: int, nombre: str, catalogo_rep: list[str],  tripulacion: int, pasaje: int, ubicacion: UBICACION):
        super().__init__(id_combate, clave, nombre, catalogo_rep)
        self.ubicacion = ubicacion
        self.tripulacion = tripulacion
        self.pasaje = pasaje

    def salida(self):
        return f"ESTACION_ESPACIAL({self.nombre}, ubicacion={self.ubicacion.value}, tripulacion={self.tripulacion}, pasaje={self.pasaje})"

class NAVE_ESTELAR(NAVE):
    def __init__(self, id_combate: str, clave: int, nombre: str, catalogo_rep: list[str],  tripulacion: int, pasaje: int, clase: CLASE):
        super().__init__(id_combate, clave, nombre, catalogo_rep)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase
    
    def salida(self):
        return f"NAVE_ESTELAR({self.nombre}, clase={self.clase.value}, tripulacion={self.tripulacion}, pasaje={self.pasaje})"

class CAZA(NAVE):
    def __init__(self, id_combate: str, clave: int, nombre: str, catalogo_rep: list[str],  dotacion: int):
        super().__init__(id_combate, clave, nombre, catalogo_rep)
        self.dotacion = dotacion
    
    def salida(self):
        return f"CAZA({self.nombre}, dotacion={self.dotacion})"

# REPUESTOS Y ALMACENES

class REPUESTOS:
    def __init__(self, nombre: str, proveedor: str, cantidad: int, precio: int):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio
    
    def salida(self):
        return f"REPUESTOS({self.nombre}, proveedor={self.proveedor}, cantidad={self.__cantidad}, precio={self.precio})"

class ALMACEN():
    def __init__(self,nombre: str, ubicacion: str, catalogo_rep: list[REPUESTOS]):
        self.nombre = nombre
        self.catalogo_rep = catalogo_rep
        self.ubicacion = ubicacion

    def salida(self):
        return f"ALMACEN({self.nombre}, ubicacion={self.ubicacion}, catalogo_rep={self.catalogo_rep})"

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

    def salida(self):
        return f"COMANDANTE({self.nombre}, nave={self.naveAsignada.nombre})"

class OPERARIO(USUARIO):
    def __init__(self, nombre: str, almacenAsignado: ALMACEN):
        super().__init__(nombre)
        self.almacenAsignado = almacenAsignado

    def salida(self):
        return f"OPERARIO({self.nombre}, almacen={self.almacenAsignado.nombre})"

# PRUEBAS

if __name__ == "__main__":
    
    # Crear naves
    executor = NAVE_ESTELAR("NE-001", 67890, "Executor", ["Motor", "Escudo"], 37000, 12000, CLASE.EJECUTOR)
    tie = CAZA("CZ-001", 11111, "TIE Fighter", ["Cabina", "Blaster"], 1)
    
    # Crear repuestos
    motor = REPUESTOS("Motor", "SoroSuub", 50, 10000)
    escudo = REPUESTOS("Escudo", "Kuat", 30, 15000)
    laser = REPUESTOS("Láser", "Taim & Bak", 100, 5000)
    
    # Crear almacén
    almacen = ALMACEN("Almacén Endor", "Endor", [motor, escudo, laser])
    
    # Crear usuarios
    comandante = COMANDANTE("Capitán Needa", executor)
    operario = OPERARIO("Oficial Jerjerrod", almacen)

    print(executor.salida())
    print(comandante.salida())
    print(operario.salida())

    
