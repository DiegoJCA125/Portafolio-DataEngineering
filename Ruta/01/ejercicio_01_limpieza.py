import pandas  as pd

# EXTRAER DATOS
datos_ventas ={
    "producto": ["Laptop", "Mouse", "Teclado", "Monitor", "Mouse", None],
    "precio": [2500000, 45000, None, 900000, 45000, 120000],
    "cantidad":[1, 3, 2, "dos", 3, 1]      
}
df = pd.DataFrame(datos_ventas)

print("========== DATOS ORIGINALES ==========")
print(df)
print("\n")

df = df.dropna(subset=["producto"])
promedio_precio = df["precio"].mean()       

df["precio"] = df["precio"].fillna(promedio_precio)

df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
df["cantidad"] = df["cantidad"].fillna(0)

df = df.drop_duplicates()

df["total"] = df["precio"] * df["cantidad"]

print("========== DATOS LIMPIOS ==========")
print(df)

df.to_csv("ventas_limpias.csv", index=False)

print("\n Archivo 'ventas_limpias.csv generado con exito")