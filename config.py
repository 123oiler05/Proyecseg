import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-muy-larga-y-aleatoria'
    # Claves para Flask-WTF reCAPTCHA (¡nombres obligatorios!)
    RECAPTCHA_PUBLIC_KEY = '6Lf-vgMqAAAAAL56XPLBqHPDVJWGoaYYfhFC6EUf'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_SECRET_KEY') or '6Lf-vgMqAAAAAMJVc_ciVEm0-hfdI7zY61qNQWjT'

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')