from pathlib import Path

import smtplib

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def enviar_mail_notificacion(
    destinatario,
    asunto,
    mensaje
):

    remitente = "devstackar@gmail.com"
    password = "vdzq kgwg djfa uyqn"

    mensaje_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">

        <div style="font-size: 18px;">

            <p>{mensaje}</p>

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

        with open(
            logo_kinepro_path,
            'rb'
        ) as f:

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

        with open(
            logo_ser_path,
            'rb'
        ) as f:

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
        # SMTP
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
            f'Notificación enviada a {destinatario}'
        )

        return True

    except Exception as e:

        print(
            f'Error enviando mail a {destinatario}: {e}'
        )

        return False