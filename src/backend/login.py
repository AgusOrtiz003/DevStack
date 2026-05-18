import sqlite3
def chequearContraseña(dni, contraseña):
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("SELECT contraseña FROM Usuarios WHERE dni=?", (dni,))
    resultado = cur.fetchone()
    conexion.close()
    if resultado is not None and str(resultado[0]) == str(contraseña):
        return True
    else:
        return False