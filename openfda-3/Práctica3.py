import socket

IP = "127.0.0.1"
PORT = 9012
MAX_OPEN_REQUESTS = 5
FILE_HTML = "API.html"

def process_client(clientsocket):

    mensaje_solicitud = clientsocket.recv(1024).decode("utf-8")
    
    import json
    import urllib.request

    with urllib.request.urlopen("https://api.fda.gov/drug/label.json?limit=10") as API:
        info = json.loads(API.read().decode())

    with open(FILE_HTML, "w") as f:
        contenido = """
        <!doctype html>
        <html>
          <head>
            <meta charset="utf-8">
            <title>API</title>
          </head>
           <body style='background-color: lightgreen'>
              <h1>¡Bienvenido a mi programa!</h2>
              <p>Se expresan a continuación los nombres de diez medicamentos.</p>
              <p>Para más información <a href="https://api.fda.gov/drug/label.json?limit=10">pulse aquí</a></p>
               """

        for i in range(10):
            text = str("Nombre del medicamento:" + info["results"][i]["openfda"].get("generic_name", ["No aparece información al respecto"])[0])
            contenido = str(contenido + "\n" + "<p>" + text + "</p>")

        f.write(contenido)
        f.close()

    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido)))

    mensaje_respuesta = str.encode( linea_inicial + cabecera + "\n" + contenido)  
    clientsocket.send(mensaje_respuesta)


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()
        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)
        clientsocket.close()

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")
