import socket #Proporciona acceso a la interfaz de socket BSD
import http.client #Define las clases que implementan el lado del cliente de los protocolos http y https
import json # Permite trabajar de forma sencilla con archivos JSON

# Configuracion del servidor: IP, Puerto
IP = "127.0.0.1"
PORT = 7793
MAX_OPEN_REQUESTS = 5 #Indica el máximo número de peticiones que puede recibir

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov") #Establecer conexión con el servidor
conn.request("GET", "/drug/label.json?&limit=10", None, headers) #Enviar solicitud al servidor
#Ponemos limite 10, pues nos piden información sobre 10 medicamentos
respuesta = conn.getresponse() #Obtener respuesta

resp = respuesta.read().decode("utf-8")#Leer respuesta y descodificar en formato utf-8
conn.close() #Cerrar la conexión al servidor

datos = json.loads(resp) #Convierte un str de JSON en datos con estructura python, en concreto un diccionario

def process_client(clientsocket): #Función que atiende al cliente y envia respuesta con texto HTML mostrado en el navegador

    mensaje_solicitud = clientsocket.recv(1024) #Leemos el mensaje de solicitud del cliente a traves del socket

    # Definimos el contenido, donde pondremos el texto en HTML que queremos que se visualice en el navegador cliente
    #También el color y el título que queremos que aparezca
    contenido = """
      <!doctype html>
      <html>
      <body style='background-color: turquoise'> 
        <h1>Medicamentos obtenidos de la API OpenFDA drugs labelling:</h1>
      </body>
      </html>
    """
    for elem in datos['results']: #Iteramos sobre los elementos del diccionario que tienen como clave results
        if elem['openfda']: #Queremos acceder a los valores asociados a la clave openfda
            print("El medicamento es:", elem['openfda']['generic_name'][0]) #Imprimir el nombre de los medicamentos
            contenido += (elem['openfda']['generic_name'][0]) #Ir añadiendo al contenido el nombre de los 10 medicamentos
            contenido+="</br></body></html>"
        else: #En caso de que carezca de la clave openfda, le indicamos que continue con el siguiente medicamento
            continue

    # El mensaje de respuesta tiene que ser un mensaje en HTTP (o el navegador no lo entendera)
    # Un mensaje HTTP esta compuesto de linea inicial, cabecera y el contenido

    linea_inicial = "HTTP/1.1 200 OK\n" #Indicar OK, cualquier petición nos va bien
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

    # Unimos todas las partes para crear un mensaje definitivo
    mensaje_respuesta = str.encode(linea_inicial + cabecera + "\n" + contenido)
    clientsocket.send(mensaje_respuesta)
    clientsocket.close()

# Crear un socket para el servidor, por el que llegan las peticiones de los clientes. Sentido: Cliente -> Servidor
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Asociar el socket a la direccion IP y puertos del servidor
    serversocket.bind((IP, PORT))

    serversocket.listen(MAX_OPEN_REQUESTS)#Socket sobre el que escucharemos el máximo número de peticiones que indicamos al principio(5)

    #El servidor se queda escuchando el "socket" hasta que llegue una conexion de un cliente, en ese momento la atiende.
    # Para ello recibe otro socket que le permite comunicarse con el cliente
    while True:
    #Llega una conexion nueva, se obtiene un nuevo socket (contiene la IP y Puerto del cliente) para comunicarnos con el cliente.
        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

    #Procesamos la peticion del cliente, pasandole el socket como argumento
        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")