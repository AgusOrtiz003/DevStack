from nicegui import ui
import sqlite3


def modal_buscar_pacientes(callback):

    with ui.dialog() as dialog, ui.card():

        ui.label(
            'Buscar pacientes'
        ).classes('text-h6')

        filtro = ui.select(
            [
                'Nombre',
                'Apellido',
                'DNI',
                'Email'
            ],
            value='Nombre',
            label='Buscar por'
        )

        valor = ui.input(
            'Valor'
        )

        def buscar():

            conn = sqlite3.connect(
                'src/backend/bdd.db'
            )

            cursor = conn.cursor()

            texto = valor.value.strip()

            if filtro.value == 'Nombre':

                cursor.execute(
                    """
                    SELECT
                        dni,
                        nombre,
                        apellido,
                        email,
                        fechaNac,
                        rol
                    FROM Usuarios
                    WHERE rol IN ('Paciente', 'Baneado')
                    AND nombre LIKE ?
                    ORDER BY apellido, nombre
                    """,
                    (f'%{texto}%',)
                )

            elif filtro.value == 'Apellido':

                cursor.execute(
                    """
                    SELECT
                        dni,
                        nombre,
                        apellido,
                        email,
                        fechaNac,
                        rol
                    FROM Usuarios
                    WHERE rol IN ('Paciente', 'Baneado')
                    AND apellido LIKE ?
                    ORDER BY apellido, nombre
                    """,
                    (f'%{texto}%',)
                )

            elif filtro.value == 'DNI':

                cursor.execute(
                    """
                    SELECT
                        dni,
                        nombre,
                        apellido,
                        email,
                        fechaNac,
                        rol
                    FROM Usuarios
                    WHERE rol IN ('Paciente', 'Baneado')
                    AND CAST(dni AS TEXT) LIKE ?
                    ORDER BY apellido, nombre
                    """,
                    (f'%{texto}%',)
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        dni,
                        nombre,
                        apellido,
                        email,
                        fechaNac,
                        rol
                    FROM Usuarios
                    WHERE rol IN ('Paciente', 'Baneado')
                    AND email LIKE ?
                    ORDER BY apellido, nombre
                    """,
                    (f'%{texto}%',)
                )

            resultados = cursor.fetchall()

            conn.close()

            callback(resultados)

            dialog.close()

        with ui.row():

            ui.button(
                'Cancelar',
                on_click=dialog.close
            ).props('flat')

            ui.button(
                'Buscar',
                icon='search',
                on_click=buscar
            )

    dialog.open()