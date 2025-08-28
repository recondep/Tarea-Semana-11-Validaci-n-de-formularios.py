import sqlite3

# Clase Producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Getters y setters
    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        self._cantidad = nueva_cantidad

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio):
        self._precio = nuevo_precio

    def __str__(self):
        return f"ID: {self._id} | Nombre: {self._nombre} | Cantidad: {self._cantidad} | Precio: ${self._precio:.2f}"


# Clase Inventario
class Inventario:
    def __init__(self, db_name="inventario.db"):
        self.db_name = db_name
        self.productos = {}  # Diccionario para almacenar productos: key = id, value = Producto
        self._conectar_db()
        self._crear_tabla()
        self._cargar_productos_desde_db()

    def _conectar_db(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def _crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def _cargar_productos_desde_db(self):
        self.cursor.execute("SELECT * FROM productos")
        filas = self.cursor.fetchall()
        for fila in filas:
            id_producto, nombre, cantidad, precio = fila
            self.productos[id_producto] = Producto(id_producto, nombre, cantidad, precio)

    def añadir_producto(self, producto):
        if producto.id in self.productos:
            print(f"Error: El producto con ID {producto.id} ya existe.")
            return False
        self.productos[producto.id] = producto
        self.cursor.execute("INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
                            (producto.id, producto.nombre, producto.cantidad, producto.precio))
        self.conn.commit()
        print(f"Producto {producto.nombre} añadido correctamente.")
        return True

    def eliminar_producto(self, id_producto):
        if id_producto not in self.productos:
            print(f"Error: No existe producto con ID {id_producto}.")
            return False
        del self.productos[id_producto]
        self.cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        self.conn.commit()
        print(f"Producto con ID {id_producto} eliminado correctamente.")
        return True

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        if id_producto not in self.productos:
            print(f"Error: No existe producto con ID {id_producto}.")
            return False
        producto = self.productos[id_producto]
        if cantidad is not None:
            producto.cantidad = cantidad
        if precio is not None:
            producto.precio = precio
        self.cursor.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
                            (producto.cantidad, producto.precio, id_producto))
        self.conn.commit()
        print(f"Producto con ID {id_producto} actualizado correctamente.")
        return True

    def buscar_producto_por_nombre(self, nombre_buscar):
        resultados = [p for p in self.productos.values() if nombre_buscar.lower() in p.nombre.lower()]
        if resultados:
            print(f"Productos que coinciden con '{nombre_buscar}':")
            for p in resultados:
                print(p)
        else:
            print(f"No se encontraron productos con nombre que contenga '{nombre_buscar}'.")

    def mostrar_todos_los_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
            return
        print("Inventario completo:")
        for producto in self.productos.values():
            print(producto)

    def cerrar(self):
        self.conn.close()


# Función para mostrar el menú y manejar la interacción con el usuario
def menu():
    inventario = Inventario()

    while True:
        print("\n--- Menú de Gestión de Inventario ---")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad o precio de un producto")
        print("4. Buscar productos por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id_producto = int(input("Ingrese ID del producto (número entero): "))
                nombre = input("Ingrese nombre del producto: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.añadir_producto(producto)
            except ValueError:
                print("Error: Entrada inválida. Asegúrese de ingresar números para ID, cantidad y precio.")

        elif opcion == "2":
            try:
                id_producto = int(input("Ingrese ID del producto a eliminar: "))
                inventario.eliminar_producto(id_producto)
            except ValueError:
                print("Error: ID debe ser un número entero.")

        elif opcion == "3":
            try:
                id_producto = int(input("Ingrese ID del producto a actualizar: "))
                cantidad_input = input("Ingrese nueva cantidad (deje vacío para no cambiar): ")
                precio_input = input("Ingrese nuevo precio (deje vacío para no cambiar): ")

                cantidad = int(cantidad_input) if cantidad_input.strip() != "" else None
                precio = float(precio_input) if precio_input.strip() != "" else None

                if cantidad is None and precio is None:
                    print("No se ingresaron cambios.")
                else:
                    inventario.actualizar_producto(id_producto, cantidad, precio)
            except ValueError:
                print("Error: Cantidad y precio deben ser números válidos.")

        elif opcion == "4":
            nombre_buscar = input("Ingrese nombre o parte del nombre a buscar: ")
            inventario.buscar_producto_por_nombre(nombre_buscar)

        elif opcion == "5":
            inventario.mostrar_todos_los_productos()

        elif opcion == "6":
            inventario.cerrar()
            print("Saliendo del programa. ¡Hasta luego!")
            break

        else:
            print("Opción inválida. Por favor, seleccione una opción del 1 al 6.")


if __name__ == "__main__":
    menu()
