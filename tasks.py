# app/tasks.py

from app import celery # Importamos la instancia global de celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Configuramos el logger para este archivo
logger = logging.getLogger(__name__)

@celery.task  # <--- DECORADOR MÁGICO
def send_email_async(name, user_email, message_body, mail_config):
    """
    Tarea asíncrona para enviar correos.
    Recibe la configuración de correo como argumento para evitar problemas de contexto.
    """
    logger.info(f"Iniciando tarea de envío de correo a: {user_email}")

    msg = MIMEMultipart()
    msg['From'] = mail_config['MAIL_USERNAME']
    msg['To'] = 'maramula753@gmail.com'
    msg['Reply-To'] = user_email
    msg['Subject'] = f"Nuevo mensaje de contacto de {name}"

    body = f"Nombre: {name}\nCorreo: {user_email}\n\nMensaje:\n{message_body}"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        # Usamos la configuración pasada como argumento
        server = smtplib.SMTP(mail_config['MAIL_SERVER'], mail_config['MAIL_PORT'])
        server.starttls()
        server.login(mail_config['MAIL_USERNAME'], mail_config['MAIL_PASSWORD'])
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        logger.info("Correo enviado exitosamente.")
        return "Enviado"
    except Exception as e:
        logger.error(f"Fallo al enviar correo: {str(e)}")
        # Aquí podrías configurar reintentos automáticos si falla
        raise e