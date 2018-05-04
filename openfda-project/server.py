from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/searchDrug")
def hello():
    ingactivo = request.args.get('active_ingredient')
    return "Hello World!"+ingactivo

@app.route("/searchCompany")
def buscar_empresa():
    empresa = request.args.get('company')
    return empresa

@app.route("/listDrugs")
def lista_medicamentos():
    medicamentos = request.args.get("generic_name")
    return medicamentos

@app.route("/listCompanies")
def lista_empresas():
    empresas = request.args.get("manufacturer_name")
    return empresas

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
