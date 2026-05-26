import sqlite3
from src.utils.fetch_usuarios import existe, chequear_correo
from datetime import datetime
def registrar(dni, paswd, nom, ap, mail, fnac):
    """Recibe los datos del usuario a registrar, asume que las condiciones para registrar ya se cumplen"""
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("""
    INSERT INTO Usuarios (dni, contraseña, nombre, apellido, email, fechaNac, rol)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (dni, paswd, nom, ap, mail, fnac, "Paciente"))
    conexion.commit()
    conexion.close()
    
def cumple_edad(fecha_nacimiento):
    """Retorna True si la edad cumple con los requerimientos (es mayor de 13 años)"""
    fecha = datetime.strptime(fecha_nacimiento,'%Y-%m-%d')
    hoy = datetime.today()
    edad = hoy.year - fecha.year
    if (hoy.month, hoy.day) < (fecha.month, fecha.day):
        edad -= 1
    return edad > 13