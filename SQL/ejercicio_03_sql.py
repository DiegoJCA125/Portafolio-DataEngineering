import sqlite3

conexion = sqlite3.connect("ventas.db")
cursor = conexion.cursor()

cursor.execute("DROP TABLE IF EXISTS ventas")
cursor.execute("DROP TABLE IF EXISTS clientes")
cursor.execute("DROP TABLE IF EXISTS vendedores")
cursor.execute("""
    CREATE TABLE clientes (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        ciudad TEXT
    )
""")

cursor.execute("""
    CREATE TABLE vendedores (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        cargo TEXT
    )
""")

cursor.execute("""
    CREATE TABLE ventas (
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER,
        vendedor_id INTEGER,
        producto TEXT,
        precio REAL,
        cantidad INTEGER,
        fecha TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (vendedor_id) REFERENCES vendedores(id)
    )
""")

cursor.executemany("INSERT INTO clientes VALUES (?, ?, ?)",[
    (1, "Ana Torres", "Bogotá"),
    (2, "Luis Gómez", "Medellín"),
    (3, "Marta Ruiz", "Cali"),
    (4, "Carlos Peña", "Bogotá"),
])

cursor.executemany("INSERT INTO vendedores VALUES (?, ?, ?)",[
    (1, "Sofía Ramírez", "senior"),
    (2, "Pedro León", "junior"),
])

cursor.executemany("INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?, ?)",[
    (1, 1, 1, "Laptop",   3200000.0, 1, "2026-01-05"),
    (2, 2, 2, "Mouse",       45000.0, 3, "2026-01-06"),
    (3, 1, 1, "Teclado",    120000.0, 2, "2026-01-10"),
    (4, 3, 2, "Monitor",    850000.0, 1, "2026-01-12"),
    (5, 2, 1, "Laptop",   3200000.0, 1, "2026-02-01"),
    (6, 4, 2, "Mouse",       45000.0, 5, "2026-02-03"),
    (7, 3, 1, "Teclado",    120000.0, 1, "2026-02-15"),
    (8, 1, 2, "Monitor",    850000.0, 2, "2026-02-20"),
])

conexion.commit()
print("Base de datos recreada con clientes, vendedores y ventas\n")

def mostrar(titulo, query):
    print(f"--- {titulo} ---")
    cursor.execute(query)
    for fila in cursor.fetchall():
        print(fila)
    print()

mostrar(
    "HAVING -> productos con ingresos totales mayores a 500.000",
    """
    SELECT producto, SUM(precio * cantidad) AS ingresos
    FROM ventas
    GROUP BY producto
    HAVING SUM(precio * cantidad > 500000)
    ORDER BY ingresos DESC
    """
)

mostrar(
    "Subconsulta -> ventas con precio mayor al promedio general",
    """
    SELECT producto, precio
    FROM ventas
    WHERE precio > (SELECT AVG(precio) FROM ventas)
    ORDER BY precio DESC
    """
)

mostrar(
    "Subconsulta -> clientes que gastan por encima del promedio",
    """
    SELECT c.nombre, SUM(v.precio * v.cantidad) AS gasto_total
    FROM ventas v
    JOIN clientes c ON v.cliente_id = c.id
    GROUP BY c.nombre
    HAVING SUM(v.precio * v.cantidad) > (
        SELECT AVG(gasto_por_cliente) FROM (
            SELECT SUM(precio * cantidad) AS gasto_por_cliente
            FROM ventas
            GROUP BY cliente_id
            )
        )
    )
    ORDER BY gasto_total DESC    
    """
)

mostrar(
    "JOIN multiple -> cada venta con cliente y vendedor que la atendio",
    """
    SELECT
        c.nombre AS cliente,
        vend.nombre AS vendedor,
        vend.cargo AS cargo_vendedor,
        v.producto,
        v.precio
    FROM ventas v
    JOIN clientes c ON v.cliente_id = c.id
    JOIN vendedores vend ON v.vendedor_id = vend.id
    ORDER BY vend.nombre
    """
)

mostrar(
    "JOIN multiple + FROUP BY -> ingresos totales por vendedor",
    """
    SELECT 
        vend.nombre AS vendedor,
        vend.cargo,
        SUM(v.precio * v.cantidad) AS ingresos_generados
    FROM ventas v
    JOIN vendedores vend ON v.vendedor_id = vend.id
    GROUP BY vend.nombre
    ORDER BY ingresos_generados DESC
    """
)

conexion.close()
print("Conexion cerrada.")