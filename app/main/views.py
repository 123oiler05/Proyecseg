from flask import render_template, flash, current_app
from app.main import bp
from app.main.forms import ContactForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

#----------------------------------------------
from app.tasks import send_email_async


# Configura el nivel de logging (útil para auditoría)
logging.basicConfig(level=logging.INFO)

# === RUTA PRINCIPAL: Página de inicio con formulario de contacto ===
@bp.route('/')
def index():
    """
    Renderiza la página principal (index.html) con un formulario de contacto seguro.
    - El formulario incluye protección CSRF y reCAPTCHA.
    - No procesa datos aquí; solo muestra la interfaz.
    """
    form = ContactForm()
    return render_template('index.html', form=form)

# === NUEVA RUTA: Política de Privacidad ===
@bp.route('/privacy')
def privacy():
    """
    Renderiza la página de Política de Privacidad.
    - Es una página estática: no recibe datos, no tiene lógica compleja.
    - Cumple con principios de transparencia y normativas como la LFPDPPP (México).
    - No introduce riesgos de seguridad (no hay entrada de usuario).
    """
    return render_template('privacy.html')

# === RUTA DE PROCESAMIENTO: Envío del formulario de contacto ===
@bp.route('/contact', methods=['POST'])
@current_app.limiter.limit("5 per minute", methods=["POST"])
def contact():
    """
    Procesa el formulario de contacto con validación segura.
    - Valida campos, CSRF y reCAPTCHA mediante Flask-WTF.
    - Registra cada intento en los logs (auditoría).
    - Envía el mensaje por correo usando SMTP autenticado.
    """
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message_body = form.message.data

        # Registro para auditoría (IP, timestamp, etc. se pueden agregar después)
        logging.info(f"Nuevo mensaje de contacto de: {email}")

        #------------------------------------------------
        # Prepara la configuración para pasarla (como vimos en pasos anteriores)
        mail_config = {
            'MAIL_SERVER': current_app.config['MAIL_SERVER'],
            'MAIL_PORT': current_app.config['MAIL_PORT'],
            'MAIL_USERNAME': current_app.config['MAIL_USERNAME'],
            'MAIL_PASSWORD': current_app.config['MAIL_PASSWORD']
        }

        # Llama a la tarea con .delay() (Esto es instantáneo)
        send_email_async.delay(name, email, message_body, mail_config)

        flash('¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.', 'success')
        # Ya no necesitas el try/except aquí porque el error (si ocurre) sucederá en el worker, no aquí.
        #-----------------------------------------------------------



        try:
            send_email(name, email, message_body)
            flash('¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.', 'success')
        except Exception as e:
            logging.error(f"Error al enviar correo: {str(e)}")
            flash('Hubo un error al enviar el mensaje. Por favor, inténtalo más tarde.', 'danger')

        # Renderiza de nuevo index.html con un formulario limpio (patrón seguro)
        return render_template('index.html', form=ContactForm())
    else:
        # Si hay errores de validación (incluyendo reCAPTCHA), los muestra
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error: {error}", 'warning')
        return render_template('index.html', form=form)


"""
# === FUNCIÓN AUXILIAR: Envío seguro de correo ===
def send_email(name, email, message_body):
    
    msg = MIMEMultipart()
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = 'maramula753@gmail.com'  # ← Correo correcto según tu HTML original
    msg['Reply-To'] = email
    msg['Subject'] = f"Nuevo mensaje de contacto de {name}"

    body = f"Nombre: {name}\nCorreo: {email}\n\nMensaje:\n{message_body}"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # Conexión segura con el servidor SMTP
    server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
    server.starttls()
    server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

"""