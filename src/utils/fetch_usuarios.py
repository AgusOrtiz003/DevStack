import sqlite3
import re
from nicegui import ui,app

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

def chequear_contraseña(dni, contraseña):
    '''Dado un dni y una contraseña, retorna si la contraseña es correcta para ese dni'''
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("SELECT contraseña FROM Usuarios WHERE dni=?", (dni,))
    resultado = cur.fetchone()
    conexion.close()
    if resultado is not None and str(resultado[0]) == contraseña:
        return True
    else:
        return False

def get_datos(dni):
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
    
def eliminar_cuenta(dni):
    
    if(existe(dni)):
        conexion = sqlite3.connect('./src/backend/bdd.db')
        cur = conexion.cursor()
        cur.execute("DELETE FROM Usuarios WHERE dni=?", (dni,))
        conexion.commit()
        conexion.close()
        logout()

def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')
        
def cambiar_correo(correo,dni):
    ''' Recibe por parametro un correo y DNI, procede a cambiar el correo a dicho DNI'''
    
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("UPDATE Usuarios SET email = ? WHERE dni= ?", (correo,dni))
    conexion.commit()
    conexion.close()
    
    
def chequear_correo(correo):
    '''Devuelve verdadero si existe ya el correo electronico a una cuenta '''
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("SELECT email FROM Usuarios WHERE email=?", (correo,))
    resultado = cur.fetchone()
    return resultado is not None

def verificar_correo(correo):
    '''Verifica que el correo respete un patron '''
    patron = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(patron, correo) is not None
