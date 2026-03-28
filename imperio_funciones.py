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

    def buscar_rep(self, nombreRep: str) -> REPUESTOS:
        for rep in self.catalogo_rep:
            if rep.nombre == nombreRep:
                return rep
    
    def tiene_stock(self, nombreRep: str, cantidad: int) -> bool:
        repuesto = self.buscar_rep(nombreRep)
        return repuesto._REPUESTOS__cantidad >= cantidad
    
    def descontar_rep(self, nombreRep: str, cantidad: int):
        repuesto = self.buscar_rep(nombreRep)
        repuesto._REPUESTOS__cantidad -= cantidad

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

    def consultar_rep(self, nombreRep: str) -> list[REPUESTOS]:
        return self.naveAsignada.catalogo_rep
    
    def adquirir_rep(self, nombreRep: str, cantidad: int) -> bool:
        if self.naveAsignada.almacen.tiene_stock(nombreRep, cantidad):
            self.naveAsignada.almacen.descontar_rep(nombreRep, cantidad)
            print(f"{self.nombre} ha adquirido {cantidad} unidades de {nombreRep} del {self.naveAsignada.almacen.nombre}.")
        else:
            print(f"Stock insuficiente para {nombreRep} en {self.naveAsignada.almacen.nombre}.")

    def salida(self):
        return f"COMANDANTE({self.nombre}, nave={self.naveAsignada.nombre})"

class OPERARIO(USUARIO):
    def __init__(self, nombre: str, almacenAsignado: ALMACEN):
        super().__init__(nombre)
        self.almacenAsignado = almacenAsignado

    def agregar_rep(self, r: REPUESTOS):
        self.almacenAsignado.catalogo_rep.append(r)
        print(f"{self.nombre} ha agregado {r.nombre} al {self.almacenAsignado.nombre}.")
    
    def eliminar_rep(self, nombreRep: str):
        repuesto = self.almacenAsignado.buscar_rep(nombreRep)
        self.almacenAsignado.catalogo_rep.remove(repuesto)
        print(f"{self.nombre} ha eliminado {nombreRep} del {self.almacenAsignado.nombre}.")
    
    def actualizar_stock(self, nombreRep: str, cantidad: int):
        repuesto = self.almacenAsignado.buscar_rep(nombreRep)
        repuesto._REPUESTOS__cantidad = cantidad
        print(f"{self.nombre} ha actualizado el stock de {nombreRep} a {cantidad} unidades en {self.almacenAsignado.nombre}.")
    
    def listar_reps(self):
        print(f"Repuestos en {self.almacenAsignado.nombre}:")
        for rep in self.almacenAsignado.catalogo_rep:
            print(f"{rep.nombre} (Proveedor: {rep.proveedor}, Cantidad: {rep._REPUESTOS__cantidad}, Precio: {rep.precio})")

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
    
    print(" PRUEBA DEL SISTEMA \n")
    
    # OPERARIO - Listar repuestos
    print("1. OPERARIO LISTA REPUESTOS:")
    operario.listar_reps()
    
    # OPERARIO - Agregar nuevo repuesto
    print("\n2. OPERARIO AGREGA REPUESTO:")
    blindaje = REPUESTOS("Blindaje", "Merr-Sonn", 40, 12000)
    operario.agregar_rep(blindaje)
    
    # OPERARIO - Actualizar stock
    print("\n3. OPERARIO ACTUALIZA STOCK:")
    operario.actualizar_stock("Láser", 200)

    # OPERARIO - Listar repuestos actualizados
    print("\n4. OPERARIO LISTA REPUESTOS ACTUALIZADOS:")
    operario.listar_reps()
    
    # ALMACÉN - Tiene stock
    print("\n5. ALMACÉN VERIFICA STOCK:")
    print(f"¿Hay 100 láseres? {almacen.tiene_stock('Láser', 100)}")
    print(f"¿Hay 300 láseres? {almacen.tiene_stock('Láser', 300)}")
    
    # ALMACÉN - Buscar repuesto
    print("\n6. ALMACÉN BUSCA REPUESTO:")
    rep = almacen.buscar_rep("Motor")
    print(f"Encontrado: {rep.salida()}")
    
    # ALMACÉN - Descontar repuesto
    print("\n7. ALMACÉN DESCUENTA REPUESTO:")
    almacen.descontar_rep("Motor", 10)
    print(f"Motor después de descontar: cantidad={motor._REPUESTOS__cantidad}")
    
    # COMANDANTE - Consultar repuestos de nave
    print("\n8. COMANDANTE CONSULTA CATÁLOGO DE NAVE:")
    print(f"Repuestos en {executor.nombre}: {comandante.consultar_rep('')}")
    
    # COMANDANTE - Adquirir repuestos (stock suficiente)
    print("\n9. COMANDANTE ADQUIERE REPUESTOS (stock suficiente):")
    executor.almacen = almacen  # Asignar almacén a la nave
    comandante.adquirir_rep("Escudo", 15)
    print(f"Escudo después de adquisición: cantidad={escudo._REPUESTOS__cantidad}")
    
    # COMANDANTE - Adquirir repuestos (stock insuficiente)
    print("\n10. COMANDANTE INTENTA ADQUIRIR (stock insuficiente):")
    comandante.adquirir_rep("Láser", 500)
    
    # OPERARIO - Eliminar repuesto
    print("\n11. OPERARIO ELIMINA REPUESTO:")
    operario.eliminar_rep("Blindaje")
    
    # OPERARIO - Listar final
    print("\n12. OPERARIO LISTA REPUESTOS FINALES:")
    operario.listar_reps()
    
    print("\n=== FIN DE PRUEBA ===")
