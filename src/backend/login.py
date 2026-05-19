import sqlite3
def chequearContraseña(dni, contraseña):
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("SELECT contraseña FROM Usuarios WHERE dni=?", (dni,))
    resultado = cur.fetchone()
    conexion.close()
    if resultado is not None and resultado[0] == contraseña:
        return True
    else:
        return False

def getNombre(dni):
    conexion= sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("SELECT nombre FROM Usuarios WHERE dni=?", (dni,))
    resultado = cur.fetchone()
    conexion.close()
    return resultado[0]

def getRol(dni):
    conexion= sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("SELECT rol FROM Usuarios WHERE dni=?", (dni,))
    resultado = cur.fetchone()
    conexion.close()
    return resultado[0]