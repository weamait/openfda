from flask import Flask
from flask import request
import http.client
import json

app = Flask(__name__)


@app.route("/searchDrug")
def buscar_drugs():
    ingactivo = request.args.get('active_ingredient').replace(" ", "%20")
    gestion = gestionopenfda("/drug/label.json?search=active_ingredient:"+ingactivo+"&limit=10")
    mi_html = informacion(gestion)
    return mi_html

@app.route("/searchCompany")
def buscar_empresa():
    empresa = request.args.get('manufacturer_name').replace(" ", "%20")
    gestion1 = gestionopenfda1("/drug/label.json?search=manufacturer_name:"+empresa+"&limit=10")
    mi_html = informacion1(gestion1)
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
    mi_html = informacion1(gestion1)
    return mi_html

@app.errorhandler(404)
def recurso_no_encontrado(error):
    notfound = """
              <!doctype html>
              <html>
              <body style='background-color: red'>
                <h1>Recurso no encontrado</h2>
              <body>
              <html>
            """
    return  notfound



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
                drugs += "<li>"
                drugs += str(elem['openfda']['generic_name'][0])
                drugs += "</li>"
            else:
                drugs += "<li>"
                drugs += ("No encontrado")
                drugs += "</li>"
                continue
    return drugs

def informacion(drugs):
    info = """
          <!doctype html>
          <html>
          <body style='background-color: turquoise'>
            <h1>Drugs</h2>
          <body>
          <html>
        """

    info += drugs
    info += """</ul></body></html>"""

    return info

def gestionopenfda1(gestion1):
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", gestion1, None, headers)
    respuesta = conn.getresponse()
    resp = respuesta.read().decode("utf-8")
    conn.close()
    datos1 = json.loads(resp)

    drugs1 = ""
    if "results" in datos1:
        for elem in datos1['results']:
            if 'generic_name' in elem['openfda']:
                drugs1 += "<li>"
                drugs1 += str(elem['openfda']['manufacturer_name'][0])
                drugs1 += "</li>"
            else:
                drugs1 += "<li>"
                drugs1 += ("No encontrado")
                drugs1 += "</li>"
                continue
    return drugs1

def informacion1(drugs1):
    info1 = """
          <!doctype html>
          <html>
          <body style='background-color: turquoise'>
            <h1>Drugs</h2>
          <body>
          <html>
        """

    info1 += drugs1
    info1 += """</ul></body></html>"""

    return info1




@app.route("/")
def paginaHTML(): #crear página web con formularios o alguna pregunta o lo que sea.
    contenido = """
        <!DOCTYPE html>
        <html>
        <body>
        <body style='background-color: turquoise'>
        <h2>Active ingredient</h2>
        <form action="/searchDrug">
          active_ingredient:<br>
          <input type="text" name="active_ingredient">
          <br>
          Limit:<br>
          <input type="text" name="active_ingredient">
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
        <form action="/searchCompany">
          company:<br>
          <input type="text" name="manufacturer_name">
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
        <form action="/listDrugs">
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
        <form action="/listCompanies">
          Limit:<br>
          <input type="text" name="limit">
          <br><br>
          <input type="submit" value="Submit">
        </form>
        </body>
        </html>"""

    return contenido



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
