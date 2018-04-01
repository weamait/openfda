import socket

IP = "192.168.0.161"
PORT = 10058
MAX_OPEN_REQUESTS = 5

import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

def process_client(clientsocket):
    """Funcion que atiende al cliente. Lee su peticion (aunque la ignora)
       y le envia un mensaje de respuesta en cuyo contenido hay texto
       en HTML que se muestra en el navegador"""

    # Leemos a traves del socket el mensaje de solicitud del cliente
    # Pero no hacemos nada con el. Lo descartamos: con independencia de
    # lo que nos pida, siempre le devolvemos lo mismo
    mensaje_solicitud = clientsocket.recv(1024)

    # Empezamos definiendo el contenido, porque necesitamos saber cuanto
    # ocupa para indicarlo en la cabecera
    # En este contenido pondremos el texto en HTML que queremos que se
    # visualice en el navegador cliente
    contenido = """
      <!doctype html>
      <html>
      for elem in repos['results']:
        print("El identificador es:", elem['openfda']['generic_name'])
    """
    contenido +=elem
    contenido+="</body></html>"
    # Creamos el mensaje de respuesta. Tiene que ser un mensaje en
    # HTTP, o de lo contrario el navegador no lo entendera
    # (Hay que hablar HTTP)
    # Un mensaje HTTP esta compuesto de
    # Linea inicial
    # cabecera
    # Linea en blanco
    # Cuerpo (contenido a enviar)

    # -- Indicamos primero que todo OK. Cualquier peticion, aunque sea
    # -- incorrecta nos va bien (somos un servidor cutre...)
    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

    # -- Creamos el mensaje uniendo todas sus partes
    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()


# -----------------------------------------------
# ------ Aqui comienza a ejecutarse el servidor
# -----------------------------------------------

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serversocket.bind((IP, PORT))

    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")