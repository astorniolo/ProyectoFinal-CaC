from flask import Flask , jsonify, request
# del modulo flask importar la clase Flask y los métodos jsonify,request

from flask_cors import CORS # del modulo flask_cors importar CORS
# cors se ut siempre en un apiREST siempre que me conecte del front a una api
# da un error de seguridad asi siempre instalar cors

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# pqt  Alchemy y marshmallow son para manejo de DB
app=Flask(__name__) # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
#                                     !driver       ://usuario:clave@host/nombre
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://astorniolo:hepatalgina@astorniolo.mysql.pythonanywhere-services.com/astorniolo$default'
# URI de la BBDD driver de la BD user:clave@URLBBDD/nombreBBDD
# aca voy a tener que cambiae cuando pase el py a python anywhere

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app) #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app) #crea el objeto ma de de la clase Marshmallow


#---------------DEFINO LOS MODELOS DE LA BD-------------------------
# defino la tabla
class Drama(db.Model): # la clase Drama hereda de db.Model
    id=db.Column(db.Integer, primary_key=True) #define los campos de la tabla
    titulo=db.Column(db.String(100))
    episodios=db.Column(db.Integer)
    genero=db.Column(db.String(100))
    anio=db.Column(db.Integer)
    autor=db.Column(db.String(100))
    estrellas=db.Column(db.Integer)
    descripcion=db.Column(db.String(500))
    imagen=db.Column(db.String(100))
    
    def __init__(self,titulo,episodios,genero,anio,autor,estrellas,descripcion,imagen): #crea el constructor de la clase
        self.titulo=titulo # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.episodios=episodios
        self.genero=genero
        self.anio=anio
        self.autor=autor
        self.estrellas=estrellas
        self.descripcion=descripcion
        self.imagen=imagen
    

with app.app_context():
    db.create_all() # aqui crea todas las tablas
    # si las tablas estan creada python se aviva y no las crea
    
# ************************************************************
class DramaSchema(ma.Schema):
    #defino los campos de la tabla
    class Meta:
        fields=('id','titulo','episodios','genero','anio','autor','estrellas','descripcion','imagen')

# El objeto drama_schema es para traer un solo drama
drama_schema=DramaSchema() 
 # El objeto dramas_schema es para traer multiples registros de drama
dramas_schema=DramaSchema(many=True)

# ----------------------------------CONTROLADORES----------------
# ----------------------------------CONTROLADORES Drama
# crea los endpoint o rutas (json)
@app.route('/dramas',methods=['GET'])
def get_dramas():
    all_dramas=Drama.query.all() # el metodo query.all() lo hereda de db.Model
    result=dramas_schema.dump(all_dramas) # el metodo dump() lo hereda de ma.schema y
                                                # trae todos los registros de la tabla
    return jsonify(result) # retorna un JSON de todos los registros de la tabla

@app.route('/dramas/<id>',methods=['GET'])
def get_drama(id):
    drama=Drama.query.get(id)
    return drama_schema.jsonify(drama) # retorna el JSON de un drama recibido como parametro

@app.route('/dramas/<id>',methods=['DELETE'])
def delete_drama(id):
    drama=Drama.query.get(id)
    db.session.delete(drama)
    db.session.commit()
    return drama_schema.jsonify(drama) # me devuelve un json con el registro eliminado

@app.route('/dramas', methods=['POST']) # crea ruta o endpoint
def create_drama():
    #print(request.json) # request.json contiene el json que envio el cliente
    titulo=request.json['titulo'] 
    episodios=request.json['episodios']
    genero=request.json['genero']
    anio=request.json['anio']
    autor=request.json['autor']
    estrellas=request.json['estrellas']
    descripcion=request.json['descripcion']
    imagen=request.json['imagen']
    new_drama=Drama(titulo,episodios,genero,anio,autor,estrellas,descripcion,imagen)
    db.session.add(new_drama)
    db.session.commit()
    return drama_schema.jsonify(new_drama)

@app.route('/dramas/<id>' ,methods=['PUT'])
def update_drama(id):
    drama=Drama.query.get(id)
    drama.titulo=request.json['titulo'] 
    drama.episodios=request.json['episodios']
    drama.genero=request.json['genero']
    drama.anio=request.json['anio']
    drama.autor=request.json['autor']
    drama.estrellas=request.json['estrellas']
    drama.descripcion=request.json['descripcion']
    drama.imagen=request.json['imagen']
    db.session.commit()
    return drama_schema.jsonify(drama)


# programa principal *******************************
#ejecuta la aplicacion en el puerto 5000
if __name__=='__main__':
    app.run(debug=True, port=5000) # ejecuta el servidor Flask en el puerto 5000