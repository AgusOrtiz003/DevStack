import sqlite3

def crear_tabla_usuarios():

    try:

        with sqlite3.connect('src/backend/bdd.db') as conexion:

            cursor = conexion.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dni TEXT NOT NULL,
                    contraseña TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    email TEXT NOT NULL,
                    fechaNac DATE NOT NULL,
                    rol TEXT NOT NULL
                )
            ''')

            conexion.commit()

            print(
                'Tabla Usuarios creada correctamente'
            )

    except Exception as e:

        print(
            f'Error al crear la tabla Usuarios: {e}'
        )