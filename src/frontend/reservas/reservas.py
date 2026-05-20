from nicegui import ui, app
from datetime import date, timedelta
from backend.reservas.reserva_bdd import registrar_reserva, listar_reservas
import sqlite3

# Página de registar reserva
def pagina_reservas(tabs,reservas_tab,tabla_reservas):
    def formularioReserva():
        with ui.card().classes('w-150 p-6'):
            with ui.row().classes('w-full no-wrap gap-8 items-start'):
                with ui.column().classes('w-full items-center'):
                    fecha = ui.date().props(
                        ':options="date => { '
                        'const d = new Date(date.replace(/-/g, \'/\')); '
                        'const day = d.getDay(); '
                        'const today = new Date(); today.setHours(0,0,0,0); '
                        'const currentYear = new Date().getFullYear(); '
                        'return day !== 0 && day !== 6 && d > today && d.getFullYear() === currentYear; }'
                        '"'
                    )
                with ui.column().classes('w-3/5 gap-5'):
                    hora = ui.select(options=horas, label='Horario').classes('w-full')
                    obraSocial = ui.select(options=obrasSociales,label='Obra Social').classes('w-full')
                    metPago = ui.select(options=metodosPago,label='Método de Pago').classes('w-full')
                    tratamiento = ui.select(options=tratamientos,label='Tratamiento').classes('w-full')
            ui.button('Reservar turno',icon='event_available',
                      on_click=lambda: crearReserva(fecha,
                                                    hora,
                                                    tratamiento,
                                                    obraSocial,
                                                    metPago,
                                                    dniPaciente)
                                                    ).classes('w-full text-lg')
    
    def crearReserva(fecha,hora,trat,obraSoc,metPago,dniPac):
        if not fecha.value:
            ui.notify('Seleccione una fecha', color='warning')
            return
        if not hora.value:
            ui.notify('Seleccione una hora', color='warning')
            return
        if not obraSoc.value:
            ui.notify('Seleccione una obra social', color='warning')
            return
        if not metPago.value:
            ui.notify('Seleccione un método de pago', color='warning')
            return
        if not trat.value:
            ui.notify('Seleccione un tratamiento', color='warning')
            return
        try:
            registrar_reserva(fecha.value,hora.value,trat.value,obraSoc.value,metPago.value,dniPac)
            tabla_reservas.rows = listar_reservas(dniPac)
            tabla_reservas.update()
            ui.notify('Turno reservado con éxito',color='green')
            fecha.set_value(None)
            hora.set_value(None)
            obraSoc.set_value(None)
            metPago.set_value(None)
            trat.set_value(None)
            tabs.set_value(reservas_tab)
        except sqlite3.IntegrityError:
            ui.notify('Turno ya reservado', color='red')
        except Exception as e: # Verificar errores
            print(e)
### MOVER CONSTANTES A OTRO LADO
    dniPaciente = app.storage.user.get('dni')
    tratamientos=['Tren superior','Tren medio','Tren inferior']
    obrasSociales=['IOMA','OSDE','Ninguna']
    metodosPago=['Efectivo','Transferencia','Billetera virtual']
    horas = ['13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00']
####################################### PÁGINA ##################################################
    # Parte central
    with ui.row().classes('w-full justify-center'):
        formularioReserva()