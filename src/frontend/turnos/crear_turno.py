from nicegui import ui
import sqlite3
from backend.kinesiologos.listar_kinesiologos import obtener_kinesiologos
from backend.turnos.listar_turnos import listar_los_turnos
from backend.turnos.crear_turno import crear_turno

def pagina_crear_turno(tabla_principal):

    def actualizar_listado():
        tabla_principal.rows = listar_los_turnos()
        tabla_principal.update()

    def crear_turno_pagina(fecha,hora,tratamiento,kinesiologos,cupo_max):
        if not fecha.value or not hora.value or not tratamiento.value or not kinesiologos.value:
            ui.notify('Seleccione todos los campos',color='red-500')
            return
        try:
            crear_turno(fecha.value,hora.value,tratamiento.value,cupo_max.value,kinesiologos.value)
            ui.notify('Turno registrado con éxito',color='green-500')
            actualizar_listado()
        except sqlite3.IntegrityError:
            ui.notify('Turno ya registrado',color='red-500')
        except ValueError:
            ui.notify('Kinesiólogo/s ya asignado/s en este horario',color='red-500')


    horarios = [
        '13:00',
        '14:00',
        '15:00',
        '16:00',
        '17:00',
        '18:00',
        '19:00',
        '20:00',
    ]

    tratamientos = [
        'Tren superior',
        'Tren medio',
        'Tren inferior',
    ]

    kinesiologos = {
        k[0]: f'{k[3]} {k[2]}'
        for k in obtener_kinesiologos()
    }

    with ui.row().classes('w-full justify-center'):
        with ui.card().classes('w-180'):
            with ui.row().classes('w-full no-wrap'):
                with ui.column().classes('w-full'):
                    fecha_select = ui.date().props(
                        ':options="date => { '
                        'const d = new Date(date.replace(/-/g, \'/\')); '
                        'const day = d.getDay(); '
                        'const today = new Date(); today.setHours(0,0,0,0); '
                        'const currentYear = new Date().getFullYear(); '
                        'return day !== 0 && day !== 6 && d > today && d.getFullYear() === currentYear; }'
                        '"'
                    ).classes('w-full')
                with ui.column().classes('w-full gap-4'):
                    hora_select = ui.select(
                        options=horarios,
                        label='Horario'
                    ).classes('w-full').props('outlined dense')

                    tratamiento_select = ui.select(
                        options=tratamientos,
                        label='Tratamiento'
                    ).classes('w-full').props('outlined dense')

                    kinesiologos_select = ui.select(
                        options=kinesiologos,
                        label='Kinesiólogo/s',
                        multiple=True,
                        with_input=True
                    ).classes('w-full').props('outlined dense use-chips clearable stack-label')

                    cupo_select = ui.number(
                        label='Cupo máximo',
                        value=10,
                        min=1,
                        max=20
                    ).classes('w-full').props('outlined dense')

                    ui.button(
                        'Crear turno',
                        on_click=lambda: crear_turno_pagina(fecha_select,hora_select,tratamiento_select,kinesiologos_select,cupo_select)
                    ).classes('w-full mt-auto')