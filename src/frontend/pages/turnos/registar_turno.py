from nicegui import ui
import sqlite3
from datetime import datetime
from backend import registrar_turno

# Página de registrar turnos
@ui.page('/registrarTurno')
def pagina_registar_turno():
    
    def registar_turno():
        if not fecha.value:
            ui.notify('Seleccione una fecha',color='negative')
        return
        if not hora.value:
            ui.notify('Seleccione una hora',color='negative')
        return
        if not tratamiento.value:
            ui.notify('Seleccione un tratamiento',color='negative')
        return
        if not kinesiologo.value:
            ui.notify('Seleccione al menos un kinesiólogo',color='negative')
        return
        registrar_un_turno(fecha.value,hora.value,tratamiento.value,cupoMaximo.value)
        ui.notify('Turno registrado correctamente',color='positive')

    # Esta función debería estar en otro lado
    def consultar_kinesiologos():
        conexion = sqlite3.connect('bdd.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT nombre FROM kinesiologos')
        resultados = cursor.fetchall()
        conexion.close()
        return [fila[0] for fila in resultados]

        ui.notify('Turno registrado correctamente')
####################################### PÁGINA ##################################################
    ui.page_title('Registrar Turno')

    # Parte superior
    with ui.header().classes('items-center justify-between'):
        ui.button(icon='home',on_click=ui.navigate.back).props('flat color=white')
        with ui.row().classes('items-center gap-1'):
            ui.button(icon='account_circle').props('flat color=white')

    # Centro de la página        
    with ui.card().classes('w-[500px] fixed-center items-center'):
        with ui.row().classes('gap-8'):
            fecha = ui.input(label='Fecha').classes('w-50').props('type=date')
            hora = ui.input(label='Hora').classes('w-50').props('type=time')
        ui.select(consultar_kinesiologos(),label='Kinesiólogo/s a cargo',multiple=True).classes('w-full')
        with ui.row().classes('gap-8'):
            tratamiento = ui.select(['Tren superior','Tren medio','Tren inferior'],label='Tratamiento').classes('w-50')
            cupoMaximo = ui.number(label='Cupo',value=1,min=1).classes('w-50')
        ui.button('Registrar turno',icon='event',on_click=registrar_turno()).classes('mt-6 self-center px-8 w-full')
    