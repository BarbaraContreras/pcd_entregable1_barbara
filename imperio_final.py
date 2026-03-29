from enum import Enum
from abc import ABC, abstractmethod

# EXCEPCIONES PERSONALIZADAS

class ErrorSistemaImperio(Exception): #Excepción base del sistema
    pass

class ErrorRepuestoNoEncontrado(ErrorSistemaImperio): # Cuando un repuesto no existe en el almacén
    pass

class ErrorStockInsuficiente(ErrorSistemaImperio): # Cuando no hay suficiente cantidad en stock
    pass

# ENUMERACIONES

class UBICACION(Enum):
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cúmulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

class CLASE(Enum):
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"

# JERARQUIA DE NAVES

class UNIDAD_COMBATE: #Clase base para todas las unidades de combate
    def __init__(self, id_combate: str, clave: int):
        self.id_combate = id_combate  
        self.__clave = clave  
    
class NAVE(UNIDAD_COMBATE): #Clase base para todas las naves (hereda de UNIDAD_COMBATE)
    def __init__(self, id_combate: str, clave: int, nombre: str, catalogo_rep: list[str]):
        super().__init__(id_combate, clave)
        self.nombre = nombre  # Nombre de la nave
        self.catalogo_rep = catalogo_rep  # Lista de repuestos que usa esta nave
    
    def salida(self): #Método para mostrar la información de la nave de forma legible
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

class REPUESTOS: #Representa un repuesto para naves
    def __init__(self, nombre: str, proveedor: str, cantidad: int, precio: int):
        self.nombre = nombre  
        self.proveedor = proveedor  
        self.__cantidad = cantidad  # Cantidad disponible (PRIVADA)
        self.precio = precio  
    
    def salida(self):
        return f"REPUESTOS({self.nombre}, proveedor={self.proveedor}, cantidad={self.__cantidad}, precio={self.precio})"

class ALMACEN(): #Gestiona el almacén de repuestos y su inventario
    def __init__(self,nombre: str, ubicacion: str, catalogo_rep: list[REPUESTOS]):
        self.nombre = nombre  
        self.catalogo_rep = catalogo_rep  
        self.ubicacion = ubicacion  

    def buscar_rep(self, nombreRep: str) -> REPUESTOS: # Busca un repuesto por nombre. Lanza excepción si no existe
        for rep in self.catalogo_rep:
            if rep.nombre == nombreRep:
                return rep  
        raise ErrorRepuestoNoEncontrado(f"Repuesto '{nombreRep}' no encontrado")
    
    def tiene_stock(self, nombreRep: str, cantidad: int) -> bool: # Verifica si hay suficiente stock de un repuesto. 
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")  # Validar cantidad positiva
        repuesto = self.buscar_rep(nombreRep)  # Buscar el repuesto
        if repuesto is None:
            return False  
        return repuesto._REPUESTOS__cantidad >= cantidad  
    
    def descontar_rep(self, nombreRep: str, cantidad: int): # Descontar cantidad de un repuesto del almacén.
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")  # Validar cantidad positiva
        repuesto = self.buscar_rep(nombreRep)  # Buscar el repuesto
        if repuesto is None:
            raise ErrorRepuestoNoEncontrado(f"No se puede descontar {nombreRep}")  # No existe
        if repuesto._REPUESTOS__cantidad < cantidad:
            raise ErrorStockInsuficiente(f"Stock insuficiente de {nombreRep}")  # No hay suficiente
        repuesto._REPUESTOS__cantidad -= cantidad  # Descontar la cantidad

    def salida(self):
        return f"ALMACEN({self.nombre}, ubicacion={self.ubicacion}, catalogo_rep={self.catalogo_rep})"

# USUARIOS

class USUARIO(ABC): #Clase abstracta para usuarios del sistema (COMANDANTE/OPERARIO)
    def __init__(self, nombre: str):
        self.nombre = nombre  # Nombre del usuario

    @abstractmethod
    def salida(self): # Método abstracto de subclases para mostrar información del usuario
        pass

