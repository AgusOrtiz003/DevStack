#!/usr/bin/env python3

from nicegui import ui

from backend.kinesiologos.listar_kinesiologos import obtener_kinesiologos

# =========================
# FILTRAR DATOS
# =========================

def filtrar_kinesiologos(
    nombre='',
    apellido='',
    cuit=''
):

    datos = obtener_kinesiologos()

    filtrados = []

    for k in datos:
        k_cuit = str(k[1]).lower()
        k_nombre = str(k[2]).lower()
        k_apellido = str(k[3]).lower()

        coincide = True

        if nombre:
            if nombre.lower() not in k_nombre:
                coincide = False

        if apellido:
            if apellido.lower() not in k_apellido:
                coincide = False

        if cuit:
            if cuit.lower() not in k_cuit:
                coincide = False

        if coincide:
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

        def buscar():

            datos_filtrados = filtrar_kinesiologos(
                nombre=nombre_input.value or '',
                apellido=apellido_input.value or '',
                cuit=cuit_input.value or '',
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