from flask import Flask, url_for, session, request, redirect, render_template
#* Importación Paquete con la clase
from paquete.Sorteos import Sorteos
#*Random
import random
#* CSV
import csv
# *Importar MONGO DB
from pymongo import MongoClient
#* Libreria Documentación
import doctest
#* necesitamos esta libreria que nos ayudará con el if main.
import os


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
db = client['examen_m4_c3']

# * Creacion coleccion EMAIL, donde estarán los registros de email de los usuarios para el sorteo
collectionEmail = db['collectionEmail']

# * Creacion coleccion
collectionSorteos = db['collectionSorteos']



#*******************************************

#* Objeto
# objetoClase = nombreClase(collection, session['usuario])


#*******************************************

# * Coleccion con la información de la Inmobiliaría

# ******************************************
#* RUTE REDIRECCIONAR
@app.route('/')
def redireccionar():

    """
    RUTA REDIRECCIONAR A LA RUTA HOME
    """

    return redirect(url_for('home'))

# ******************************************
#* RUTE HOMRE
@app.route('/home')
def home():

    """
    RUTA HOME
    """

    if 'email' in session:

        print(f'todavía existe la session: ' + session['email'])

        return render_template('home.html', email_existe=True, email=session['email'])

    else:

        return render_template('home.html', email_existe=False)

    return render_template('home.html')

# ******************************************
#* Si tienes SESSION, que cuando vuelva a HOME, toda la sección que tengas se borre, en este
#* caso es con POST, es decir, que según la página en la que estes, el boton para volver a home.html
# #* debe tener un FORM de POST.
#* Por sí lo necesitas
@app.route('/home', methods=['GET', 'POST'])
def homeDatos():

    """
    LLEGADA DE DATOS A LA RUTA HOME, ESTO ES PARA PODER LIMPIAR LA SESSION CUANDO VUELVAN A HOME A TRAVEZ DE LA APLICACIÓN.
    """

    if request.method == 'POST':

        session.clear()

    return render_template('home.html')

#************************************************

#* Login por si lo necesitas
#* Solo le falta la contraseña, simplemente sería agregarsela
@app.route('/usuario')
def usuario():

    """
    RUTA USUARIO, PARA INGRESAR EL LOGIN. USUARIO Y CONTRAÑESA, O SOLO USUARIO DEPENDIENDO DEL CASO
    """

    return render_template('usuario.html')



#************************************************

#* Login por si lo necesitas
@app.route('/usuario', methods=['GET'])
def usuarioGet():

    """
    RUTA USUARIO, PARA INGRESAR EL LOGIN. USUARIO Y CONTRAÑESA, O SOLO USUARIO DEPENDIENDO DEL CASO
    """

    if request.method == 'GET':

        session.clear()

    return render_template('usuario.html')

# ******************************************
@app.route('/usuario', methods=['POST'])
def usuariodatos():

    """
    LLEGADA DATOS DE USUARIO, CON LOS DATOS DEL LOGIN, PARA PODER INGRESAR A LA APLICACIÓN EN SÍ.
    """

    # * Lista que almacena al usuario
    listaemailCorrecto = []

    email = request.form['email']

    leer_email = collectionEmail.find({'email': f'{email}'})

    # print(list(leer_usuario))

    for i in leer_email:

        print(i['email'])
        listaemailCorrecto.extend([i['email'], str(i['_id'])])

    # print(listaUsuarioCorrecto[0])

    if listaemailCorrecto != []:

        if listaemailCorrecto[0] == email:
            # * iniciar sesion
            # * Limpiamos la session cada vez que haga una nueva session.
            session.clear()
            session['email'] = email
            session['email_id'] = listaemailCorrecto[1]
            print('session creada')

            agregarEmail_id = collectionEmail.update_one({'email': f'{email}'}, {'$set': {'email_id': listaemailCorrecto[1]}})

            return redirect(url_for('home'))

        else:

            return render_template('usuario.html', no_email=True)
    else:

        return render_template('usuario.html', no_email=True)

    return render_template('usuario.html')