class COMANDANTE(USUARIO): # Usuario con permisos para consultar y adquirir repuestos de su nave
    def __init__(self, nombre: str, naveAsignada: NAVE, almacen: ALMACEN):
        super().__init__(nombre)
        self.naveAsignada = naveAsignada  
        self.almacen = almacen  # Acceso a un almacén de referencia

    def consultar_rep(self, nombreRep: str) -> list[REPUESTOS]: # Ver los repuestos de la nave asignada
        return self.naveAsignada.catalogo_rep
    
    def adquirir_rep(self, nombreRep: str, cantidad: int): # Solicitar repuestos del almacén para la nave.
        # Verificar que la nave usa este repuesto
        if nombreRep not in self.naveAsignada.catalogo_rep:
            raise ErrorSistemaImperio(f"La nave {self.naveAsignada.nombre} no usa repuesto '{nombreRep}'")
        
        if cantidad <= 0: # Validar que la cantidad sea positiva
            raise ValueError("La cantidad debe ser mayor a 0")
        
        # Verifica stock suficiente
        if not self.almacen.tiene_stock(nombreRep, cantidad):
            raise ErrorStockInsuficiente(f"Stock insuficiente para {nombreRep}")
        
        print(f"{self.nombre} ha solicitado {cantidad} unidades de {nombreRep} para {self.naveAsignada.nombre}.")

    def salida(self):
        return f"COMANDANTE({self.nombre}, nave={self.naveAsignada.nombre})"

class OPERARIO(USUARIO): # Usuario con permisos para gestionar un almacén
    def __init__(self, nombre: str, almacenAsignado: ALMACEN):
        super().__init__(nombre)
        self.almacenAsignado = almacenAsignado  # Almacén que gestiona

    def agregar_rep(self, r: REPUESTOS): # Añadir un nuevo repuesto al almacén
        mensaje = f"{self.nombre} ha agregado {r.nombre} al {self.almacenAsignado.nombre}." 
        self.almacenAsignado.catalogo_rep.append(r)  
        print(mensaje)
    
    def eliminar_rep(self, nombreRep: str): # Eliminar un repuesto del almacén
        repuesto = self.almacenAsignado.buscar_rep(nombreRep)  # Buscar el repuesto
        if repuesto is None:
            raise ErrorRepuestoNoEncontrado(f"No existe '{nombreRep}'")
        self.almacenAsignado.catalogo_rep.remove(repuesto)  # Eliminar de la lista
        print(f"{self.nombre} ha eliminado {nombreRep} del {self.almacenAsignado.nombre}.")
    
    def actualizar_stock(self, nombreRep: str, cantidad: int): #Cambiar la cantidad disponible de un repuesto
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")  # Confirmar cantidad no negativa
        repuesto = self.almacenAsignado.buscar_rep(nombreRep)  # Buscar el repuesto
        if repuesto is None:
            raise ErrorRepuestoNoEncontrado(f"No existe '{nombreRep}'")
        repuesto._REPUESTOS__cantidad = cantidad  # Actualizar la cantidad
        print(f"{self.nombre} ha actualizado el stock de {nombreRep} a {cantidad} unidades en {self.almacenAsignado.nombre}.")
    
    def listar_reps(self): #Mostrar todos los repuestos del almacén con sus detalles
        print(f"Repuestos en {self.almacenAsignado.nombre}:")
        for rep in self.almacenAsignado.catalogo_rep:
            print(f"{rep.nombre} (Proveedor: {rep.proveedor}, Cantidad: {rep._REPUESTOS__cantidad}, Precio: {rep.precio})")

    def salida(self):
        return f"OPERARIO({self.nombre}, almacen={self.almacenAsignado.nombre})"
    
# PRUEBAS

