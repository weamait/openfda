import http.client
import json
#importamos el modulo http.client ya que define las clases que implementan el lado del cliente de los protocolos http y https
#importamos el modulo json para poder trabajar de forma sencilla con archivos JSON
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #Establecer conexión con el servidor
conn.request("GET", "/drug/label.json", None, headers) #Enviar solicitud al servidor
#Si no incluimos limite, por defecto es 1
respuesta = conn.getresponse() #Obtener respuesta

resp = respuesta.read().decode("utf-8") #Leer respuesta y descodificar en formato utf-8
conn.close() #Cerrar la conexión al servidor

medicamentos = json.loads(resp) # Convierte str de JSON en datos con estructura python, en concreto un diccionario

med_res = medicamentos['results'] #Clave del diccionario de la que extraeremos la información solicitada
print("El identificador es", med_res[0]['id'], ", su propósito es", med_res[0]['purpose'], "y su fabricante es",med_res[0]['openfda']['manufacturer_name'])
#Imprimimos el identificador, proposito y fabricante