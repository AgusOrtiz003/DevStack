import sqlite3

conexion = sqlite3.connect('./src/back-end/bdd.db')
cur= conexion.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni STRING(8) NOT NULL,
    nombre STRING(255) NOT NULL,
    apellido STRING(255) NOT NULL,
    email STRING(255) NOT NULL,
    fechaNac DATE NOT NULL,
    rol STRING(10) NOT NULL
)
""")
conexion.commit()
conexion.close()