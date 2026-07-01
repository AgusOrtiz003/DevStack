from backend.usuarios.crear_tabla_usuarios import crear_tabla_usuarios
from backend.kinesiologos.crear_tabla_kinesiologos import (
    crear_tabla_kinesiologos,
    crear_tabla_turnos_kinesiologos
)
from backend.listas_de_espera.crear_tablas_lista_espera import (
    crear_tablas_lista_espera,
    crear_tablas_lista_espera_recurrente
)
from backend.notificaciones.crear_tabla_notificaciones import (
    crear_tablas_notificaciones
)
from backend.pagos.crear_tabla_pagos import crear_tabla_pagos
from backend.reservas.crear_tabla_reservas import crear_tabla_reserva
from backend.reservas.crear_tabla_reservas_recurrentes import (
    crear_tabla_reservas_recurrentes
)
from backend.turnos.crear_tabla_turnos import crear_tabla_turnos


def crear_base_datos():
    crear_tabla_usuarios()
    crear_tabla_kinesiologos()
    crear_tabla_turnos()
    crear_tabla_turnos_kinesiologos()
    crear_tabla_reserva()
    crear_tabla_reservas_recurrentes()
    crear_tablas_lista_espera()
    crear_tablas_lista_espera_recurrente()
    crear_tablas_notificaciones()
    crear_tabla_pagos()

    print('Base de datos inicializada correctamente')