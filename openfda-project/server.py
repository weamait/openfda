from flask import request
import http.client
import json
from flask import Flask,redirect,abort

app = Flask(__name__)


@app.route("/searchDrug")
def buscar_drugs():
    ingactivo = request.args.get('active_ingredient').replace(" ", "%20")
    limit = request.args.get('limit')
    if limit:
        gestion = gestionopenfda("/drug/label.json?search=active_ingredient:"+ingactivo+"&limit="+limit)
        mi_html = informacion(gestion)
    else:
        gestion = gestionopenfda("/drug/label.json?search=active_ingredient:" + ingactivo + "&limit=10")
        mi_html = informacion(gestion)
    return mi_html

@app.route("/searchCompany")
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

@app.route("/listDrugs")
def lista_medicamentos():
    medicamentos = request.args.get('limit')
    gestion = gestionopenfda("/drug/label.json?&limit="+medicamentos)
    mi_html = informacion(gestion)
    return mi_html

@app.route("/listCompanies")
def lista_empresas():
    empresas = request.args.get('limit')
    gestion1 = gestionopenfda1("/drug/label.json?&limit="+empresas)
    mi_html = informacion(gestion1)
    return mi_html

@app.route("/listWarnings")
def lista_advertencias():
    adver = request.args.get('limit')
    warnings = advertencias("/drug/label.json?&limit="+adver)
    mi_html = informacion(warnings)
    return mi_html


def gestionopenfda(gestion):
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", gestion, None, headers)
    respuesta = conn.getresponse()
    resp = respuesta.read().decode("utf-8")
    conn.close()
    datos = json.loads(resp)

    drugs = ""
    if "results" in datos:
        for elem in datos['results']:
            if 'generic_name' in elem['openfda']:
                drugs += "<li>" + str(elem['openfda']['generic_name'][0]) +"</li>"
            else:
                drugs += "<li>" + ("No encontrado") +"</li>"
                continue
    return drugs


def gestionopenfda1(gestion1):
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

def advertencias(warnings):
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


def informacion(drugs):
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

@app.route("/")
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


@app.route('/redirect')
def redireccion():
    return redirect("http://localhost:8000/", code=302)

@app.route('/secret')
def autenticacion():
    abort(401)
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
