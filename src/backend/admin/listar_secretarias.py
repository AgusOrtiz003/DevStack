import sqlite3


def obtener_secretarias():

    conn = sqlite3.connect(
        'src/backend/bdd.db'
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            dni,
            nombre,
            apellido,
            email,
            fechaNac,
            rol
        FROM Usuarios
        WHERE rol = 'Secretaria'
        ORDER BY apellido, nombre
    """)

    secretarias = cursor.fetchall()

    conn.close()

    return secretarias