import sqlite3

def existe(dni):
    '''Dado un dni retorna si existe o no en la base de datos'''
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()

    cur.execute("""
    SELECT * FROM Usuarios WHERE dni = ?
    """, (dni,))

    resultado = cur.fetchone()

    conexion.close()

    return resultado is not None

def chequearContraseña(dni, contraseña):
    '''Dado un dni y una contraseña, retorna si la contraseña es correcta para ese dni'''
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("SELECT contraseña FROM Usuarios WHERE dni=?", (dni,))
    resultado = cur.fetchone()
    conexion.close()
    if resultado is not None and resultado[0] == contraseña:
        return True
    else:
        return False
    
def getDatos(dni):
    '''Dado un dni, retorna un diccionario con los datos del usuario'''
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("SELECT dni, nombre, apellido, email, fechaNac, rol FROM Usuarios WHERE dni=?", (dni,))
    resultado = cur.fetchone()
    conexion.close()
    if resultado is not None:
        return {
            'dni': resultado[0],
            'nombre': resultado[1],
            'apellido': resultado[2],
            'email': resultado[3],
            'fechaNac': resultado[4],
            'rol': resultado[5]
        }
    else:
        return None