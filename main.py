from flask import Flask, url_for, session, request, redirect, render_template
from inmobiliaria.Inmobiliaria import Inmobiliaria
import random
import csv
# *Importar MONGO DB
from pymongo import MongoClient

# *DATOS BASE DE DATOS EN LA NUBE
'''
usuario: mongodb
contraseña:mongodb
'''

# * Intanciar Flask
app = Flask(__name__)

# * Crear un llave/clave secreta para SESSION
app.config['SECRET_KEY'] = 'SUPER SECRETO'

# **************************************
# * ULR Conexion
MONGO_URL_ATLAS = 'mongodb+srv://mongodb:mongodb@cluster0-l6v7e.mongodb.net/test?retryWrites=true&w=majority'

# * Establecer conexion
client = MongoClient(MONGO_URL_ATLAS, ssl_cert_reqs=False)

# * Creacion base de datos MongoDB
db = client['examen_m4_c2']

# * Creacion coleccion
collectionVivienda = db['viviendas']

# * Coleccion con la información de la Inmobiliaría

# ******************************************
@app.route('/')
def redireccionar():

    return redirect(url_for('home'))

# ******************************************


@app.route('/home')
def home():

    return render_template('home.html')

# ******************************************


@app.route('/crearFicha')
def crearFicha():

    return render_template('crearFicha.html')

# ******************************************


@app.route('/crearFicha', methods=['POST'])
def crearFichaDatos():

    # * Lista con datos de la coleccion de Viviendas
    listaVivienda = []
    #* '_id' se convertira en STRING para poder hacer el SESSION y hacer la actualización de las medidas, esto más adelante.
    id_string = ''

    # * Datos Propietario

    nombrePropietario = request.form['nombrePropietario']

    numeroPropietario = request.form['numeroPropietario']

    email = request.form['email']

    dni = request.form['dni']

    # * Datos Vivienda

    direccion = request.form['direccion']

    tipoVivienda = request.form['tipoVivienda']

    operacion = request.form['operacion']

    precio = request.form['precio']

    planta = request.form['planta']

    puerta = request.form['puerta']

    # * input hidden para generar el CREAR FICHa
    crear = 1

    #* Diccionario para buscar vivienda
    diccBuscador = {
        'datosPropietario.propietario':nombrePropietario,
        'datosPropietario.numero':numeroPropietario,
        'datosPropietario.dni':dni,
        'datosPropietario.email':email,
        'datosVivienda.direccion':direccion,
        'datosVivienda.tipovivienda':tipoVivienda,
        'datosVivienda.operacion':operacion,
        'datosVivienda.precio':precio,
        'datosVivienda.planta':planta,
        'datosVivienda.puerta':puerta
        }

    # * Datos de la vivienda, query a mongoDB
    leer_vivienda = collectionVivienda.find(diccBuscador)

    print(leer_vivienda)

    # print(list(leer_vivienda))

    for i in list(leer_vivienda):

        listaVivienda.append(i)
        # id_string = str(i['_id'])

    print(f'listaVivienda: {listaVivienda}')

    if listaVivienda != []:

        print('Ya esta registrada la vivienda')

        return render_template('crearFicha.html', vivienda_existe=True)

    
    nuevaVivienda = {
        'datosPropietario': {
            'propietario': nombrePropietario,
            'numero': numeroPropietario,
            'dni': dni,
            'email': email
        },
        'datosVivienda': {
            'direccion': direccion,
            'tipovivienda': tipoVivienda,
            'operacion': operacion,
            'precio': precio,
            'planta': planta,
            'puerta': puerta
        }
    }

    agregar_vivienda = collectionVivienda.insert_one(nuevaVivienda)

    #* Variable que tendra el query con el documento recien agregado, para extraerle el '_id' que se usara para el SESSION
    #* el cual me permiti´ra usarlo cuando actualice este documento con las medidas
    extraer_id = collectionVivienda.find(diccBuscador)

    listaVivienda.clear()

    for ext in list(extraer_id):

        listaVivienda.append(str(ext['_id']))

    #* variable que hará la query, que me permitirá agregarle 'id_vivienda', que lo usaré para medidas.html.
    agregarID = collectionVivienda.update_one(diccBuscador, {'$set': {'id_vivienda': listaVivienda[0]}})

    if listaVivienda != []:

        print('La lista ha sido limpiada, y se agrego el nuevo documento')
        print(listaVivienda)

        session['id_documento'] = listaVivienda[0]

    return render_template('crearFicha.html', crearFicha=crear)

# ******************************************


@app.route('/medidas')
def medidas():

    return render_template('medidas.html', id_session=session['id_documento'])

# ******************************************


@app.route('/medidas', methods=['POST'])
def medidasDatos():

    #* Datos medidas
    supTotal = request.form['superficieTotal']
    supHabitacion = request.form['superficieHabitacion']
    altura = request.form['altura']
    cocina = request.form['cocina']
    salaPrincipal = request.form['salaPrincipal']
    banyo = request.form['banyo']

    #* Diccionario con la información de las medidas que se convertira en un documento embebido.
    diccMedidas = {
        'superficieTotal':supTotal,
        'superficieHabitacion':supHabitacion,
        'altura':altura,
        'cocina':cocina,
        'salaPrincipal':salaPrincipal,
        'banyo':banyo
    }

    #* Variable que tiene el 'id_vivienda' del SESSION
    id_vivienda = session['id_documento']
    
    #* esta variable con el query que agregara al documento recien agregado las medidas que se enviaron.
    retomarDocumento = collectionVivienda.update_one({'id_vivienda': id_vivienda}, {'$set': {'medidasVivienda': diccMedidas}})



    return render_template('medidas.html')

# ******************************************


@app.route('/verFicha')
def verFicha():

    return render_template('verFicha.html')


# ******************************************
@app.errorhandler(404)
def page_no_found(error):
    return '<h1> Pagina no encontrada, siga buscando</h1>'


# ******************************************
if __name__ == "__main__":

    app.run('0.0.0.0', '5000', debug=True)
