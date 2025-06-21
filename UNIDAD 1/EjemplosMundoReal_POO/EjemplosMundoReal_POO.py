# ejemplo de tienda

# Esta clase modela los artículos individuales que la tienda vende.
# Contiene atributos como su nombre, precio y la cantidad disponible en stock.
# También define cómo se representa un producto en texto.
class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return f"{self.nombre} (${self.precio:.2f}) - Stock: {self.stock}"

# Aqui esta clase representa a los usuarios de la tienda.
# Cada cliente tiene un nombre y un identificador único.
# Además, cada cliente mantiene un registro de los productos que ha agregado a su "carrito"
# y puede realizar acciones como añadir productos o calcular el total de su carrito.
class Cliente:
    def __init__(self, nombre, id_cliente):
        self.nombre = nombre
        self.id_cliente = id_cliente
        self.productos_en_carrito = {} # Diccionario: {Objeto Producto: cantidad}

    def agregar_al_carrito(self, producto, cantidad=1):
        if producto.stock >= cantidad:
            self.productos_en_carrito[producto] = self.productos_en_carrito.get(producto, 0) + cantidad
            print(f"{self.nombre} añadió {cantidad}x {producto.nombre} al carrito.")
            return True
        else:
            print(f"No hay suficiente stock de {producto.nombre}.")
            return False

    def calcular_total_carrito(self):
        total = sum(p.precio * c for p, c in self.productos_en_carrito.items())
        return total

    def __str__(self):
        return f"Cliente: {self.nombre} (ID: {self.id_cliente})"

# Esta es la clase central del sistema. Representa la tienda en sí.
# La tienda es responsable de gestionar su catálogo de productos y de procesar las compras de los clientes.
# Contiene métodos para añadir productos al catálogo, mostrar lo que vende y, crucialmente,
# verificar el stock y completar las transacciones de los clientes.
class Tienda:
    def __init__(self, nombre_tienda):
        self.nombre = nombre_tienda
        self.catalogo = {} # Diccionario: {nombre_producto_str: Objeto Producto}

    def añadir_producto(self, producto):
        self.catalogo[producto.nombre] = producto
        print(f"Producto '{producto.nombre}' añadido al catálogo.")

    def procesar_compra(self, cliente):
        print(f"\n--- Procesando compra de {cliente.nombre} ---")
        if not cliente.productos_en_carrito:
            print("Carrito vacío. Compra cancelada.")
            return False

        # Verificar stock antes de modificarlo para asegurar que todos los items pueden ser comprados
        for producto, cantidad in cliente.productos_en_carrito.items():
            if producto.stock < cantidad:
                print(f"ERROR: {producto.nombre} sin suficiente stock. Compra cancelada.")
                cliente.productos_en_carrito.clear() # Vaciar carrito si falla
                return False

        # Si hay stock para todos los productos en el carrito, proceder con la venta
        total = cliente.calcular_total_carrito()
        for producto, cantidad in cliente.productos_en_carrito.items():
            producto.stock -= cantidad # Reducir el stock del producto
            print(f"Stock de {producto.nombre} ahora: {producto.stock}")

        print(f"Compra de ${total:.2f} completada para {cliente.nombre}.")
        cliente.productos_en_carrito.clear() # Vaciar el carrito del cliente después de la compra
        return True

    def mostrar_catalogo(self):
        print(f"\n--- Catálogo de {self.nombre} ---")
        if not self.catalogo:
            print("Catálogo vacío.")
            return
        for prod_nombre, prod_obj in self.catalogo.items():
            print(f"- {prod_obj}")
        print("------------------------------")

# Este es el punto de entrada del programa donde se crean los objetos
# y se simulan las interacciones entre ellos para mostrar cómo funciona
# el sistema de la tienda.
if __name__ == "__main__":
    # Crear una instancia de la Tienda con un nombre personalizado
    mi_tienda = Tienda("La Tienda de Manuel Lapo")

    # Crear algunos productos y añadirlos al catálogo de la tienda
    laptop = Producto("Laptop Gamer", 1200.00, 5)
    teclado = Producto("Teclado Mecánico", 80.50, 10)
    mi_tienda.añadir_producto(laptop)
    mi_tienda.añadir_producto(teclado)
    mi_tienda.mostrar_catalogo()

    # Crear instancias de clientes con nombres personalizados
    cliente_manuel = Cliente("Manuel Lapo", "ML001")
    cliente_maribel = Cliente("Maribel Salinas", "MS002")
    print(cliente_manuel)
    print(cliente_maribel)

    # Simular que Manuel Lapo añade productos a su carrito
    cliente_manuel.agregar_al_carrito(laptop, 1)
    cliente_manuel.agregar_al_carrito(teclado, 2)
    cliente_manuel.agregar_al_carrito(laptop, 1) # Añade otra laptop, total 2
    cliente_manuel.agregar_al_carrito(teclado, 10) # Intento de añadir más de lo que hay en stock, esto fallará en la compra

    # Procesar la compra de Manuel Lapo
    mi_tienda.procesar_compra(cliente_manuel)
    mi_tienda.mostrar_catalogo() # El stock de Laptop y Teclado (2 unidades) debería haberse actualizado

    # Simular que Maribel Salinas intenta una compra con stock insuficiente
    cliente_maribel.agregar_al_carrito(laptop, 5) # Intenta comprar 5 laptops, pero el stock es 3 (5 inicial - 2 de Manuel)
    mi_tienda.procesar_compra(cliente_maribel) # Esta compra debería fallar por falta de stock