import http.client
import json
#importamos el modulo http.client ya que define las clases que implementan el lado del cliente de los protocolos http y https
#importamos el modulo json para poder trabajar de forma sencilla con archivos JSON
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #Establecer conexión con el servidor
conn.request("GET", "/drug/label.json?&limit=10", None, headers) #Enviar solicitud al servidor
#Ponemos limite 10, pues nos piden información sobre 10 medicamentos
respuesta = conn.getresponse() #Obtener respuesta

resp = respuesta.read().decode("utf-8") #Leer respuesta y descodificar en formato utf-8
conn.close() #Cerrar la conexión al servidor

medicamentos = json.loads(resp) # Convierte un str de JSON en datos con estructura python, en concreto un diccionario

for elem in medicamentos['results']: #Iteramos sobre los elementos del diccionario que tienen como clave results
    print("El identificador es:", elem['id'])
    #Imprimimos el identificador