# ******************************************
@app.route('/registro')
def registro():

    """
    RUTA REGISTRO, PARA REGISTRARSE EN LA APLICACIÓN
    """

    return render_template('registro.html')


# ******************************************
@app.route('/registro', methods=['GET', 'POST'])
def registroDatos():

    """
    LLEGADA DE DATOS A LA RUTA REGISTRO. PARA REGISTRAR AL USUARIO EN LA APLICACIÓN
    """

    if request.method == 'POST':

        email = request.form['email']

        leer_email = collectionEmail.find({'email': f'{email}'})

        # print(list(leer_usuario))

        # * Si en la BD no esta vacio, entonces el email que se ingreso en el input existe en la BD
        if list(leer_email) != []:

            return render_template('registro.html', correo_existe=True)

        collectionEmail.insert_one({"email": email})

        agregarEmail_id = collectionEmail.update_one({'email': f'{email}'}, {'$set': {'email_id': session['email_id']}})

        return redirect(url_for('home'))

    return render_template('registro.html')


# ******************************************


@app.route('/listaSorteos')
def listaSorteos():

    """
    RUTA NOMBRERUTA, TE PERMITE
    """

    return render_template('listaSorteos.html')


# ******************************************


@app.route('/listaSorteos', methods=['POST'])
def listaSorteosDatos():

    """
    RUTA NOMBRERUTA, TE PERMITE
    """

    #* Input hidden, de agregar sorteos para mantener actualizados los sorteso con el mes y fechas correspondientes.
    #* Es decir, nos ayudará para que el codigo del método ListaSorteos() pueda hacer la parte de agregar los sorteos si no lo están
    actualizarFechasSorteos = request.form['agregarSorteos']

    #* objeto de la clase Sorteos
    objSorteos = Sorteos(collectionSorteos, session['email'], session['email_id'])

    #* metodo para agregar sorteos
    (mensaje, listaConSorteos, condicionarparticipacion) = objSorteos.listaSorteos(actualizarFechasSorteos)


    
    return render_template('listaSorteos.html', mensaje=mensaje, listaSorteos=listaConSorteos, participacion=condicionarparticipacion)

#*******************************************

@app.route('/sorteo')
def sorteo():

    """
    RUTA NOMBRERUTA, TE PERMITE
    """

    return render_template('sorteo.html')


# ******************************************


@app.route('/sorteo', methods=['POST'])
def sorteoDatos():

    """
    RUTA NOMBRERUTA, TE PERMITE
    """

    #* input hidden
    participar = request.form['participar']

    #* input con las fechas de la semana:

    semana = request.form['semana']

    #?????????????????????????????????????????????????????????

    #* objeto de la clase Sorteos
    objSorteos = Sorteos(collectionEmail, session['email'], session['email_id'])

    #* metodo para agregar sorteos
    (mensaje, listaUsuarios) = objSorteos.sorteo(participar, semana)

    return render_template('sorteo.html', mensaje=mensaje, usuarios=listaUsuarios)

#*******************************************

#* Si necesitas más rutas, copia y pega estas dos plantillas de rutas

# @app.route('/nuevaRuta')
# def nuevaRuta():

    """
    RUTA NOMBRERUTA, TE PERMITE
    """

#     return render_template('nuevaRuta.html')


# ******************************************


# @app.route('/nuevaRuta', methods=['POST'])
# def nuevaRutaDatos():

    """
    RUTA NOMBRERUTA, TE PERMITE
    """

# return render_template('nuevaRuta.html')

# ******************************************
#*PAGE ERROR
@app.errorhandler(404)
def page_no_found(error):

    """
    RUTA DE 'PAGINA NO ENCONTRADA', POR SI ALGUIEN PONE LA RUTA DE URL MAL.
    """
    return '<h1> Pagina no encontrada, siga buscando</h1>'


# ******************************************
#*MAIN
if __name__ == "__main__":

    """
    MAIN, PARA INICIAR MAIN.PY
    """
    #* FORMA MAIN CON DOCKER
    # app.run('0.0.0.0', '5000', debug=True)
    #* Como funciona?R/: Basicamente estamos definiendo el puerto local, 
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)