if __name__ == "__main__":
    try:  
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
        comandante = COMANDANTE("Capitán Needa", executor, almacen)  
        operario = OPERARIO("Oficial Jerjerrod", almacen)
        
        print("=== PRUEBAS DEL SISTEMA ===\n")
        
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
        if rep:
            print(f"Encontrado: {rep.salida()}")
        
        # ALMACÉN - Descontar repuesto
        print("\n7. ALMACÉN DESCUENTA REPUESTO:")
        almacen.descontar_rep("Motor", 10)
        print(f"Motor después de descontar: cantidad={motor._REPUESTOS__cantidad}")
        
        # COMANDANTE - Consultar repuestos de nave
        print("\n8. COMANDANTE CONSULTA CATÁLOGO DE NAVE:")
        print(f"Repuestos en {executor.nombre}: {comandante.consultar_rep('')}")
        
        # COMANDANTE - Adquirir repuestos (stock suficiente)
        print("\n9. COMANDANTE SOLICITA REPUESTOS (stock suficiente):")
        try:
            comandante.adquirir_rep("Escudo", 15)  
            almacen.descontar_rep("Escudo", 15)  
            print(f"Escudo después de descontar: cantidad={escudo._REPUESTOS__cantidad}")
        except (ErrorSistemaImperio, ErrorStockInsuficiente) as e:
            print(f"Error capturado: {e}")
        
        # OPERARIO - Eliminar repuesto
        print("\n10. OPERARIO ELIMINA REPUESTO:")
        try:
            operario.eliminar_rep("Blindaje")
        except ErrorRepuestoNoEncontrado as e:
            print(f"Error capturado: {e}")
        
        # OPERARIO - Listar final
        print("\n11. OPERARIO LISTA REPUESTOS FINALES:")
        operario.listar_reps()
        
        # EJEMPLOS DE ERRORES
        print("\n=== PRUEBAS DE ERRORES ===\n")
        
        # Error 1: Repuesto no encontrado
        print("ERROR 1 - Repuesto no encontrado:")
        try:
            almacen.buscar_rep("Hipermotor")
        except ErrorRepuestoNoEncontrado as e:
            print(f"Capturado correctamente: {e}")
        
        # Error 2: Stock insuficiente al descontar
        print("\nERROR 2 - Stock insuficiente:")
        try:
            almacen.descontar_rep("Escudo", 500)  # Solo hay 15
        except ErrorStockInsuficiente as e:
            print(f"Capturado correctamente: {e}")
        
        # Error 3: Cantidad negativa
        print("\nERROR 3 - Cantidad negativa:")
        try:
            almacen.descontar_rep("Motor", -5)
        except ValueError as e:
            print(f"Capturado correctamente: {e}")
        
        # Error 4: Agregar objeto inválido (no es REPUESTOS)
        print("\nERROR 4 - Tipo de dato incorrecto:")
        try:
            operario.agregar_rep("Esto no es un repuesto")
        except AttributeError as e:
            print(f"Capturado correctamente: {e}")
        
        # Error 5: Eliminar repuesto que no existe
        print("\nERROR 5 - Eliminar repuesto inexistente:")
        try:
            operario.eliminar_rep("NaveDeDestructor")
        except ErrorRepuestoNoEncontrado as e:
            print(f"Capturado correctamente: {e}")
        
        # Error 6: Actualizar stock con cantidad negativa
        print("\nERROR 6 - Actualizar con cantidad negativa:")
        try:
            operario.actualizar_stock("Motor", -20)
        except ValueError as e:
            print(f"Capturado correctamente: {e}")
        
        # Error 7: Verificar stock con cantidad negativa
        print("\nERROR 7 - Verificar stock con cantidad negativa:")
        try:
            almacen.tiene_stock("Láser", -10)
        except ValueError as e:
            print(f"Capturado correctamente: {e}")
        
        # Error 8: Adquirir repuesto que la nave NO usa
        print("\nERROR 8 - Nave no usa este repuesto:")
        try:
            comandante_tie = COMANDANTE("Piloto TIE", tie, almacen)
            comandante_tie.adquirir_rep("Escudo", 5)  # TIE no usa Escudo
        except ErrorSistemaImperio as e:
            print(f"Capturado correctamente: {e}")
        
    
    except ErrorSistemaImperio as e:
        print(f"\n Error del sistema: {e}")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
  
