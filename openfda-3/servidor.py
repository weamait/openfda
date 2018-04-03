import socket
import http.client
import json

# Configuracion del servidor: IP, Puerto
IP = "192.168.0.158"
PORT = 9070
MAX_OPEN_REQUESTS = 5

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=10", None, headers)
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
      <body style='background-color: turquoise'>
        <h1>Los diez medicamentos son los siguientes:</h1>
      </body>
      </html>
    """
    for elem in repos['results']:
        if elem['openfda']:
            print("El medicamento es:", elem['openfda']['generic_name'][0])
            contenido += (elem['openfda']['generic_name'][0])
            contenido+="</br></body></html>"
        else:
            continue

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

# Crear un socket para el servidor. Es por el que llegan las
# peticiones de los clientes. Sentido: Cliente -> Servidor
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Asociar el socket a la direccion IP y puertos del servidor
    serversocket.bind((IP, PORT))

    # Se trata de un socket de servidor, sobre el que escucharemos
    # Se permiten MAX_OPEN_REQUESTS solicitudes que se encolan antes
    # El resto se rechazan
    serversocket.listen(MAX_OPEN_REQUESTS)

    # Bucle principal del servidor. El servidor se queda escuchando
    # el "socket" hasta que llegue una conexion de un cliente
    # En ese momento la atiende. Para ello recibe otro socket que le
    # permite comunicarse con el cliente
    while True:
        # Esperar a que lleguen conexiones del exterior
        # Cuando llega una conexion nueva, se obtiene un nuevo socket para
        # comunicarnos con el cliente. Este sockets
        # contiene la IP y Puerto del cliente
        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        # Ahora procesamos la peticion del cliente, pasandole el
        # socket como argumento
        # now do something with the clientsocket
        # in this case, we'll pretend this is a non threaded server
        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")