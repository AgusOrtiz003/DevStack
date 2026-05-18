from nicegui import ui

# Acá irian todos los import de páginas .py que se tienen que ejecutar
from backend import modificar_turno
from frontend.pages import home
# Importar páginas de reserva
from frontend.pages.reservas import cancelar_reserva,listar_reservas,modificar_reserva,registar_reserva
# Importar páginas de turnos
from frontend.pages.turnos import listar_turnos,NO_USAR_registar_turno

ui.run(language='es')

