import sqlite3
from nicegui import ui
from backend.listar_turnos_para_secretarias import listar_los_turnos


def eliminar_turno_seleccionado(tabla):

    # Verifica si hay una fila seleccionada
    if not tabla.selected:
        ui.notify('Seleccioná un turno', color='orange')
        return

    # Obtiene el ID del turno seleccionado
    id_turno = tabla.selected[0]['id']

    try:
        # Conexión a la base de datos
        conexion = sqlite3.connect('./src/backend/bdd.db')
        cursor = conexion.cursor()

        # Elimina el turno
        cursor.execute(
            'DELETE FROM turnos WHERE id = ?',
            (id_turno,)
        )

        conexion.commit()
        conexion.close()

        # Mensaje
        ui.notify('Turno eliminado correctamente', color='green')

        # Refresca la tabla
        tabla.rows = listar_los_turnos()
        tabla.update()

    except Exception as e:
        ui.notify(f'Error al eliminar turno: {e}', color='red')