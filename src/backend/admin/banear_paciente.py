from nicegui import ui
import sqlite3


def modal_cambiar_estado_paciente():

    with ui.dialog() as dialog, ui.card():

        ui.label(
            'Cambiar estado de paciente'
        ).classes('text-h6')

        dni_input = ui.input(
            'DNI del paciente'
        ).props('type=number')

        def cambiar_estado():

            dni = dni_input.value

            if not dni:
                ui.notify(
                    'Ingrese un DNI',
                    color='negative'
                )
                return

            conn = sqlite3.connect(
                'src/backend/bdd.db'
            )

            cursor = conn.cursor()

            cursor.execute(
                '''
                SELECT id, nombre, apellido, rol
                FROM Usuarios
                WHERE dni = ?
                ''',
                (dni,)
            )

            usuario = cursor.fetchone()

            if not usuario:

                conn.close()

                ui.notify(
                    'No existe un usuario con ese DNI',
                    color='negative'
                )

                return

            id_usuario = usuario[0]
            nombre = usuario[1]
            apellido = usuario[2]
            rol_actual = usuario[3]

            if rol_actual == 'Administrador':

                conn.close()

                ui.notify(
                    'No se puede modificar el estado de un administrador',
                    color='negative'
                )

                return


            if rol_actual == 'Paciente':
                nuevo_rol = 'Baneado'

            elif rol_actual == 'Baneado':
                nuevo_rol = 'Paciente'

            else:

                conn.close()

                ui.notify(
                    f'El usuario tiene rol "{rol_actual}"',
                    color='warning'
                )

                return

            cursor.execute(
                '''
                UPDATE Usuarios
                SET rol = ?
                WHERE id = ?
                ''',
                (nuevo_rol, id_usuario)
            )

            conn.commit()
            conn.close()

            ui.notify(
                f'{nombre} {apellido}: {rol_actual} → {nuevo_rol}',
                color='positive'
            )

            dialog.close()

        with ui.row():

            ui.button(
                'Cancelar',
                on_click=dialog.close
            ).props('flat')

            ui.button(
                'Cambiar estado',
                icon='swap_horiz',
                on_click=cambiar_estado
            )

    dialog.open()