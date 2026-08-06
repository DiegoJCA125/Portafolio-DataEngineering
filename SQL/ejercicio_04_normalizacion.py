import sqlite3

conexion = sqlite3.connect("normalizacon.db")
cursor = conexion.cursor()

def mostrar(titulo, query):
    print(f" --- {titulo} --- ")
    cursor.execute(query)
    for fila in cursor.fetchall():
        print(fila)
    print()

cursor.execute("DROP TABLE IF EXISTS pedidos_planos")
cursor.execute("""
    CREATE TABLE pedidos_planos (
        pedido_id INTEGER PRIMARY KEY,
        cliente_nombre TEXT,
        cliente_ciudad TEXT,
        vendedor_nombre TEXT,
        vendedor_cargo TEXT,
        producto TEXT,
        precio REAL
    )
""")

cursor.executemany("INSERT INTO pedidos_planos VALUES (?, ?, ?, ?, ?, ?, ?)",[
    (1, "Ana Torres", "Bogotá", "Sofía Ramírez", "senior", "Laptop", 3200000.0),
    (2, "Ana Torres", "Bogotá", "Pedro León",    "junior", "Monitor", 850000.0),
    (3, "Luis Gómez",  "Medellín", "Sofía Ramírez", "senior", "Mouse", 45000.0),
])
conexion.commit()

mostrar("Tabla Plana -> se repetira los datos de Ana y Sofia","""
    SELECT * FROM pedidos_planos
""")

print(" -> PROBLEMA: si Ana Torres se muda a Calida, hay que encontrar Y")
print("--> Actualizar CADA fila donde apoarece 'Bogota' junto a su nombre")
print("--> Sik el sistema tiene miles de pedidos, es facil dejar alguno")
print("--> Se desactualiza -> datos inconsistences\n")

cursor.executemany("DROP TABLE IF EXISTS clientes")
cursor.executemany("DROP TABLE IF EXISTS vendedores")
cursor.executemany("DROP TABLE IF EXISTS pedidos")

cursor.execute("""
    CREATE TABLE clientes(
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE,
        ciudad TEXT
    )
""")

cursor.execute("""
    CREATE TABLE vendedores(
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE,
        cargo TEXT
    )
""")

cursor.execute("""
    CREATE TABLE pedidos(
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER,
        vendedor_id INTEGER,
        producto TEXT,
        precio REAL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (vendedor_id) REFERENCES vendedores(id)
    )
""")

cursor.execute("""
    INSERT OR IGNORE INTO clientes (ombre, ciudad)
    SELECT DISTINCT cliente_nombre, cliente_ciudad FROM pedidos_planos
""")

cursor.execute("""
    INSERT OR IGNORE INTO vendedores (nombre, cargo)
    SELECT DISTINCT vendedor_nombre, vendedor_cargo FROM pedidos_planos
""")

cursor.execute("""
    INSERT INTO pedidos (cliente_id, vendedor_ir, producto, precio)
    SELECT
        c.id,
        v.id,
        pp.producto,
        pp.precio
    FROM pedidos_planos pp
    JOIN clientes c ON pp.cliente_nombre = c.nombre
""")
conexion.commit()

print("DATOS MIGRADOS A LA ESTRUCTURA NORMALIZADA\n")
mostrar("clientes (cada cliente aparece UNA sola vez)", "SELECT * FROM clientes")
mostrar("vendedores (cada vendedor aparece UNA sola vez)", "SELECT * FROM vendedores")
mostrar("pedidos (solo guarda IDs, no texto repetido)", "SELECT * FROM pedidos")

cursor.execute("UPDATE clientes SET ciudad = 'Cali' WHERE nombre 'Ana Torres'")
conexion.commit()

mostrar(
    "Despues de UPDATE -> Un solo cambio se vera reglejado en todos los pedidos mediante el JOIN",
    """
    SELECT c.nombre, c.ciudad, p.producto, p.precio
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id
    WHERE c.nombre = 'Ana Torres'
    """
)

conexion.close()
print("CONEXION CERRADA")