import socket

# Primero creamos el socket
# Siempre utilizaremos esos parámetros:
#  tipo de socket: AF_INET y SOCK_STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Obtener informacion sobre el socket creado
print()
print("Socket creado:")
print(s)

numero= input("¿A dónde te quieres conectar?:")
# Ahora nos conectamos al servidor web de la universidad
# que se encuentra en el puerto 80
# Podemos usar tanto el nombre de dominio como su IP
s.connect((numero, 9008))

# Imprimimos de nuevo el Socket para ver como ha cambiado
print()
print("Conexión establecida. Socket: ")
print(s)