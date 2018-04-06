import http.client #Este modulo define las clases que implementan el lado del cliente de los protocolos http y https
import json #Importamos el modulo json para poder trabajar de forma sencilla con archivos JSON
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #Establecer conexión con el servidor
conn.request("GET", "/drug/label.json", None, headers) #Enviar solicitud al servidor
#Si no incluimos limite, por defecto es 1
respuesta = conn.getresponse() #Obtener respuesta

resp = respuesta.read().decode("utf-8") #Leer respuesta y descodificar en formato utf-8
conn.close() #Cerrar la conexión al servidor

datos = json.loads(resp) # Convierte str de JSON en datos con estructura python, en concreto un diccionario

print("El identificador es", datos['results'][0]['id'], ", su propósito es", str(datos['results'][0]['purpose'])[2:-2], "y su fabricante es",str(datos['results'][0]['openfda']['manufacturer_name'])[2:-2])
#Imprimimos el identificador, proposito y fabricante de un medicamento