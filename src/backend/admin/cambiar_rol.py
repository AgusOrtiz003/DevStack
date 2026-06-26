import sqlite3

def cambiar_rol(dni, nuevoRol):
    '''Dado un dni y un nuevo rol, actualiza el rol del usuario en la base de datos'''
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("UPDATE Usuarios SET rol=? WHERE dni=?", (nuevoRol, dni))
    conexion.commit()
    conexion.close()