
#Crear clase modelo
from app import db


class Persona(db.Model):#Creamo la clase modelo para la base de datos funcion model
    id=db.Column(db.Integer, primary_key=True)#para crear las columnas en la base de datos
    nombre=db.Column(db.String(255))
    apellido=db.Column(db.String(255))
    email=db.Column(db.String(255))
    def __str__(self):
        return(f'Id:{self.id},'
               f'Nombre:{self.nombre},'
               f'Apellido:{self.apellido},'
               f'Email:{self.email}')