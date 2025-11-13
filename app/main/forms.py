from flask_wtf import FlaskForm  #libreria para validar entradas
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[
        DataRequired("El nombre es obligatorio."),
        Length(min=2, max=50, message="El nombre debe tener entre 2 y 50 caracteres.")
    ])
    email = StringField('Correo electrónico', validators=[
        DataRequired("El correo es obligatorio."),
        Email("Formato de correo inválido.")
    ])
    message = TextAreaField('Mensaje', validators=[
        DataRequired("El mensaje es obligatorio."),
        Length(min=10, max=1000, message="El mensaje debe tener entre 10 y 1000 caracteres.")
    ])
    recaptcha = RecaptchaField()