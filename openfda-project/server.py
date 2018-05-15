from flask import request #Importamos este modulo para las peticiones
import http.client #Permite trabajar con lo relacionado con el cliente
import json #Permite trabajar de forma sencilla con archivos JSON
from flask import Flask,redirect,abort #Los importamos para poder realizar la extension lV de redireccion y autenticacion

app = Flask(__name__)


@app.route("/searchDrug") #Introducimos el punto de entrada
def buscar_drugs(): #definimos una función que nos permita obtener los ingredientes activos
    ingactivo = request.args.get('active_ingredient').replace(" ", "%20") #pedimos el ingrediente activo y sustituimos los espacios vacios por %20
    limit = request.args.get('limit')
    if limit: #En la pagina principal damos la opcion de meter un limite
        gestion = gestionopenfda("/drug/label.json?search=active_ingredient:"+ingactivo+"&limit="+limit)
        mi_html = informacion(gestion)
    else: #en caso de que la casilla del limite se deje vacia se devuelve por defecto 10
        gestion = gestionopenfda("/drug/label.json?search=active_ingredient:" + ingactivo + "&limit=10")
        mi_html = informacion(gestion)
    return mi_html
#se repite lo comentado
@app.route("/searchCompany") #Intrducimos punto de entrada, se buscan las empresas
def buscar_empresa():
    empresa = request.args.get('company').replace(" ", "%20")
    limit = request.args.get('limit')
    if limit:
        gestion1 = gestionopenfda1("/drug/label.json?search=manufacturer_name:"+empresa+"&limit="+limit)
        mi_html = informacion(gestion1)
    else:
        gestion1 = gestionopenfda1("/drug/label.json?search=manufacturer_name:" + empresa + "&limit=10")
        mi_html = informacion(gestion1)
    return mi_html

@app.route("/listDrugs") #Lista con medicamentos
def lista_medicamentos(): #En la pantalla aparece una casilla que permite introducir un limite de los medicamentos que se quiere que devuelva
    medicamentos = request.args.get('limit')
    gestion = gestionopenfda("/drug/label.json?&limit="+medicamentos)
    mi_html = informacion(gestion)
    return mi_html

@app.route("/listCompanies") #Lo mismo que lo anterior pero siendo una lista con los nombres de las empresas
def lista_empresas():
    empresas = request.args.get('limit')
    gestion1 = gestionopenfda1("/drug/label.json?&limit="+empresas)
    mi_html = informacion(gestion1)
    return mi_html

@app.route("/listWarnings") #Extension 1, obtenemos un listado con las advertencias de los farmacos
def lista_advertencias():
    adver = request.args.get('limit')
    warnings = advertencias("/drug/label.json?&limit="+adver)
    mi_html = informacion(warnings)
    return mi_html


def gestionopenfda(gestion): #Funcion que obtiene los datos de generic name de openfda
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov") #Establecer conexión con el servidor
    conn.request("GET", gestion, None, headers) #Enviar solicitud al servidor
    respuesta = conn.getresponse() #Obtener respuesta
    resp = respuesta.read().decode("utf-8") #Leer respuesta y descodificar en formato utf-8
    conn.close() #Cerrar la conexión al servidor
    datos = json.loads(resp) #Convierte un str de JSON en datos con estructura python, en concreto un diccionario

    drugs = "" #Almacenamos en la variable drugs los datos obtenidos
    if "results" in datos:
        for elem in datos['results']:
            if 'generic_name' in elem['openfda']:
                drugs += "<li>" + str(elem['openfda']['generic_name'][0]) +"</li>" #Usamos li para añadir puntos a la lista
            else:
                drugs += "<li>" + ("No encontrado") +"</li>"
                continue
    return drugs


def gestionopenfda1(gestion1): #Funcion que obtiene los datos de manufacturer name de openfda
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", gestion1, None, headers)
    respuesta = conn.getresponse()
    resp = respuesta.read().decode("utf-8")
    conn.close()
    datos = json.loads(resp)

    drugs = ""
    if "results" in datos:
        for elem in datos['results']:
            if 'generic_name' in elem['openfda']:
                drugs += "<li>" + str(elem['openfda']['manufacturer_name'][0]) +"</li>"
            else:
                drugs += "<li>" +("No encontrado") +"</li>"
                continue
    return drugs

def advertencias(warnings): #Funcion que obtiene los datos de warnings de openfda
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", warnings, None, headers)
    respuesta = conn.getresponse()
    resp = respuesta.read().decode("utf-8")
    conn.close()
    datos = json.loads(resp)

    drugs = ""
    for elem in datos['results']:
        if 'warnings' in elem:
            drugs += "<li>" + str(elem['warnings']) +"</li>"
        else:
            drugs += "<li>" + ("No hay advertencias") +"</li>"
            continue
    return drugs


def informacion(drugs): #Pagina html donde se muestra la informacion almacenada en drugs
    info = """
          <!doctype html>
          <html>
          <body style='background-color: DeepSkyBlue'>
            <h1>Drugs</h2>
          <body>
          <html>
          <ul>
        """

    info += drugs
    info += """</ul></body></html>"""

    return info

@app.route("/") #Pagina html con los formularios donde seleccionamos la info que queremos ver
def paginaHTML():
    contenido = """
        <!DOCTYPE html>
        <html>
        <body>
        <body style='background-color: turquoise'>
        <h2>Active ingredient</h2>
        <form action="searchDrug">
          active_ingredient:<br>
          <input type="text" name="active_ingredient">
          <br>
          Limit:<br>
          <input type="text" name="limit">
          <br><br>
          <input type="submit" value="Submit">
        </form>
        </body>
        </html>"""
    contenido +="""
        <!DOCTYPE html>
        <html>
        <body>
        <h2>Company</h2>
        <form action="searchCompany">
          company:<br>
          <input type="text" name="company">
           <br>
          Limit:<br>
          <input type="text" name="limit">
          <br><br>
          <input type="submit" value="Submit">
        </form>
        </body>
        </html>"""
    contenido +="""
        <!DOCTYPE html>
        <html>
        <body>
        <h2>Drugs list</h2>
        <form action="listDrugs">
          Limit:<br>
          <input type="text" name="limit">
          <br><br>
          <input type="submit" value="Submit">
        </form>
        </body>
        </html>"""
    contenido +="""
        <!DOCTYPE html>
        <html>
        <body>
        <h2>Companies list</h2>
        <form action="listCompanies">
          Limit:<br>
          <input type="text" name="limit">
          <br><br>
          <input type="submit" value="Submit">
        </form>
        </body>
        </html>"""
    contenido += """
            <!DOCTYPE html>
            <html>
            <body>
            <h2>Warnings list</h2>
            <form action="listWarnings">
              Limit:<br>
              <input type="text" name="limit">
              <br><br>
              <input type="submit" value="Submit">
            </form>
            </body>
            </html>"""

    return contenido


@app.route('/redirect') #Extension lV, redirige a la pagina principal
def redireccion():
    return redirect("http://localhost:8000/", code=302)

@app.route('/secret') #Extensin lV, devuelve info a cerca de que no esta permitido el acceso a la URL
def autenticacion():
    abort(401)
if __name__ == "__main__": #Establecemos port y host
    app.run(host='0.0.0.0',port=8000)
