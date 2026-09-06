from typing import List, Optional, Dict
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class Restaurante:
    def __init__(self):
        # Colecciones principales (Listas) para almacenar y persistir
        self._productos: List[Producto] = ArchivoServicio.cargar_productos()
        self._usuarios: List[Usuario] = ArchivoServicio.cargar_usuarios()
        self._ventas: List[Venta] = ArchivoServicio.cargar_ventas()

        # Índices auxiliares en memoria (Diccionarios) para optimizar búsquedas O(1)
        self._index_productos: Dict[str, Producto] = {}
        self._index_usuarios: Dict[str, Usuario] = {}
        self._index_ventas_usuario: Dict[str, List[Venta]] = {}

        # Reconstrucción de índices al iniciar
        self._reconstruir_indices()

    def _reconstruir_indices(self) -> None:
        """Reconstruye los índices auxiliares a partir de las listas principales recuperadas de JSON."""
        # Índice por código de producto
        self._index_productos = {p.codigo: p for p in self._productos}

        # Índice por identificación de usuario
        self._index_usuarios = {u.identificacion: u for u in self._usuarios}

        # Índice de ventas por usuario
        self._index_ventas_usuario = {}
        for venta in self._ventas:
            self._index_ventas_usuario.setdefault(venta.usuario_id, []).append(venta)

    def registrar_producto(self, codigo: str, nombre: str, precio: float, stock: int) -> bool:
        if self.buscar_producto(codigo) is not None:
            return False
        nuevo_producto = Producto(codigo, nombre, precio, stock)

        # Guardar en lista principal e índice auxiliar
        self._productos.append(nuevo_producto)
        self._index_productos[codigo] = nuevo_producto

        ArchivoServicio.guardar_productos(self._productos)
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        # Búsqueda optimizada O(1) usando el diccionario
        return self._index_productos.get(codigo)

    def obtener_productos(self) -> List[Producto]:
        return self._productos

    def registrar_usuario(self, identificacion: str, nombre: str) -> bool:
        if self.buscar_usuario(identificacion) is not None:
            return False
        nuevo_usuario = Usuario(identificacion, nombre)

        # Guardar en lista principal e índice auxiliar
        self._usuarios.append(nuevo_usuario)
        self._index_usuarios[identificacion] = nuevo_usuario

        ArchivoServicio.guardar_usuarios(self._usuarios)
        return True

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        # Búsqueda optimizada O(1) usando el diccionario
        return self._index_usuarios.get(identificacion)

    def obtener_usuarios(self) -> List[Usuario]:
        return self._usuarios

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        # Búsquedas instantáneas usando los métodos optimizados
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)

        # Sincronizar el índice auxiliar de ventas por usuario
        self._index_ventas_usuario.setdefault(identificacion_usuario, []).append(venta)

        producto.vender(cantidad)

        ArchivoServicio.guardar_ventas(self._ventas)
        ArchivoServicio.guardar_productos(self._productos)
        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> List[Venta]:
        # Consulta optimizada O(1) sin recorrer la lista de ventas completa
        return self._index_ventas_usuario.get(identificacion_usuario, [])