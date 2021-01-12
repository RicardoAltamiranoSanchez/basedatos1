from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Persona_form(FlaskForm):#clase para el form
    nombre=StringField('Nombre',validators=[DataRequired()])#Aqui ya es codigo html
    apellido=StringField('Apellido')
    email=StringField('Email',validators=[DataRequired()])
    enviar=SubmitField('Enviar')#este es para el boton