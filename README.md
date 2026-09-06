# Restaurante App - Semana 12

## Estudiante:
**JENIFER ESTEFANIA MERCHAN JAUREGUI** 

## Descripción del Proyecto
Mejora de rendimiento sobre el sistema `restaurante_app` mediante la implementación de estructuras de datos auxiliares (índices en memoria con diccionarios) para optimizar búsquedas y consultas frecuentes.

## Estructura del Proyecto
```text
restaurante_app/
│── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
│── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
│── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
│── main.py
└── README.md
```
## Mejoras de Rendimiento Aplicadas  
Se conservaron las listas principales (`_productos, _usuarios, _ventas`) para mantener el orden y la persistencia en archivos JSON, e incorporamos índices auxiliares en memoria (`dict`):

_Búsqueda de productos (`buscar_producto`):_

Antes: Recorrido lineal O(n) sobre la lista de productos.

Ahora: Búsqueda instantánea O(1) usando el diccionario `_index_productos`.

_Búsqueda de usuarios (`buscar_usuario`):_

Antes: Recorrido lineal O(n) sobre la lista de usuarios.

Ahora: Búsqueda instantánea O(1) usando el diccionario `_index_usuarios`.

_Consulta de ventas por usuario (`consultar_ventas_usuario`):_

Antes: Filtro lineal O(n) recorriendo todas las ventas registradas.

Ahora: Consulta instantánea O(1) usando la estructura `_index_ventas_usuario` (dict de `id_usuario` -> `List[Venta]`).

_Sincronización y Reconstrucción_

Reconstrucción inicial: Al iniciar el programa, el método `_reconstruir_indices()` llena los diccionarios a partir de los datos recuperados desde JSON.

Sincronización continua: Cada vez que se registra un nuevo producto, usuario o venta, la información se añade tanto a la lista de persistencia como al índice auxiliar correspondiente.

## Estructuras Utilizadas
- `self.productos` / `self.usuarios` / `self.ventas`: Listas para almacenamiento persistente y recorrido global.
- `self._index_productos`: `dict` `[codigo -> Producto]`
- `self._index_usuarios`: `dict` `[identificacion -> Usuario]`
- `self._index_ventas_usuario`: `dict` `[id_usuario -> List[Venta]]`

## Ejecución

python main.py

## Pruebas Realizadas
-Comprobación de Persistencia Inicial: Creación de usuarios y productos, cierre y reapertura del sistema comprobando que
los datos persistieran correctamente.  

-Venta Válida: Venta de 10 unidades sobre un producto con stock de 50. Se comprobó la reducción del stock a 40, la creación 
del registro en `ventas.json` y la correcta asignación al usuario.  

-Venta Inválida (Stock Insuficiente): Intento de venta de una cantidad superior al stock restante. El sistema rechazó la 
transacción, conservando intactos los registros y el stock actual.   

-Consulta de Ventas: Filtrado de compras por usuario validando la correcta recuperación e iteración de la colección de 
ventas.  