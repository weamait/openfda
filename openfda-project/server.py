from flask import Flask
from flask import request
import http.client
import json

app = Flask(__name__)


@app.route("/searchDrug")
def buscar_drugs():
    ingactivo = request.args.get('active_ingredient')
    json=gestionopenfda("/drug/label.json?&limit=11&search=active_ingredient" + ingactivo)
    html= paginaHTML(json)
    return html

@app.route("/searchCompany")
def buscar_empresa():
    empresa = request.args.get('company')
    json = gestionopenfda("/drug/label.json?&limit=11&search=company" + empresa)
    html = paginaHTML(json)
    return html

@app.route("/listDrugs")
def lista_medicamentos():
    medicamentos = request.args.get("generic_name")
    json = gestionopenfda("/drug/label.json?&limit=11&search=generic_name" + medicamentos)
    html = paginaHTML(json)
    return html

@app.route("/listCompanies")
def lista_empresas():
    empresas = request.args.get("manufacturer_name")
    json = gestionopenfda("/drug/label.json?&limit=11&search=manufacturer_name" + empresas)
    html = paginaHTML(json)
    return html

def gestionopenfda():
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?&limit=11", None, headers)
    respuesta = conn.getresponse()

    resp = respuesta.read().decode("utf-8")
    conn.close()
    datos = json.loads(resp)

    for elem in datos['results']:
        if elem['openfda']:
            datos = ("El medicamento es:", elem['openfda']['generic_name'][0])
        else:
            datos= ("No encontrado")
            continue
    return datos
@app.route("/")
def paginaHTML(): #crear página web con formularios o alguna pregunta o lo que sea.
    contenido = """
          <!DOCTYPE html>
            <html>
            <body>
            <body style='background-color: turquoise'>

            <h2>HTML Forms</h2>

            <form action="/action_page.php">
              Search Drug:<br>
              <input type="text" name="searchDrug">
              <br>
              Search company:<br>
              <input type="text" name="searchCompany">
              <br><br>
              <input type="submit" value="Submit">
            </form> 

            <p>If you click the "Submit" button, the form-data will be sent to a page called "/action_page.php".</p>

            </body>
            </html>"""
    return contenido



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
