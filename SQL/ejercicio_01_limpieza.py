import sqlite3

conexion = sqlite3.connect("empresa.db")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        CIUDAD TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER,
        producto TEXT,
        monto REAL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
""")

conexion.commit()
print("Tablas creadas correctamente!")

cursor.execute("DELETE FROM clientes")
cursor.execute("DELETE FROM pedidos")

clientes_ejemplo = [
    (1, "Carlos Ramirez", "Armenia"),
    (2, "Laura Gomez", "Bogota"),
    (3, "Andres Torres", "Medellin"),
    (4, "Sofia Martinez", "Armenia")
]

cursor.executemany("INSERT INTO clientes (id, nombre, ciudad) VALUES (?, ?, ?)", clientes_ejemplo)

pedidos_ejemplo = [
    (1, 1, "Laptop", 2500000.0),
    (2, 1, "Mouse", 45000.0),
    (3, 2, "Teclado", 120000.0),
    (4, 3, "Monitor", 900000.0),
    (5, 1, "Monitor", 900000.0),
    (6, 4, "Laptop", 2500000.0)
]

cursor.executemany("INSERT INTO pedidos (id, cliente_id, producto, monto) VALUES (?, ?, ?, ?)", pedidos_ejemplo)

conexion.commit()
print("Datos de ejemplo insertados")

cursor.execute("""
    SELECT clientes.nombre, clientes.ciudad, pedidos.producto, pedidos.monto
    FROM pedidos
    JOIN clientes ON pedidos.cliente_id = clientes.id
    ORDER BY clientes.nombre
""")
resultados = cursor.fetchall()

print ("\n ----- PEDIDOS CON NOMBRE DE CLIENTE -----")
for fila in resultados:
    nombre, ciudad, producto, monto = fila
    print(f"{nombre} ({ciudad}) compro {producto} por ${monto:,.0f}")

cursor.execute("""
    SELECT clientes.nombre, COUNT(pedidos.id) as total_pedidos, SUM(pedidos.monto) AS total_gastado
    FROM pedidos
    JOIN clientes ON pedidos.cliente_id = clientes.id
    GROUP BY clientes.nombre
    ORDER BY total_gastado DESC
""")
resultados_agrupados = cursor.fetchall()

print("\n ---- TOTAL GASTADO POR CLIENTE ----")
for fila in resultados_agrupados:
    nombre, cantidad_pedidos, total = fila
    print(f"{nombre}: {cantidad_pedidos} pedidos, total ${total:,.0f}")

cursor.execute("""
    SELECT clientes.nombre, COUNT(pedidos.id) AS total_pedidos,  SUM(pedidos.monto) AS total_gastado
    FROM pedidos
    JOIN clientes ON pedidos.cliente_id = clientes.id
    GROUP BY clientes.nombre
    HAVING COUNT(pedidos.id) > 1
    ORDER BY total_gastado DESC
""")
resultados_frecuentes = cursor.fetchall()

print("\n ------ CLIENTES CON MAS DE 1 PEDIDO -----")
for fila in resultados_frecuentes:
    nombre, cantidad_pedidos, total = fila
    print(f"{nombre}: {cantidad_pedidos} pedidos, total ${total:,.0f}")
    
conexion.close()

