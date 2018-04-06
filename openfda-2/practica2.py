import http.client #Este modulo define las clases que implementan el lado del cliente de los protocolos http y https
import json #Importamos el modulo json para poder trabajar de forma sencilla con archivos JSON
headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection('api.fda.gov') #Establecer conexión con el servidor
conn.request('GET', '/drug/label.json?&search=active_ingredient:"acetylsalicylic+acid"&limit=100', None, headers)#Enviar solicitud al servidor
#Ponemos limite 100, pues nos piden información sobre todos los medicamentos
respuesta = conn.getresponse() #Obtener respuesta

resp = respuesta.read().decode("utf-8")#Leer respuesta y descodificar en formato utf-8
conn.close() #Cerrar la conexión al servidor

datos = json.loads(resp) # Convierte un str de JSON en datos con estructura python, en concreto un diccionario

for elem in datos['results']: #Iteramos sobre los elementos del diccionario que tienen como clave results
    if elem['openfda']: #Queremos acceder a los valores asociados a la clave openfda
        print("El medicamento con id", elem['id'], "ha sido fabricado por", str(elem['openfda']['manufacturer_name'])[2:-2])
        #Imprimimos el nombre del fabricante cuyo medicamento contiene ácido acetilsalicílico como principio activo
    else: #En caso de que carezca de la clave openfda, le indicamos que continue con el siguiente medicamento
        print("El medicamento con id", elem['id'], "no tiene nombre de fabricante especificado")
        continue