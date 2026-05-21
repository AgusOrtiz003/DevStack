import sqlite3
from src.utils.fetch_usuarios import existe
def registrar(dni, paswd, nom, ap, mail, fnac):
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()

    if not existe(dni):
        cur.execute("""
        INSERT INTO Usuarios (dni, contraseña, nombre, apellido, email, fechaNac, rol)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (dni, paswd, nom, ap, mail, fnac, "Paciente"))

        conexion.commit()
        conexion.close()
        return True
    else:
        conexion.close()
        return False
