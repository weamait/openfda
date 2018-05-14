from flask import Flask
from flask import request
import http.client
import json

app = Flask(__name__)


@app.route("/searchDrug")
def buscar_drugs():
    ingactivo = request.args.get('active_ingredient').replace(" ", "%20")
    gestion=gestionopenfda("/drug/label.json?search=active_ingredient:"+ingactivo+"&limit=10")
    mi_html= paginaHTML(gestion)
    return mi_html

@app.route("/searchCompany")
def buscar_empresa():
    empresa = request.args.get('company').replace(" ", "%20")
    gestion = gestionopenfda("/drug/label.json?search=company:"+empresa+"&limit=10")
    mi_html = paginaHTML(gestion)
    return mi_html

@app.route("/listDrugs")
def lista_medicamentos():
    medicamentos = request.args.get("generic_name").replace(" ", "%20")
    gestion = gestionopenfda("/drug/label.json?&search=generic_name:"+medicamentos+"&limit=10")
    mi_html = paginaHTML(gestion)
    return mi_html

@app.route("/listCompanies")
def lista_empresas():
    empresas = request.args.get("manufacturer_name").replace(" ", "%20")
    gestion = gestionopenfda("/drug/label.json?&limit=11&search=manufacturer_name:"+empresas+"&limit=10")
    mi_html = paginaHTML(gestion)
    return mi_html

def gestionopenfda(gestion):
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", gestion, None, headers)
    respuesta = conn.getresponse()
    resp = respuesta.read().decode("utf-8")
    conn.close()
    datos = json.loads(resp)

    drugs=""
    for elem in datos['results']:
        if elem['openfda']:
            drugs += str(elem['openfda']['generic_name'][0])
            drugs += "<br>"
        else:
            drugs += ("No encontrado")
            drugs += "<br>"
            continue
    return drugs
@app.route("/")
def paginaHTML(): #crear página web con formularios o alguna pregunta o lo que sea.
    contenido = """
        <!DOCTYPE html>
        <html>
        <body>
        <h2>ACtive ingredient</h2>
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
    app.run(host='0.0.0.0',port=8002)
