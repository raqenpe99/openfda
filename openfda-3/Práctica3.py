import socket

IP = "127.0.0.1"
PORT = 9011
MAX_OPEN_REQUESTS = 5

def process_client(clientsocket):

    mensaje_solicitud = clientsocket.recv(1024).decode("utf-8")
    
    import json
    import urllib.request

    with urllib.request.urlopen("https://api.fda.gov/drug/label.json?limit=10") as API:
        info = json.loads(API.read().decode())
    
    def crea_lista(info): #Nos crea una lista con los nombres de cada medicamento para el posterior manejo de los datos-
                          #Si no tiene nombre genérico, se almacena su identificador.
        nombres=[]
        for i in range(10):
            text = info["results"][i]["openfda"].get("generic_name",  [info["results"][i]["id"]])[0]
            nombres.append(text)
        return nombres

    def crea_html(nombres): #Genera el contenido que será devuelto en un html, iterando sobre cada medicamento dentro de la lista
                            #ya creada y agrupándo los nombres en una tabla.
                            #A continuación imprime la información en pantalla.
        contenido = """
        <!doctype html>
        <html>
          <head>
            <meta charset="utf-8">
            <title>API</title>
          </head>
           <body style='background: linear-gradient(to right, #D358F7, #FF0040)'>
              <h1>Obtención de datos Openfda:</h2>
              <p>Se expresan a continuación los nombres de diez medicamentos.</p>
              <p>Para más información sobre ellos, <a href="https://api.fda.gov/drug/label.json?limit=10">pulse aquí</a></p>
              <img src="https://2.bp.blogspot.com/-_QDuJunXuyM/WJxbPq_5XsI/AAAAAAAASls/84d8ZrZYoCMyt_jigvCRmqGxJjITZjjcACLcB/s1600/medico.jpg" border="1" width="500" height="500" align="right">
              <table style="width:50%" border="4">
              <tr>
              <th><p style="color:white;"style="font-size:50px;">NOMBRES</p>\n"""


        for medicamento in nombres:
            contenido = str(contenido + "\n" + "<tr>\n   <th><p style='font-size:12px'>" + medicamento + '</p></th>\n  </tr>\n')
            
            print("Medicamento:", medicamento)

            
        return contenido
            
        
    #Definimos a continuación  el contenido que ya hemos definido en crea_html, para lo cual llamamos a la primera función:
    contenido=crea_html(crea_lista(info))
    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(contenido))) #El contenido será nuestra función html

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
