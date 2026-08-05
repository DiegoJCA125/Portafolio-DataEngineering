import sqlite3
conexion = sqlite3.connect("ventas.db")
cursor = conexion.cursor()

cursor.execute("DROP TABLE IF EXISTS ventas")
cursor.execute("DROP TABLE IF EXISTS clientes")

cursor.execute("""
    CREATE TABLE clientes (
        id INTEGER PRIMARY KEY, 
        nombre TEXT NO NULL, 
        ciudad TEXT
    )
""")

cursor.execute("""
    CREATE TABLE ventas (
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER, 
        producto TEXT,
        precio REAL,
        cantidad INTEGER,
        fecha TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    )
""")
print("Tablas creadas correctamente \n")

clientes_data = [
    (1, "Ana Torres", "Bogotá"),
    (2, "Luis Gómez", "Medellín"),
    (3, "Marta Ruiz", "Cali"),
    (4, "Carlos Peña", "Bogotá"),
]
cursor.executemany("INSERT INTO clientes VALUES (?, ?, ?)", clientes_data)

ventas_data = [
    (1, 1, "Laptop",     3200000.0, 1, "2026-01-05"),
    (2, 2, "Mouse",         45000.0, 3, "2026-01-06"),
    (3, 1, "Teclado",      120000.0, 2, "2026-01-10"),
    (4, 3, "Monitor",      850000.0, 1, "2026-01-12"),
    (5, 2, "Laptop",      3200000.0, 1, "2026-02-01"),
    (6, 4, "Mouse",          45000.0, 5, "2026-02-03"),
    (7, 3, "Teclado",       120000.0, 1, "2026-02-15"),
    (8, 1, "Monitor",       850000.0, 2, "2026-02-20"),
]
cursor.executemany("INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?)", ventas_data)

conexion.commit()
print("Datos insertados correctamente\n")

def mostrar(titulo, query):
    """EJECUTA UNA QUERY Y MUESTRA EL TITULO + LOS RESULTADOS EN CONSOLA"""
    print(f"---- {titulo} ----")
    cursor.execute(query)
    filas = cursor.fetchall()

    for fila in filas:
        print(fila)
    print()

mostrar(
    "SELECT * -> todas las ventas",
    "SELECT * FROM ventas"
)

mostrar(
    "WHERE -> ventas de mas de 500.000",
    "SELECT producto, precio FROM ventas WHERE precio >500000"
)

mostrar(
    "ORDER BY + LIMIT -> las 3 ventas mas caras",
    "SELECT producto, precio FROM ventas ORDER BY precio DESC LIMIT 3"    
)

mostrar(
    "GROUP BY -> ingresos totales por producto",
    """
    SELECT
        producto,
        SUM(precio * cantidad) AS ingresos,
        COUNT(*) AS veces_vendido
    FROM ventas
    GROUP BY producto
    ORDER BY ingresos DESC
    """
)

mostrar(
    "JOIN -> que coompro cada cliente, con su nombre y ciudad",
    """
    SELECT
        clientes.nombre,
        clientes.ciudad,
        ventas.producto,
        ventas.precio
    FROM ventas
    JOIN clientes ON ventas.cliente_id = clientes.id
    ORDER BY clientes.nombre
    """
)

mostrar(
    "JOIN + GROUP BY -> gasto total por cliente",
    """
    SELECT
        clientes.nombre,
        clientes.ciudad,
        SUM(ventas.precio * ventas.cantidad) AS gasto_total
    FROM ventas
    JOIN clientes ON ventas.cliente_id = clientes.id
    GROUP BY clientes.nombre
    ORDER BY gasto_total DESC
    """
)

conexion.close()
print("Conexion cerrada")