from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from database import db
from forms import Persona_form
from models import Persona

app=Flask(__name__)
#Configuracion para la base de datos
USER_DB='postgres'
PASS_DB='admin'
URL_DB='localhost'
NAME_DB='sap_flask_db'
FULL_URL_DB=f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'#CADENA DE CONEXION COMPLETA
app.config['SQLALCHEMY_DATABASE_URI']=FULL_URL_DB#cual es laconexion de la bd que va utilizar
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#inicializacion del objeto db sqlalchemy
#db=SQLAlchemy(app)refctorizamos esta variable
db.init_app(app)
#configuracion de flask-migrate
migrate=Migrate()
migrate.init_app(app,db)#de indicamos los dos parametro que es la app y la base ded
#Configuracion de flak-wtf osa el form
app.config['SECRET_KEY']='llave_maestra'






@app.route('/')
@app.route('/index')#se puede poner multiples rutas
@app.route('/index.html')#deben comenzar con una barra inclinada
def inicio():
    #listado de personas
    personas=Persona.query.all()#obtnemos toda la informacion dentro de esta tabla
    #personas.Persona.query.order_by(id)ordenamos con este metodo de pendiendo el como ordenamos dentro del corchetes
    total_personas=Persona.query.count()#Obtenemos la cantidad total de registros dentro de la tabla
    app.logger.debug(f'Listado de personas{personas}')
    app.logger.debug(f'Total de personas{total_personas}')

    return render_template('index.html',personas=personas,total_personas=total_personas)#lo enviamos ala pagina y los parametors
@app.route('/ver/<int:id>')
def ver_persona(id):
    #persona=Persona.query.get(id)#primera forma
    persona=Persona.query.get_or_404(id)#por si hay un error
    app.logger.debug(f' ver persona:{persona}')
    return render_template('detalle.html',persona=persona)
@app.route('/agregar',methods=['GET','POST'])
def agregar():
    persona=Persona()#Creamos una nueva clae de modelos  tipo perosna
    persona_form=Persona_form(obj=persona)#form es de formulario y debemos instaciar la clase de tipo models socializar
    if request.method=='POST':#preguntamos si el tipo de metodo es de tipo post importamos del objeto flask.request
        if persona_form.validate_on_submit():#preguntamos si el formulario si es valido solo si se hace elenvio del formulario
            persona_form.populate_obj(persona)#llenamos el objetos que persona que definimos de clase models
            app.logger.debug(f'Persona a insertar {persona}')
            #insertamos el nuevo registro
            db.session.add(persona)#mandamos a llamar el metodo db de base de datos y abrimos una session y lo add para añadir ala base dedatos
            db.session.commit()#guardamos la informacion en la base de datos
            return redirect(url_for('inicio'))#lo derijimos ala pagina una pagina especifica
    return render_template('agregar.html',forma=persona_form)
@app.route('/editar/<int:id>',methods=['GET','POST'])#tipos http get y post get para mostrar el formulario y edirtar un registro y posst para procear os datos
def editar(id):
    #Recuperamos el objeto  persona editar
    persona=Persona.query.get_or_404(id)#recuperamos la informacion con el id proporcionado
    persona_form=Persona_form(obj=persona)#asociamos nuestra base de datos a  nuesta clase form o formulario
    if request.method == 'POST':  # preguntamos si el tipo de metodo es de tipo post importamos del objeto flask.request
        if persona_form.validate_on_submit():  # preguntamos si el formulario si es valido solo si se hace elenvio del formulario
            persona_form.populate_obj(persona)  # llenamos el objetos que persona que definimos de clase models
            app.logger.debug(f'Persona a insertar {persona}')
            # editamos un nuevo registro solo se usa el commit
            db.session.commit()  # guardamos la informacion en la base de datos
            return redirect(url_for('inicio'))  # lo derijimos ala pagina una pagina especifica
    return  render_template('editar.html',forma=persona_form)
@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona=Persona.query.get_or_404(id)#Recuperamos los datos en la base de dato
    app.logger.debug(f'Registro a eliminar {persona}')#
    db.session.delete(persona)#Eliminar el registro de la base de datos
    db.session.commit()#guardamos los cambio s
    return redirect(url_for('inicio'))#redirigimos a ala pagina incial
