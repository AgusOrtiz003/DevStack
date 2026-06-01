import sqlite3
from src.utils.fetch_usuarios import existe, chequear_correo
from datetime import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def registrar(dni, paswd, nom, ap, mail, fnac):
    """Recibe los datos del usuario a registrar, asume que las condiciones para registrar ya se cumplen"""
    conexion = sqlite3.connect('./src/backend/bdd.db')
    cur = conexion.cursor()
    cur.execute("""
    INSERT INTO Usuarios (dni, contraseña, nombre, apellido, email, fechaNac, rol)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (dni, paswd, nom, ap, mail, fnac, "Paciente"))
    conexion.commit()
    conexion.close()

def cumple_edad(fecha_nacimiento):
    """Retorna True si la edad cumple con los requerimientos (es mayor de 13 años)"""
    fecha = datetime.strptime(fecha_nacimiento,'%Y-%m-%d')
    hoy = datetime.today()
    edad = hoy.year - fecha.year
    if (hoy.month, hoy.day) < (fecha.month, fecha.day):
        edad -= 1
    return edad >= 13

import smtplib

from pathlib import Path

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


import smtplib

from pathlib import Path

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def enviar_mail(destinatario, nombre, apellido):

    remitente = "devstackar@gmail.com"
    password = "vdzq kgwg djfa uyqn"

    asunto = "Registro exitoso"

    mensaje_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">

        <div style="font-size: 20px;">

            <p>Hola <b>{nombre} {apellido}</b>.</p>

            <p>Tu cuenta fue registrada correctamente.</p>

            <p>Gracias por usar nuestra aplicación.</p>

        </div>

        <br><br>

        <table>
            <tr>
                <td>
                    <img src="cid:logo_kinepro" width="250">
                </td>

                <td style="padding-left: 25px;">
                    <img src="cid:logo_ser" width="180">
                </td>
            </tr>
        </table>

    </body>
    </html>
    """

    msg = MIMEMultipart('related')

    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    msg.attach(
        MIMEText(
            mensaje_html,
            'html'
        )
    )

    try:

        # =========================
        # Logo KinePro
        # =========================

        logo_kinepro_path = (
            Path(__file__).parent.parent
            / 'frontend'
            / 'icons'
            / 'kinePro-logo.png'
        )

        with open(logo_kinepro_path, 'rb') as f:

            logo_kinepro = MIMEImage(
                f.read()
            )

        logo_kinepro.add_header(
            'Content-ID',
            '<logo_kinepro>'
        )

        logo_kinepro.add_header(
            'Content-Disposition',
            'inline',
            filename='kinePro-logo.png'
        )

        msg.attach(
            logo_kinepro
        )

        # =========================
        # Logo SER
        # =========================

        logo_ser_path = (
            Path(__file__).parent.parent
            / 'frontend'
            / 'icons'
            / 'LogoSER.jpeg'
        )

        with open(logo_ser_path, 'rb') as f:

            logo_ser = MIMEImage(
                f.read()
            )

        logo_ser.add_header(
            'Content-ID',
            '<logo_ser>'
        )

        logo_ser.add_header(
            'Content-Disposition',
            'inline',
            filename='LogoSER.jpeg'
        )

        msg.attach(
            logo_ser
        )

        # =========================
        # Envío SMTP
        # =========================

        servidor = smtplib.SMTP(
            'smtp.gmail.com',
            587
        )

        servidor.starttls()

        servidor.login(
            remitente,
            password
        )

        servidor.send_message(
            msg
        )

        servidor.quit()

        print(
            'Mail enviado correctamente'
        )

    except Exception as e:

        print(
            'Error enviando mail:',
            e
        )