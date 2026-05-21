#!/usr/bin/env python3

from nicegui import ui

from backend.kinesiologos.listarKinesiologos import (
    obtener_kinesiologos
)

# =========================
# HORARIOS
# =========================

HORARIOS = [
    "08:00","09:00","10:00","11:00","12:00",
    "13:00","14:00","15:00","16:00","17:00",
    "18:00","19:00","20:00"
]

# =========================
# FILTRAR DATOS
# =========================

def filtrar_kinesiologos(
    nombre='',
    apellido='',
    cuit='',
    hora_desde='',
    hora_hasta=''
):

    datos = obtener_kinesiologos()

    filtrados = []

    for k in datos:

        k_cuit = str(k[0]).lower()
        k_nombre = str(k[1]).lower()
        k_apellido = str(k[2]).lower()
        k_hora_desde = str(k[3])
        k_hora_hasta = str(k[4])

        match_nombre = (
            nombre.lower() in k_nombre
        ) if nombre else True

        match_apellido = (
            apellido.lower() in k_apellido
        ) if apellido else True

        match_cuit = (
            cuit.lower() in k_cuit
        ) if cuit else True

        match_desde = (
            k_hora_desde >= hora_desde
        ) if hora_desde else True

        match_hasta = (
            k_hora_hasta <= hora_hasta
        ) if hora_hasta else True

        if (
            match_nombre
            and match_apellido
            and match_cuit
            and match_desde
            and match_hasta
        ):

            filtrados.append(k)

    return filtrados

# =========================
# MODAL BUSQUEDA
# =========================

def modal_buscar_kinesiologos(callback_actualizar_tabla):

    with ui.dialog() as dialog, ui.card().classes('w-96'):

        ui.label(
            'Buscar Kinesiólogo'
        ).classes(
            'text-xl font-bold'
        )

        nombre_input = ui.input(
            'Nombre'
        ).classes('w-full')

        apellido_input = ui.input(
            'Apellido'
        ).classes('w-full')

        cuit_input = ui.input(
            'CUIT'
        ).classes('w-full')

        hora_desde_input = ui.select(
            HORARIOS,
            label='Hora Desde'
        ).classes('w-full')

        hora_hasta_input = ui.select(
            HORARIOS,
            label='Hora Hasta'
        ).classes('w-full')

        # =====================
        # BUSCAR
        # =====================

        def buscar():

            # -----------------
            # VALIDAR HORAS
            # -----------------

            if (
                hora_desde_input.value
                and hora_hasta_input.value
                and hora_desde_input.value > hora_hasta_input.value
            ):

                ui.notify(
                    'Hora Desde no puede ser mayor que Hora Hasta',
                    color='negative'
                )

                return

            datos_filtrados = filtrar_kinesiologos(
                nombre=nombre_input.value or '',
                apellido=apellido_input.value or '',
                cuit=cuit_input.value or '',
                hora_desde=hora_desde_input.value or '',
                hora_hasta=hora_hasta_input.value or ''
            )

            callback_actualizar_tabla(
                datos_filtrados
            )

            dialog.close()

        # =====================
        # BOTONES
        # =====================

        with ui.row().classes(
            'w-full justify-end'
        ):

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